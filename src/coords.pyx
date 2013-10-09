import doctest
import numpy as np
import math


cdef extern from "math.h":
    double sin(double)
    double cos(double)
    double atan2(double, double)

cdef double pi = 3.141592654

cpdef xy_coords(py, px, uly, ulx, dimy, dimx):
    '''Given a latitude/longitude pair and resolution information about the 
    raster file, gives the row/column of the corresponding raster matrix.

    >>> xy_coords(90, -180, 90, -180, 10, 10)
    (0, 0)
    >>> xy_coords(0, 10, 90, -180, 10, 10)
    (9, 19)
    >>> xy_coords(89, -179, 90, -180, 1, 1)
    (1, 1)
    >>> xy_coords(-10, 0, 0, 0, 10, 10)
    (1, 0)
    >>> xy_coords(-2, 0, 0, 0, 0.5, 2.5)
    (4, 0)
    >>> xy_coords(-5, 0, 0, 0, 1, 1)
    (5, 0)
    '''
    
    # positive y-direction in raster vs on globe are reversed
    # (positive is North, but down in raster)
    cdef int dy, dx
    dy = int((uly-py)/dimy)
    dx = int((px-ulx)/dimx)

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

cpdef double distance(double y1, double x1, double y2, double x2):
    '''Approximate distance between two lat/lon points, in km.
    
    p1 and p2 should be tuples containing (lat,lon)
    
    >>> 1250 <= distance(50,-50, 40,-40) <= 1500
    True
    >>> 1000 <= distance(50,-50, 40,-50) <= 1250
    True
    >>> 110 <= distance(0,0, 1,0) <= 112
    True
    '''
    dy = radians(abs(y2-y1))
    dx = radians(abs(x2-x1))
    a = sin(dy/2)**2 + sin(dx/2)**2 * cos(radians(y1)) * cos(radians(y2))
    c = 2 * atan2(a**0.5, (1-a)**0.5)
    return 6371 * c

cpdef points_within_distance(sy, sx, uly, ulx, dimy, dimx, double radius=40):
    '''Find the set of lat/lon coords in a raster that are within `radius` km of 
    the starting point.
    
    >>> points_within_distance(0,0, 90,-180, 0.5,0.5, 0)
    [(0.0, 0.0)]
    >>> points_within_distance(0,0, 90,-180, 0.5,0.5, 100)
    [(-0.5, -0.5), (-0.5, 0.0), (-0.5, 0.5), (0.0, -0.5), (0.0, 0.0), (0.0, 0.5), (0.5, -0.5), (0.5, 0.0), (0.5, 0.5)]
    '''
    
    cdef double lat_width, lon_width, dist, bi, ai
    cdef int box_y, box_x
    lat_width = distance(sy-dimy/2, sx, sy+dimy/2, sx)
    lon_width = distance(sy, sx-dimx/2, sy, sx+dimx/2)
    box_y = int(radius/lat_width)+1
    box_x = int(radius/lon_width)+1
    points = []

    b = np.linspace(sy-dimy*box_y, 
                    sy+dimy*box_y, 
                    1+box_y*2)
    a = np.linspace(sx-dimx*box_x, 
                    sx+dimx*box_x, 
                    1+box_x*2)
    for bi in b:
        for ai in a:
            dist = distance(sy,sx,bi,ai)
            if dist <= radius: points.append((bi,ai))
                
    return points
