import os

__version__ = '0.1.0'

# get the path to the package data directory
_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_data_dir():
    return os.path.join(_ROOT, 'data')
DATA_DIR = get_data_dir()
DATA_PATHS = ('.', DATA_DIR,)

def find_data(name):
    for data_dir in DATA_PATHS:
        path = os.path.join(data_dir, name)
        if os.path.exists(path):
            return path

# upper left and lower right corners of a BIOCLIM raster file (lat,lon)
ul = (90, -180)
lr = (-60, 180)