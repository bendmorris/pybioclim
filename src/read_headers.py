''' 
>>> variable_names['bio1']
'annual mean temperature'
'''
import os
from config import DATA_PATHS, find_data


variable_names = {}
metadata = {}

def read_header(name):
    header_path = find_data(name + '.hdr')
    with open(header_path) as header_file:
        for line in header_file:
            line = line.strip().lower()
            if not line: continue
            
            key, value = line.split()[0], ' '.join(line.split()[1:])
            if key == 'variable':
                if ' = ' in value:
                    value = value.split(' = ')[1]
                variable_names[name] = value
            if key == 'nodata':
                try:
                    value = float(value)
                except ValueError: pass
            if not name in metadata:
                metadata[name] = {}
            
            metadata[name][key] = value

for data_dir in DATA_PATHS:
    headers = [filename for filename in os.listdir(data_dir)
                        if filename.endswith('.hdr')]

    for header in headers:
        name = header[:-len('.hdr')]
        if not name in metadata:
            read_header(name)

