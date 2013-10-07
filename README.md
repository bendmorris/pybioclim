This is a simple Python package for interacting with BIOCLIM climate data in 
Python. The data files are included in the repository.

To install:

    python setup.py install

To use:

    import pybioclim
    # get the GDAL Dataset object
    data = pybioclim.get_dataset('bio1')
    
    # get a list of values at specified lat/lon coordinates
    lat_lon = [(0,0),
               (-20,-170),
               (50, 12.2527)]
    values = pybioclim.get_values('bio1', lat_lon)
    
    # draw a map of a BIOCLIM variable
    pybioclim.draw_map('bio1')