import doctest
import math
import numpy as np


def memoize(f):
    memos = {}
    def new_f(*args, **kwargs):
        if not (args, str(kwargs)) in memos:
            memos[(args, str(kwargs))] = f(*args, **kwargs)
        return memos[(args, str(kwargs))]
    return new_f

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

@memoize
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

@memoize
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

@memoize
def points_within_distance(start_point, radius, ul, dims):
    '''Find the set of lat/lon coords in a raster that are within `radius` km of 
    the starting point.
    
    >>> points_within_distance((0,0), 0, (90, -180), (0.5, 0.5))
    [(0, 0)]
    >>> points_within_distance((0,0), 100, (90, -180), (0.5, 0.5))
    [(-0.5, -0.5), (-0.5, 0.0), (-0.5, 0.5), (0.0, -0.5), (0, 0), (0.0, 0.5), (0.5, -0.5), (0.5, 0.0), (0.5, 0.5)]
    '''
    
    box_size = 1
    points = set([start_point])
    seen = set([start_point])
    last_point_size = 1
    while True:
        b, a = [np.linspace(start_point[i]-dims[i]*box_size, 
                            start_point[i]+dims[i]*box_size, 
                            1+box_size*2)
                for i in (0,1)]
        for bi in b:
            for ai in a:
                if not ((bi, ai)) in seen:
                    dist = distance((bi,ai),start_point)
                    if dist <= radius: points.add((bi,ai))
                    seen.add((bi, ai))
                
        if not len(points) > last_point_size: break
        last_point_size = len(points)
        box_size += 1

    return sorted(list(points))
