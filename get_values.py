import gdal
from read_headers import variable_names
from coords_to_raster_xy import xy_coords


def get_values(file, points, ul_x=None, ul_y=None, lr_x=None, lr_y=None):
    '''Given a .bil file (or other file readable by GDAL) and a set of (lat,lon) 
    points, return a list of values for those points. -9999 will be converted to 
    None.'''

    data = gdal.Open(file)
    raster = data.ReadAsArray()
    if ul_x is None: ul_x = -180
    if ul_y is None: ul_y = 90
    if lr_x is None: lr_x = 180
    if lr_y is None: lr_y = -60
    
    xdim = (float(lr_x-ul_x)/data.RasterXSize)
    ydim = (float(ul_y-lr_y)/data.RasterYSize)

    result = []
    for lat, lon in points:
        y, x = xy_coords(lat, lon, ul_x, ul_y, xdim, ydim)
        value = raster[y,x]
        if value == -9999: value = None
        result.append(value)
    return result


if __name__ == '__main__':
    import sys
    file = sys.argv[1]
    n = 2
    points = []
    while len(sys.argv) > n:
        points.append((float(sys.argv[n]), float(sys.argv[n+1])))
        n += 2
    print get_values(file, points)
