import csv
import ast
from copy import deepcopy

class STM:
    def __init__(self, num_pitches=12): # num_pitches is the number of unique pitch classes in the system in question
        self.span = [0. for i in range(num_pitches)]
        self.back = [0 for i in range(num_pitches)]
        self.length = num_pitches
    '''
    def read(self, pitch):
        for i in range(len(self.span)):
            if self.span[i] != -1.0:
                #self.span[i] = round(self.span[i]-.1, 1)
                self.back[i] += 1
                if self.back[i] > 7:
                    self.span[i] = -1.0
        self.span[int(pitch)] = 1.0
        self.back[int(pitch)] = 1
    '''
    def read(self, pitch):
        for i in range(len(self.span)):
            if self.span[i] != -1.0:
                self.span[i] = round(self.span[i]-.125, 3)
        self.span[int(pitch)] = 1.0
    
    def clear(self):
        self.span = [0. for i in range(self.length)]
    
    def __repr__(self):
        return str(self.span)


#rf = open('../ReducedSongData/GermanReduced.txt', 'r')
#wf = open('../TrainingData/German.txt', 'w')

#rf = open('../ReducedSongData/HanReduced.txt', 'r')
#wf = open('../TrainingData/Han.txt', 'w')

rf = open('../ReducedSongData/HindustaniReduced.txt', 'r')
wf = open('../TrainingData/Hindustani.txt', 'w')

data = csv.reader(rf, delimiter='\t')
output = []

reader = STM()

for row in data:
    reader.clear()
    song = ast.literal_eval(row[2])
    song_output = []
    for i in range(len(song)):
        reader.read(song[i])
        song_output.append(deepcopy(reader.span))
    output.append(song_output[7:])
    
wf.write(str(output))
        
