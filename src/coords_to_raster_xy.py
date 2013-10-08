import doctest


def xy_coords(lat, lon, ul_x, ul_y, x_dim, y_dim, x_size, y_size):
    '''Given a latitude/longitude pair and resolution information about the 
    raster file, gives the row/column of the corresponding raster matrix.

    >>> xy_coords(0, 0, 0, 0, 10, 10, 100, 100)
    (0, 0)
    >>> xy_coords(0, 10, 0, 0, 10, 10, 100, 100)
    (0, 1)
    >>> xy_coords(-10, 0, 0, 0, 10, 10, 100, 100)
    (1, 0)
    >>> xy_coords(-2, 0, 0, 0, 2.5, 0.5, 100, 100)
    (4, 0)
    >>> xy_coords(-5, 0, 0, 0, 1, 1, 4, 4)
    (1, 0)
    >>> xy_coords(0, 180, 0, 0, 1, 1, 360, 180) == xy_coords(0, -180, 0, 0, 1, 1, 360, 180)
    True
    '''

    dy = int(round((ul_y-lat)/y_dim)) % y_size
    dx = int(round((lon-ul_x)/x_dim)) % x_size

    return dy, dx


if __name__ == '__main__':
    doctest.testmod()
