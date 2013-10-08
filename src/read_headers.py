import os
import cPickle as pkl
from config import DATA_DIR


pkl_path = os.path.join(DATA_DIR, 'headers.pkl')

def dump_headers():
    ''' 
    >>> variable_names['bio1']
    'annual mean temperature'
    '''
    headers = [filename for filename in os.listdir(DATA_DIR)
                        if filename.endswith('.hdr')]
    
    variable_names = {}
    metadata = {}
    for header in headers:
        name = header[:-len('.hdr')]
        with open(os.path.join(DATA_DIR, header)) as header_file:
            for line in header_file:
                line = line.strip().lower()
                if not line: continue

                key, value = line.split()[0], ' '.join(line.split()[1:])
                if key == 'variable':
                    value = value.split(' = ')[1]
                    variable_names[name] = value
                if key == 'nodata':
                    try:
                        value = float(value)
                    except ValueError: pass
                if not name in metadata:
                    metadata[name] = {}
                metadata[name][key] = value


    with open(pkl_path, 'w') as dump_file:
        pkl.dump((variable_names, metadata), dump_file, -1)


if not os.path.exists(pkl_path): dump_headers()
with open(pkl_path) as pkl_file:
    variable_names, metadata = pkl.load(pkl_file)