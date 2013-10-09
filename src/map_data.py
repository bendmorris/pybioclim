from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from config import ul, lr
from read_headers import variable_names
from get_data import get_dataset, extract_attributes, get_spatial_variance


def draw_map(file, map=None, show=True, title=None, log=False, map_type=None):
    '''Use Matplotlib's basemap to generate a map of a given BIOCLIM data 
    file.
    
    You can supply a Basemap object (in any projection) as the optional 
    keyword argument "map." If none is provided, the default Miller 
    projection will be used.'''
    
    data, raster, no_value, ul, dims, size = extract_attributes(file)
    data = get_dataset(file)
    lats = np.linspace(ul[0], ul[0]-dims[0]*size[0], size[0], endpoint=False)
    lons = np.linspace(ul[1], ul[1]+dims[1]*size[1], size[1], endpoint=False)
    if map_type == 'variance':
        x, y = np.meshgrid(lons, lats)
        data = np.zeros(x.shape)
        values = get_spatial_variance(file, 
                                      [(lat, lon) 
                                       for lat in lats 
                                       for lon in lons])
        for a in range(data.shape[0]):
            for b in range(data.shape[1]):
                data[a,b] = values.pop()
    
    # because missing data is entered as -9999, created a masked array so that 
    # these points will not be plotted
    values = np.ma.masked_where(raster==no_value, raster)
    
    # log transform data, if requested
    if log:
        if (values < 0).any():
            values -= min(values)
        values = np.log1p(values)
    
    plt.figure()
    if title is None:
        title = '%s' % file
        if file in variable_names:
            title += ': %s' % variable_names[file]
    plt.title(title)
    if map is None:
        map = Basemap(projection='mill',lon_0=0)
        map.drawcoastlines(linewidth=1)
        map.drawcountries(linewidth=1)
        map.drawstates(linewidth=0.5)
    
    x, y = np.meshgrid(lons, lats)
            
    map.pcolormesh(x, y, data=values, latlon=True, cmap=plt.cm.Spectral_r)
    cbar = plt.colorbar()
    
    if show: plt.show()