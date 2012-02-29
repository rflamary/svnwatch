#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 29 14:38:58 2012

Script to notify the user for changes in a subversion repository.

this script is based on the program svnnotify

@author: remi.flamary àt gmail.com
"""

try:
    import pysvn, pynotify
except:
    print "Error while loading external depencencies."
    print "Make sure 'pysvn' and 'pynotify' is installed."
    exit()
    
import datetime, time, ConfigParser as cfg



def read_config():
    """Read the configuration file containing server, username and password"""
    global svn_root, svn_username, svn_password

    config_file = 'svnnotify.cfg'
    config_header = 'server'

    try:
        parser = cfg.ConfigParser()
        parser.read(config_file)
        svn_root = parser.get(config_header, 'server')
        svn_username = parser.get(config_header, 'user')
        svn_password = parser.get(config_header, 'pass')
    except BaseException as e:
        print "Error while parsing file '%s':" % config_file
        print e
        exit()

def notify(paths, authors):
    """Display the changed paths using libnotify"""
    title_string = 'New commits to repository'
    path_string = ', '.join(paths)
    author_string = ', '.join(authors)
    message_string = path_string
    
    if pynotify.init("SVN Monitor"):
        n = pynotify.Notification(title_string, message_string, "emblem-shared")
        n.show()

def log_message(paths, authors):
    """Print a log message containing the time, authors and paths"""
    now = datetime.datetime.now()
    now = now.strftime("%H:%M")
    path_string = ', '.join(paths)
    author_string = ', '.join(authors)
    print "[%s] Paths: %s -- Authors: %s" % (now, path_string, author_string)
    

def credentials(realm, username, may_save):
    """Return the default login credentials"""
    return True, svn_username, svn_password, False

def discover_changes(last_revision=pysvn.Revision(pysvn.opt_revision_kind.number, 0)):
    """Find out the changes occured since the last time this method is ran"""
    if last_revision is None:
        last_revision=pysvn.Revision(pysvn.opt_revision_kind.number, 0)
    client = pysvn.Client()
    client.callback_get_login = credentials
    log = client.log(
        svn_root, 
        discover_changed_paths=True,
        revision_end=last_revision
        )
    if len(log) is 1:
        return last_revision, None, None
    authors = []
    paths = []
    for entry in log[:-1]:
        if entry.author not in authors:
            authors.append(entry.author)
        for change in entry.changed_paths:
            path = change.path.split('/',2)[1]
            if path not in paths:
                paths.append(path)
    last_revision = log[0].revision
        
    return last_revision, authors, paths

if __name__ == '__main__':
    read_config()
    print 'Monitoring SVN repository: %s' % svn_root
    print '- Press %s to quit -' % '^C'
    last_revision = None
    while True:
        last_revision, authors, paths = discover_changes(last_revision)
        if paths is not None:
            log_message(paths, authors)
            notify(paths, authors)
        time.sleep(2*60)
