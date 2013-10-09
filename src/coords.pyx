import doctest
import numpy as np
import math


cdef extern from "math.h":
    double sin(double)
    double cos(double)
    double atan2(double, double)

cdef double pi = 3.141592654

cpdef xy_coords(point, ul, dims, sizes=None):
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
    cdef int dy, dx
    
    dy = int(round((ul[0]-point[0])/dims[0]))
    dx = int(round((point[1]-ul[1])/dims[1]))
    if not sizes is None:
        dy %= sizes[0]
        dx %= sizes[1]

    return dy, dx

cpdef double radians(double deg):
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
    return deg/180.*(pi)

cpdef double distance(p1, p2):
    '''Approximate distance between two lat/lon points, in km.
    
    p1 and p2 should be tuples containing (lat,lon)
    
    >>> 1250 <= distance((50, -50), (40, -40)) <= 1500
    True
    >>> 1000 <= distance((50, -50), (40, -50)) <= 1250
    True
    >>> 110 <= distance((0,0),(1,0)) <= 112
    True
    '''
    cdef float y1, y2, x1, x2, dy, dx, a, c
    y1, x1 = p1
    y2, x2 = p2
    dy = radians(abs(y2-y1))
    dx = radians(abs(x2-x1))
    a = sin(dy/2)**2 + sin(dx/2)**2 * cos(radians(y1)) * cos(radians(y2))
    c = 2 * atan2(a**0.5, (1-a)**0.5)
    return 6371 * c

cpdef points_within_distance(start_point, double radius, ul, dims):
    '''Find the set of lat/lon coords in a raster that are within `radius` km of 
    the starting point.
    
    >>> points_within_distance((0,0), 0, (90, -180), (0.5, 0.5))
    [(0.0, 0.0)]
    >>> points_within_distance((0,0), 100, (90, -180), (0.5, 0.5))
    [(-0.5, -0.5), (-0.5, 0.0), (-0.5, 0.5), (0.0, -0.5), (0.0, 0.0), (0.0, 0.5), (0.5, -0.5), (0.5, 0.0), (0.5, 0.5)]
    '''
    
    cdef double sx, sy, lat_width, lon_width
    sy, sx = start_point
    lat_width = distance((sy-dims[0]/2, sx), (sy+dims[0]/2, sx))
    lon_width = distance((sy, sx-dims[1]/2), (sy, sx+dims[1]/2))
    box_size = (int(radius/lat_width)+1, int(radius/lon_width)+1)
    points = []

    b, a = [np.linspace(start_point[i]-dims[i]*box_size[i], 
                        start_point[i]+dims[i]*box_size[i], 
                        1+box_size[i]*2)
            for i in (0,1)]
    for bi in b:
        for ai in a:
            dist = distance((bi,ai),start_point)
            if dist <= radius: points.append((bi,ai))
                
    return points
