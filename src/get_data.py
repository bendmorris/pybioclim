import os
import math
import gdal
from read_headers import variable_names
from coords_to_raster_xy import xy_coords
from config import DATA_DIR, ul, lr


loaded_datasets = {}

def get_dataset(file):
    '''Returns an open GDAL dataset object for the given BIOCLIM data file.
    
    >>> data = get_dataset('bio1')
    >>> import os
    >>> os.path.basename(data.GetDescription())
    'bio1.bil'
    '''
    if not '.' in file: file += '.bil'
    if not file in loaded_datasets:
        loaded_datasets[file] = gdal.Open(os.path.join(DATA_DIR, file))
    return loaded_datasets[file]

def dim(width, size):
    return float(width)/size

def get_values(file, points, ul=ul, lr=lr):
    '''Given a .bil file (or other file readable by GDAL) and a set of (lat,lon) 
    points, return a list of values for those points. -9999 will be converted to 
    None.
    
    >>> lat_lons = [(10,10), (20,20), (0,0)]
    >>> get_values('bio1', lat_lons)
    [254, 252, None]
    '''

    data = get_dataset(file)
    raster = data.ReadAsArray()
    
    size = data.RasterYSize, data.RasterXSize
    xdim = dim(lr[1]-ul[1], size[1])
    ydim = dim(ul[0]-lr[0], size[0])
    dims = (ydim, xdim)

    result = [raster[xy_coords((lat, lon), ul, dims, size)] for (lat, lon) in points]
    result = [None if value == -9999 else value for value in result]

    return result

def radians(deg):
    '''Converts degrees to radians.

    >>> abs(radians(0)) < 0.00001
    True
    >>> abs(radians(90) - math.pi/2) < 0.00001
    True
    >>> abs(radians(180) - math.pi) < 0.00001
    True
    >>> abs(radians(270) - 3*math.pi/2) < 0.00001
    True
    >>> abs(radians(360) - 2*math.pi) < 0.00001
    True
    '''
    return deg/180.*(math.pi)

def distance(p1, p2):
    '''Approximate distance between two lat/lon points, in km.
    
    p1 and p2 should be tuples containing (lat,lon)
    
    >>> 1250 <= distance((50, -50), (40, -40)) <= 1500
    True
    >>> 1000 <= distance((50, -50), (40, -50)) <= 1250
    True
    '''
    y1, x1 = p1
    y2, x2 = p2
    dy = radians(abs(y2-y1))
    dx = radians(abs(x2-x1))
    a = math.sin(dy/2)**2 + math.sin(dx/2)**2 * math.cos(radians(y1)) * math.cos(radians(y2))
    c = 2 * math.atan2(a**0.5, (1-a)**0.5)
    return 6371 * c

def points_within_distance(start_point, radius, ul, dims):
    '''Find the set of lat/lon coords in a raster that are within `radius` km of 
    the starting point.'''
    pass
    