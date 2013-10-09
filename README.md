This is a simple Python package for interacting with BIOCLIM climate data in 
Python. The data files are included in the repository.

Requirements:

* numpy
* gdal
* gitpython
* cython
* matplotlib/Basemap (optional, for drawing maps)

To install:

    python setup.py install

To use:

    >>> import pybioclim
    
    # get the GDAL Dataset object
    >>> data = pybioclim.get_dataset('bio1')
    >>> array = data.ReadAsArray()
    
    # get a list of values at specified lat/lon coordinates
    >>> lat_lon = [(0,0),
    ...            (-20,-170),
    ...            (50, 12.2527)]
    >>> values = pybioclim.get_values('bio1', lat_lon)
    
    # compute the spatial variance within a given radius (in km)
    >>> variance = pybioclim.get_spatial_variance('bio1', lat_lon, radius=25)
    
    # draw a map of a BIOCLIM variable (using matplotlib and Basemap)
    pybioclim.draw_map('bio17', log=True)
