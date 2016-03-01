import csv

def parseFile(readFile, writeFile):
    # USE FIRST PITCH SET FOR GERMAN & CHINESE, SECOND FOR HINDUSTANI
    #PITCHES = {'A':0, 'A#':1, 'B-':1, 'B':2, 'C-':2, 'B#':3, 'C':3, 'C#':4, 'D-':4, 'D':5, 'D#':6, 'E-':6, 'E':7, 'E#':8, 'F':8, 'F#':9, 'G-':9, 'G':10, 'G#':11, 'A-':11}
    PITCHES = {'D':0, 'N-':1, 'N':2, 'S':3, 'R-':4, 'R':5, 'G-':6, 'G':7, 'M':8, 'M-':9, 'P':10, 'D-':11}
    
    rf = open(readFile, 'r')
    wf = open(writeFile, 'w')
    
    songs = csv.reader(rf)
    
    output = ''
    for song in songs:
        notes = []
        melody = song[3] # CHANGE TO 2 FOR HINDUSTANI
        i = len(melody) - 1
        while i >= 0: #iterate from end of song to beginning of song
            if melody[i] == '#' or melody[i] == '-':
                token = melody[i-1:i+1]
                i -= 2
            else:
                token = melody[i]
                i -= 1
            notes = [PITCHES[token]] + notes
        output += song[0] + '\t' + song[1] + '\t' + str(notes) + '\n'
    
    wf.write(output)
    
parseFile('../FullSongData/HindustaniSet.txt', '../FullSongData/HindustaniTrials.txt')