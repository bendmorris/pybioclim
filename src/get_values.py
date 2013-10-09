import os
import math
import gdal
import numpy as np
from read_data import variable_names, metadata, read_header, get_dataset, extract_attributes
from coords import xy_coords, distance, points_within_distance
from config import DATA_PATHS, find_data


def get_values(file, points):
    '''Given a .bil file (or other file readable by GDAL) and a set of (lat,lon) 
    points, return a list of values for those points. -9999 will be converted to 
    None.
    
    >>> lat_lons = [(10,10), (20,20), (0,0)]
    >>> get_values('bio1', lat_lons)
    [257.0, 249.0, None]
    '''

    data, raster, no_value, ul, dims, size = extract_attributes(file)

    result = [float(raster[xy_coords((lat, lon), ul, dims, size)]) for (lat, lon) in points]
    result = [None if value == no_value else value for value in result]

    return result


def get_average(file, points, radius=40):
    '''Like get_values, but computes the average value within a circle of the 
    specified radius (in km).
    
    Missing values are ignored. Returns None if there were no values within the 
    circle.
    
    >>> lat_lons = [(10,10), (20,20), (0,0)]
    >>> get_average('bio1', lat_lons, 0)
    [257.0, 249.0, None]
    >>> get_average('bio1', lat_lons, 100) != get_average('bio1', lat_lons, 50) != get_average('bio1', lat_lons, 0)
    True
    '''

    data, raster, no_value, ul, dims, size = extract_attributes(file)
    
    result = []
    for point in points:
        within = points_within_distance(point, radius, ul, dims)
        raster_positions = [xy_coords((lat, lon), ul, dims, size) for (lat, lon) in within]
        values = [raster[pos] for pos in raster_positions if raster[pos] != no_value]
        if len(values) == 0: result.append(None)
        else:
            result.append(sum(values)/float(len(values)))

    return result


def get_spatial_variance(file, points, radius=40):
    '''Like get_values, but computes the spatial variance within a circle of the
    specified radius (in km).
    
    Missing values are ignored. Returns None if there were no values within the 
    circle.
    
    >>> lat_lons = [(10,10), (20,20), (0,0)]
    >>> get_spatial_variance('bio1', lat_lons, 0)
    [0.0, 0.0, None]
    >>> (get_spatial_variance('bio1', lat_lons[0:1], 100) >= 
    ... get_spatial_variance('bio1', lat_lons[0:1], 50) >= 
    ... get_spatial_variance('bio1', lat_lons[0:1], 0))
    True
    '''

    data, raster, no_value, ul, dims, size = extract_attributes(file)
    
    result = []
    for point in points:
        # because the distance between longitude points approaches 0 at the 
        # poles, only compute variance between 60 N and 60 S
        if abs(point[0]) > 60:
            result.append(None)
            continue

        within = points_within_distance(point, radius, ul, dims)
        raster_positions = [xy_coords((lat, lon), ul, dims, size) for (lat, lon) in within]
        values = [raster[pos] for pos in raster_positions if raster[pos] != no_value]
        if len(values) == 0: result.append(None)
        else:
            result.append(float(np.var(values)))

    return result
