import os

PITCHES = {'A':0, 'A#':1, 'B-':1, 'B':2, 'C-':2, 'B#':3, 'C':3, 'C#':4, 'D-':4, 'D':5, 'D#':6, 'E-':6, 'E':7, 'E#':8, 'F':8, 'F#':9, 'G-':9, 'G':10, 'G#':11, 'A-':11}
KEYDICT = {1453:(0,'C','a'), 1709:(1,'G','e'), 1717:(2,'D','b'), 2741:(3,'A','f#'), 2773:(4,'E','c#'), 2774:(5,'B','g#'), 2902:(6,'G-','e-'), 2906:(7,'D-','B-'), 
           3418:(8,'A-','f'), 3434:(9,'E-','c'), 1387:(10,'B-','g'), 1451:(11,'F','d')}

# Initialize key counter
COUNT = [0 for i in range(12)]
TOTAL = 0

# Get the key signature of each .krn file
for file in os.listdir("../MusicFiles/GermanMusic"):
    # Open each file and read it as a list of strings (one sting per line)
    f = open("../MusicFiles/GermanMusic/" + file, 'r')
    text = f.readlines()
    f.close
    f = None
    
    for i in range(len(text)):
        if text[i].startswith('{'):
            start = i
            break
    for i in range(len(text)):
        if text[i].startswith('=='):
            end = i
            break
    
    text = text[start:end]
    
    for i in range(len(text)):
        text[i] = text[i].replace('}', '')
        text[i] = text[i].replace(']', '')
        text[i] = text[i].replace('\n', '')
    
    # Track all pitches used in the song
    pitches = []
    first = None
    for i in range(len(text)):
        if text[i].startswith('=') or text[i].startswith('*') or text[i].startswith('!'):
            pass
        elif text[i].endswith('-') or text[i].endswith('#'):
            pitch = text[i][-2:]
        elif text[i].endswith('n') or text[i][-1].isdigit():
            pitch = text[i][-2]
        else:
            pitch = text[i][-1]

        pitch = pitch.upper()
        if i == 0:
            first = pitch
        if pitch not in pitches and pitch != 'R':
            pitches.append(pitch)
    
    pitches.sort()
    
    # Convert pitch set into an ID number, by treating it as a 12-digit binary number
    id = 0
    for p in pitches:
        id += 2**PITCHES[p]
    if id not in KEYDICT:
        os.rename('../GermanMusic/' + file, '../RemovedMusic/GermanRemoved/GermanNonDiatonic/' + file)
        print file
        print pitches
    else:
        # Lookup key based on ID number
        key = KEYDICT[id]
        # Add to count
        COUNT[key[0]] += 1.0
        TOTAL += 1.0

# Output results
print TOTAL
print COUNT
for i in range(12):
    COUNT[i] = round(COUNT[i]/TOTAL * 100, 1)
print COUNT



'''==========================================================================================
#OLD CODE
    # Remove files with wrong number of pitches
    if len(pitches) > 7:
        os.rename('GermanMusic/' + file, 'GermanHigh/' + file)
    elif len(pitches) < 7:
        os.rename('GermanMusic/' + file, 'GermanLow/' + file)
    else:
        good +=1
             
    print good
    print low
    print high
     
    
    # Key lookup
    # Find key signature
    for line in text:
        if line.startswith('*k['):
            key = line
            break
    
    # Extract notes from key signature        
    key = key[3:-2]
    
    # Determine key
    num = len(key)/2
    if num == 0:
        flat = 0
    elif key[1] == '-':
        flat = 1
    elif key[1] == '#':
        flat = 0
    else:
        print 'KEY SIGNATURE ERROR DETECTED'
    
    
    
    # Remove nondiatonic scales
    if flat != 0 and sharp != 0:
        os.rename('GermanMusic/' + file, 'GermanNonDiatonic/' + file)
    
    # Count flats and sharps    
    flat = 0
    sharp = 0
    for pitch in pitches:
        flat += pitch.count('-')
        sharp += pitch.count('#')
      
    if flat != 0:
        num = flat
        isflat = 1
    else:
        num = sharp
        isflat = 0
         
    # Lookup key in matrix
    key = KEYS[num][isflat]
    
    # Generate matrix of keys
KEYS = [[None for i in range(2)] for i in range(7)]

# Each row corresponds to the number of sharps or flats; Column 0 has flats, column 1 has sharps
KEYS[0][0] = [0, 'C', 'a']
KEYS[1][0] = [1, 'G', 'e']
KEYS[2][0] = [2, 'D', 'b']
KEYS[3][0] = [3, 'A', 'f#']
KEYS[4][0] = [4, 'E', 'c#']
KEYS[5][0] = [5, 'B', 'g#']
KEYS[6][0] = [6, 'F#', 'd#']
KEYS[0][1] = [0, 'C', 'a']
KEYS[1][1] = [11, 'F', 'd']
KEYS[2][1] = [10, 'B-', 'g']
KEYS[3][1] = [9, 'E-', 'c']
KEYS[4][1] = [8, 'A-', 'f']
KEYS[5][1] = [7, 'D-', 'b-']
KEYS[6][1] = [6, 'G-', 'e-']
    '''