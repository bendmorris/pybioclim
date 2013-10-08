import doctest


def xy_coords(point, ul, dims, sizes=None):
    '''Given a latitude/longitude pair and resolution information about the 
    raster file, gives the row/column of the corresponding raster matrix.

    >>> xy_coords((0, 0), (0, 0), (10, 10), (100, 100))
    (0, 0)
    >>> xy_coords((0, 10), (0, 0), (10, 10), (100, 100))
    (0, 1)
    >>> xy_coords((-10, 0), (0, 0), (10, 10), (100, 100))
    (1, 0)
    >>> xy_coords((-2, 0), (0, 0), (0.5, 2.5), (100, 100))
    (4, 0)
    >>> xy_coords((-5, 0), (0, 0), (1, 1), (4, 4))
    (1, 0)
    >>> xy_coords((0, 180), (0, 0), (1, 1), (180, 360)) == xy_coords((0, -180), (0, 0), (1, 1), (180, 360))
    True
    '''
    
    # point and ul are (lat, lon) tuples;
    # positive y-direction in raster vs on globe are reversed
    # (positive is North, but down in raster)
    dy = int(round((ul[0]-point[0])/dims[0]))
    dx = int(round((point[1]-ul[1])/dims[1]))
    if not sizes is None:
        dy %= sizes[0]
        dx %= sizes[1]

    return dy, dx
