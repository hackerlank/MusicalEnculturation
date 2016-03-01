import os

PITCHES = {'A':0, 'A#':1, 'B-':1, 'B':2, 'C-':2, 'B#':3, 'C':3, 'C#':4, 'D-':4, 'D':5, 'D#':6, 'E-':6, 'E':7, 'E#':8, 'F':8, 'F#':9, 'G-':9, 'G':10, 'G#':11, 'A-':11}
KEYDICT = {1453:(0,'C','a'), 1709:(1,'G','e'), 1717:(2,'D','b'), 2741:(3,'A','f#'), 2773:(4,'E','c#'), 2774:(5,'B','g#'), 2902:(6,'G-','e-'), 2906:(7,'D-','b-'), 
           3418:(8,'A-','f'), 3434:(9,'E-','c'), 1387:(10,'B-','g'), 1451:(11,'F','d')}

# Dictionary of which pitches are the most stable in the each relative major and minor key pairing [tonic, subdominant, dominant]
STABLE = {0:(['C','F','G'],['A','D','E']), 1:(['G','C','D'],['E','A','B']), 2:(['D','G','A'],['B','E','F#']), 3:(['A','D','E'],['F#','B','C#']), 
          4:(['E','A','B'],['C#','F#','G#']), 5:(['B','E','F#'],['G#','C#','D#']), 6:(['G-','C-','D-'],['E-','A-','B-']), 7:(['D-','G-','A-'],['B-','E-','F']), 
          8:(['A-','D-','E-'],['F','B-','C']), 9:(['E-','A-','B-'],['C','F','G']), 10:(['B-','E-','F'],['G','C','D']), 11:(['F','B-','C'],['D','G','A'])}

datafile = open('../FullSongData/GermanSet.txt', 'w')

maj = 0
min = 0
oddend = 0

KEYCOUNT = [0 for i in range(24)]

# Get the key signature of each .krn file
for file in os.listdir("../MusicFiles/GermanMusic"):
    # Open each file and read it as a list of strings (one sting per line)
    f = open("../MusicFiles/GermanMusic/" + file, 'r')
    text = f.readlines()
    f.close
    f = None
    
    DATA = [file, None, ''] # DATA holds [filename, key, transcription]
    
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
            if text[i][-3] == text[i][-2]: # if a double note, duplicate the sharp or flat
                text[i] = text[i][:-2] + text[i][-1] + text[i][-2:]
            DATA[2] += text[i].upper()
            pitch = text[i][-2:]
        elif text[i].endswith('n') or text[i][-1].isdigit():
            DATA[2] += text[i].upper()
            pitch = text[i][-2]
        else:
            DATA[2] += text[i].upper()
            pitch = text[i][-1]

        pitch = pitch.upper()
        
        
        if pitch not in pitches and pitch != 'R':
            pitches.append(pitch)
    
    pitches.sort()
    
    # Convert pitch set into an ID number, by treating it as a 12-digit binary number
    id = 0
    for p in pitches:
        id += 2**PITCHES[p]
    if id not in KEYDICT:
        print file
        print 'IRREGULAR KEY DETECTED'
    else:
        # Lookup key based on ID number
        key = KEYDICT[id]
        DATA[1] = key
    
    permitted = ['A','B','C','D','E','F','G','#','-']
    cleaned = ''
    for char in DATA[2]:
        if char in permitted:
            cleaned += char
    DATA[2] = cleaned
    if DATA[2].endswith('#') or DATA[2].endswith('-'):
        final = DATA[2][-2:]
    else:
        final = DATA[2][-1]
    
    # Determine whether key is major or minor by checking the key for which the final pitch is the tonic, subdominant, or dominant
    stable = STABLE[DATA[1][0]]
    finID = PITCHES[final]
    if finID == PITCHES[stable[0][0]] or finID == PITCHES[stable[0][1]] or finID == PITCHES[stable[0][2]]:
        major = True
        maj += 1
    elif finID == PITCHES[stable[1][0]] or finID == PITCHES[stable[1][1]] or finID == PITCHES[stable[1][2]]:
        major = False
        min += 1
    else:
        major = True
        print DATA[0]
        oddend += 1
    
    if major == True:
        DATA[1] = (DATA[1][0], DATA[1][1])
    else:
        DATA[1] = (DATA[1][0] + 12, DATA[1][2])
    
    KEYCOUNT[DATA[1][0]] += 1
    
    datafile.write(DATA[0]+','+str(DATA[1][0])+','+str(DATA[1][1])+','+DATA[2])
    datafile.write('\n')

print 'Major: ' + str(maj)
print 'Minor: ' + str(min)
print 'Unknown: ' + str(oddend)
print KEYCOUNT