from setuptools import setup
from src.config import __version__
import doctest
import os
import fnmatch
import importlib
import src.read_headers


def locate(pattern, root=os.curdir):
    '''Locate all files matching supplied filename pattern in and below
    supplied root directory.'''
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)

# run doctest unit tests in all source Python scripts
failures = 0
scripts = locate('*.py', root='src')
for script in scripts:
    script = (os.path.relpath(script)[:-len('.py')]).replace('/', '.')
    print '**', script, '**'
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
                   'pybioclim':'src'
                   },
      package_data = {
                      'pybioclim': ['data/*.bil', 'data/*.hdr', 'data/*.pkl'],
                      }
      )
