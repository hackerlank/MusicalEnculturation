import csv
from random import shuffle

def trial_reduce(readFile, writeFile, quant):
    rf = open(readFile, 'r')
    wf = open(writeFile, 'w')
    
    songs = csv.reader(rf, delimiter='\t')
    
    song_list = []
    for song in songs:
        song_list.append(song)
        
    shuffle(song_list)
    
    output = ''
    for song in song_list:
        key = int(song[1])
        if key < len(quant) and quant[key] != 0:
            output += song[0] + '\t' + song[1] + '\t' + str(song[2]) + '\n'
            quant[key] -= 1
    
    for key in quant:
        if key != 0:
            print 'One of more key quantities were not fulfilled!'
            
    wf.write(output)
    
    
    
trial_reduce('../FullSongData/GermanTrials.txt', '../ReducedSongData/GermanReduced.txt', [10, 15, 5, 5, 4, 0, 0, 0, 4, 4, 6, 13])
#trial_reduce('../FullSongData/HanTrials.txt', '../ReducedSongData/HanReduced.txt', [8, 3, 4, 9, 0, 12, 3, 8, 8, 0, 11, 0])