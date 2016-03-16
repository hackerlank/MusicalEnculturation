import scipy

def output_results(som, keynames, keys):
    print '\nRESULTS:'
    find_learned_keys(som, keynames, keys)
    map_keys(som, keynames, keys)
    
def find_learned_keys(som, keynames, keys):
    print 'KEYS LEARNED:'
    pitches = {0: 'A', 1: 'A#', 2: 'B', 3: 'C', 4: 'C#', 5: 'D', 6: 'D#', 7: 'E', 8: 'F', 9: 'F#', 10: 'G', 11: 'G#'}
    keylist = []
    for row in som.nodes:
        for node in row:
            is_key = True
            key = []
            for i in range(len(node)):
                if node[i] >= .9:
                    key += [pitches[i]]
                elif node[i] > -.9:
                    is_key = False
            if is_key and key not in keylist:
                keylist += [key]
    keylist.sort()
    for key in keylist:
        print key

def map_keys(som, keynames, keys):
    print '\nCHECKING LEARNING AND MAPPING KEYS:'
    mapping = [['' for i in range(som.width)] for j in range(som.height)]
    accurate = [[None for i in range(som.FV_size)] for j in range(len(keys))]
    locations = {}
    for i in range(len(keys)):
        keyname = keynames[i]
        key = keys[i]
        r,c = som.best_match(key)
        locations[keyname] = (r, c)
        mapping[r][c] += keyname
        accurate[i] = (abs(scipy.array(key) - som.nodes[r][c]) <= .1)
        print keyname, ': ', som.nodes[r][c]
        print accurate[i]
    for row in mapping:
        print row
    return locations
    