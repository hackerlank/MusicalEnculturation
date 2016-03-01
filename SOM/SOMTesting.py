import Model as model
import ast
import scipy
from copy import deepcopy


'''CONTROL PANEL'''
MODE = 'KEYS' # 'KEYS' to train on musical keys, 'MUSIC' to train on music datasets
SYSTEMS = 'WHC' # Include 'W' for Western system, 'C' for Chinese system, 'H' for Hindustani system
width = 15
height = 15
iterations = 1000
learning_rate = .25
pitch_count = 12


'''MODEL PREPARATION AND TRAINING'''
# Prepare set of keys and key names for the current simulation
keynames = []
keys = []
#WESTERN KEYS
if 'W' in SYSTEMS:
    #keynames += ['C','G','D','A','E','B','G-','D-','A-','E-','B-','F']
    #keys += [[1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0], [1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0], [1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0], [1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0], [1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0], [-1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0], [-1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0], [-1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0], [-1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0], [-1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0], [1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0], [1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0]]
    keynames += ['C','G','D','A','E','A-','E-','B-','F']
    keys += [[1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0], [1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0], [1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0], [1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0], [1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0], [-1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0], [-1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0], [1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0], [1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0]]

#CHINESE KEYS
if 'C' in SYSTEMS:
    #keynames += ['A*','A#*','B*','C*','C#*','D*','D#*','E*','F*','F#*','G*','G#*']
    #keys += [[1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0], [-1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0], [-1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0], [1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0], [-1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0], [1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0], [-1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0], [1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0], [-1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0], [-1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0], [1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0], [-1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0]]
    keynames += ['A*','A#*','B*','C*','D*','D#*','E*','F*','G*']
    keys += [[1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0], [-1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0], [-1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0], [1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0], [1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0], [-1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0], [1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0], [-1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0], [1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0]]

#HINDUSTANI KEYS
if 'H' in SYSTEMS:
    keynames += ['Bilaval','Khamaj','Kafi','Asavari','Bhairavi','Kalyan','Todi','Purvi','Marva','Bhairav']
    keys += [[1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0], [1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0], [1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0], [-1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0], [-1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0], [1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0], [-1.0, -1.0, 1.0, 1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0], [-1.0, -1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0, 1.0], [1.0, -1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0], [-1.0, -1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0]]

# Prepare dataset based on MODE and SYSTEMS parameters
data = []
if MODE == 'KEYS':
    data = deepcopy(keys)
    for i in range(len(data)):
        data[i] = [data[i]]
elif MODE == 'MUSIC':
    if 'W' in SYSTEMS:
        f = open('../TrainingData/German.txt')
        data += ast.literal_eval(f.read())
    if 'C' in SYSTEMS:
        f = open('../TrainingData/Han.txt')
        data += ast.literal_eval(f.read())
    if 'H' in SYSTEMS:
        f = open('../TrainingData/Hindustani.txt')
        data += ast.literal_eval(f.read())

# Generate model
print "Generating map..."
key_som = model.SOM(width,height,pitch_count,learning_rate, SYSTEMS)

# Train model
print "Training model..."
key_som.train(iterations, data)


'''OUTPUT RESULTS'''
mapping = [['' for i in range(width)] for j in range(height)]
accurate = [[None for i in range(12)] for j in range(len(keys))]
for i in range(len(keys)):
    keyname = keynames[i]
    key = keys[i]
    r,c = key_som.best_match(key)
    mapping[r][c] += keyname
    accurate[i] = (abs(scipy.array(key) - key_som.nodes[r][c]) <= .1)
    #print keyname, ': ', key_som.nodes[r][c]
    #print accurate[i]
for row in mapping:
    print row

    
    
    
    
'''OLD CODE'''    
'''
x = 0
while x < 10:
    x += 1
    print 'REPETITION: ', x
    fin = key_som.train(1000, data)
    print fin

    mapping = [['' for i in range(width)] for j in range(height)]
    for i in range(len(keys)):
        keyname = keynames[i]
        key = keys[i]
        r,c = key_som.best_match(key)
        mapping[r][c] += keyname
        print keyname, ': ', key_som.nodes[r][c]
    for row in mapping:
        print row
'''
'''
PITCHES = {'A':0, 'A#':1, 'B-':1, 'B':2, 'C-':2, 'B#':3, 'C':3, 'C#':4, 'D-':4, 'D':5, 'D#':6, 'E-':6, 'E':7, 'E#':8, 'F':8, 'F#':9, 'G-':9, 'G':10, 'G#':11, 'A-':11}
STABLE = {0:(['C','F','G'],['A','D','E']), 1:(['G','C','D'],['E','A','B']), 2:(['D','G','A'],['B','E','F#']), 3:(['A','D','E'],['F#','B','C#']), 
          4:(['E','A','B'],['C#','F#','G#']), 5:(['B','E','F#'],['G#','C#','D#']), 6:(['G-','C-','D-'],['E-','A-','B-']), 7:(['D-','G-','A-'],['B-','E-','F']), 
          8:(['A-','D-','E-'],['F','B-','C']), 9:(['E-','A-','B-'],['C','F','G']), 10:(['B-','E-','F'],['G','C','D']), 11:(['F','B-','C'],['D','G','A'])}
for i in range(len(keys)):
    stable = STABLE[i]
    pitch = stable[0][0]
    id = PITCHES[pitch]
    keys[i][id] = 1.0
    pitch = stable[0][1]
    id = PITCHES[pitch]
    keys[i][id] = .75
    pitch = stable[0][2]
    id = PITCHES[pitch]
    keys[i][id] = .5
'''