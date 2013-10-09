from Cython.Build import cythonize
try:
    # compile all .pyx files to .c files
    cythonize('src/*.pyx', annotate=True)
except ImportError:
    pass
from setuptools import setup, Extension
import doctest
import os
import fnmatch
import importlib


__version__ = None

def do_setup():
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
                      },
      install_requires=['numpy', 'gdal'],
      extras_require={'draw_map':['matplotlib', 'mpl_toolkits.basemap']},
      entry_points={
        'console_scripts': [
            'pybioclim = pybioclim.__main__:main',
        ],
      },
      ext_modules=[Extension('pybioclim.coords', ['src/coords.c'],
                             extra_compile_args = ['-O3', '-ffast-math'],)],
      )


# before installing, build modules in-place so that tests can be run
import sys
args = sys.argv
sys.argv = [sys.argv[0], 'build_ext', '--inplace']
do_setup()

from src.config import __version__


def locate(pattern, root=os.curdir):
    '''Locate all files matching supplied filename pattern in and below
    supplied root directory.'''
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)

# run doctest unit tests in all source Python scripts
failures = 0
scripts = [x for x in locate('*.py', root='src')] + [x for x in locate('*.so', root='src')]
for script in scripts:
    script = (os.path.relpath(script)[:-len('.py')]).replace('/', '.')
    print '**', script, '**'
    mod = importlib.import_module(script)
    result = doctest.testmod(mod)
    failures += result.failed

if failures > 0: raise Exception('%s tests failed.' % failures)

sys.argv = args
do_setup()