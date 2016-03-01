import os

PITCHES = {'A':0, 'A#':1, 'B-':1, 'B':2, 'C-':2, 'B#':3, 'C':3, 'C#':4, 'D-':4, 'D':5, 'D#':6, 'E-':6, 'E':7, 'E#':8, 'F':8, 'F#':9, 'G-':9, 'G':10, 'G#':11, 'A-':11}
KEYDICT = {677:(0,'A'), 1354:(1,'A#/B-'), 2708:(2,'B'), 1321:(3,'C'), 2642:(4,'C#/D-'), 1189:(5,'D'), 2378:(6,'D#/E-'), 661:(7,'E'), 1322:(8,'F'), 2644:(9,'F#/G-'), 
           1193:(10,'G'), 2386:(11,'G#/A-')}

datafile = open('../FullSongData/HanSet.txt', 'w')

# Get the key signature of each .krn file
for file in os.listdir("../MusicFiles/HanMusic"):
    # Open each file and read it as a list of strings (one sting per line)
    f = open("../MusicFiles/HanMusic/" + file, 'r')
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
    
    datafile.write(DATA[0]+','+str(DATA[1][0])+','+str(DATA[1][1])+','+DATA[2])
    datafile.write('\n')