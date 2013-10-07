import os
import cPickle as pkl


pkl_path = 'data/headers.pkl'

def dump_headers():
    headers = [filename for filename in os.listdir('data')
                        if filename.endswith('.hdr')]

    variable_names = {}
    for header in headers:
        with open(os.path.join('data', header)) as header_file:
            for line in header_file:
                line = line.strip().lower()
                if not line: continue

                key, value = line.split()[0], ' '.join(line.split()[1:])
                if key == 'variable':
                    variable_names[header] = value


    with open(pkl_path, 'w') as dump_file:
        pkl.dump(variable_names, dump_file, -1)


if __name__ == '__main__':
    dump_headers()
else:
    if not os.path.exists(pkl_path): dump_headers()
    with open(pkl_path) as pkl_file:
        variable_names = pkl.load(pkl_file)