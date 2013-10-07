import os

__version__ = '0.1.0'

_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_data_dir():
    return os.path.join(_ROOT, 'data')

DATA_DIR = get_data_dir()