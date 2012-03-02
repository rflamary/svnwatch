#!/usr/bin/env python

from distutils.core import setup
import os

ROOT = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(ROOT, 'README')).read()

setup(name='svnwatch',
      version='0.1.2',
      description='tool for monitoring commits on subversion repositories',
      long_description=README,
      author=u'Remi Flamary',
      author_email='remi.flamary@gmail.com',
      url='https://github.com/flam157/svnwatch/',
      platforms=['linux'],
      license = 'GPL',
      scripts=['svnwatch'],
      py_modules=['svnwatch'],
      requires=["argparse (>=0.1)"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: System :: Monitoring',
        'Topic :: Utilities'        
    ]
     )
