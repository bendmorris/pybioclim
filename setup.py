from setuptools import setup
from __init__ import __version__
import doctest
import os
import fnmatch
import importlib


def locate(pattern, root=os.curdir):
    '''Locate all files matching supplied filename pattern in and below
    supplied root directory.'''
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)

failures = 0
scripts = locate('*.py')
for script in scripts:
    print '**', script, '**'
    script = (os.path.relpath(script)[:-len('.py')]).replace('/', '.')
    print script
    mod = importlib.import_module(script)
    result = doctest.testmod(mod, verbose=True)
    failures += result.failed

if failures > 0: raise Exception('%s tests failed.' % failures)

setup(name='pybioclim',
      version=__version__,
      description='Python library for working with BIOCLIM climate data',
      author='Ben Morris',
      author_email='ben@bendmorris.com',
      url='https://github.com/bendmorris/pybioclim',
      packages=['pybioclim'],
      package_dir={
                'pybioclim':''
                },
      )
