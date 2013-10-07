import doctest


def xy_coords(lat, lon, ul_x, ul_y, x_dim, y_dim):
    '''Given a latitude/longitude pair and resolution information about the 
    raster file, gives the row/column of the corresponding raster matrix.

    >>> xy_coords(0, 0, 0, 0, 10, 10)
    (0, 0)
    >>> xy_coords(0, 10, 0, 0, 10, 10)
    (0, 1)
    >>> xy_coords(-10, 0, 0, 0, 10, 10)
    (1, 0)
    >>> xy_coords(-2, 0, 0, 0, 2.5, 0.5)
    (4, 0)
    '''

    dy = int(round((ul_y-lat)/y_dim))
    dx = int(round((lon-ul_x)/x_dim))

    return dy, dx


if __name__ == '__main__':
    doctest.testmod()
