import os

PITCHES = {'A':0, 'A#':1, 'B-':1, 'B':2, 'C-':2, 'B#':3, 'C':3, 'C#':4, 'D-':4, 'D':5, 'D#':6, 'E-':6, 'E':7, 'E#':8, 'F':8, 'F#':9, 'G-':9, 'G':10, 'G#':11, 'A-':11}
KEYDICT = {677:(0,'A'), 1354:(1,'A#/B-'), 2708:(2,'B'), 1321:(3,'C'), 2642:(4,'C#/D-'), 1189:(5,'D'), 2378:(6,'D#/E-'), 661:(7,'E'), 1322:(8,'F'), 2644:(9,'F#/G-'), 
           1193:(10,'G'), 2386:(11,'G#/A-')}

# Initialize key counter
COUNT = [0 for i in range(12)]
TOTAL = 0

# Get the key signature of each .krn file
for file in os.listdir("../MusicFiles/HanMusic"):
    # Open each file and read it as a list of strings (one sting per line)
    f = open("../MusicFiles/HanMusic/" + file, 'r')
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
    ID = 0
    for p in pitches:
        ID += 2**PITCHES[p]
    if ID not in KEYDICT:
        os.rename('../MusicFiles/HanMusic/' + file, '../MusicFiles/RemovedMusic/HanIrregular/' + file)
    else:
        # Lookup key based on ID number
        key = KEYDICT[ID]
        # Add to count
        COUNT[key[0]] += 1.0
        TOTAL += 1.0
    
# Output results
print TOTAL
print COUNT
for i in range(12):
    COUNT[i] = round(COUNT[i]/TOTAL * 100, 1)
print COUNT
