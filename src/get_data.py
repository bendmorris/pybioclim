import os
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

def get_values(file, points, ul_x=ul[1], ul_y=ul[0], lr_x=lr[1], lr_y=lr[0]):
    '''Given a .bil file (or other file readable by GDAL) and a set of (lat,lon) 
    points, return a list of values for those points. -9999 will be converted to 
    None.
    
    >>> lat_lons = [(10,10), (20,20), (0,0)]
    >>> get_values('bio1', lat_lons)
    [254, 252, None]
    '''

    data = get_dataset(file)
    raster = data.ReadAsArray()
    
    xdim = dim(lr_x-ul_x, data.RasterXSize)
    ydim = dim(ul_y-lr_y, data.RasterYSize)

    result = []
    for lat, lon in points:
        y, x = xy_coords(lat, lon, ul_x, ul_y, xdim, ydim)
        value = raster[y,x]
        if value == -9999: value = None
        result.append(value)
    return result
