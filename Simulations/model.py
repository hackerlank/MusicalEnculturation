import scipy
import json
from random import random, shuffle, choice, sample
from math import exp, log
from scipy.spatial.distance import euclidean
from copy import deepcopy

class SOM:

    def __init__(self, height=10, width=10, FV_size=10, learning_rate=0.005, systems='W', mode ='M', nodes=[]):
        self.height = height
        self.width = width
        self.FV_size = FV_size
        self.systems = systems
        self.mode = mode
        self.radius = (height+width)/2 # Originally /3
        self.learning_rate = learning_rate
        if nodes==[]:
            self.nodes = scipy.array([[[random()*(choice(range(0,3,2))-1) for i in range(FV_size)] for x in range(width)] for y in range(height)])
        else:
            self.nodes = nodes
        self.fixedR = False
        self.fixedLR = False
        self.log = {'final':{}, 'scores':{}, 'states':[]}
        

    def train(self, iterations=1000, full_data=[[]], log_file='../LogFiles/default_log.json'):
        print 'INITIAL SCORE: '
        self.score()
        self.update_log()
        
        # Generate matrix to store changes to connection weights
        delta_nodes = scipy.array([[[0. for i in range(self.FV_size)] for x in range(self.width)] for y in range(self.height)])
        if self.radius != 1.:
            time_constant = iterations/log(self.radius)
        else:
            time_constant = iterations/log(1.0001) # Avoids divide by zero errors
            
        for i in range(1, iterations+1):
            print "\rTRAINING ITERATION: " + str(i) + "/" + str(iterations)
            training_data = []
            if len(self.systems) == 1 or self.mode == 'K':
                training_data = full_data[0]
            elif len(self.systems) > 1 and self.mode == 'M':
                for j in range(len(self.systems)):
                    '''randomly sample songs from each system's database during each iteration'''
                    training_data += sample(full_data[j], len(full_data[j])/len(self.systems))
                    
            # Shuffle the ordering of songs at the beginning of each iteration
            shuffle(training_data)
            
            # Update learning rate and neighborhood radius for current iteration
            if self.fixedR:
                radius = self.radius
            else:
                radius = self.radius*exp(-1.0*i**1.1/time_constant)
                if radius <= 1.:
                    radius = 1.0
            rad_div_val = 2 * radius * i
            if self.fixedLR:
                learning_rate = self.learning_rate
            else:
                learning_rate = self.learning_rate*exp(-1.0*i**1.25/time_constant)
                if learning_rate < self.learning_rate/100.:
                    learning_rate = self.learning_rate/100.
            print '\nRadius: ', radius
            print 'Learning rate: ', learning_rate
            #delta_nodes.fill(0.)
            # Train all data from a song before moving on to the next song
            for song in training_data:
                train_vector = song
                # Clear weight adjustments before each song
                delta_nodes.fill(0.)
                
                for t in range(len(train_vector)):
                    train_vector[t] = scipy.array(train_vector[t])
                
                for j in range(len(train_vector)):
                    #delta_nodes.fill(0.) # Clear weight adjustments before each token
                    
                    # Find the node with the highest activation level
                    best = self.best_match(train_vector[j])
                    
                    # Update the weights for all nodes in the neighborhood of the winning node
                    for loc in self.find_neighborhood(best, radius):
                        influence = exp( (-1.0 * (loc[2]**2)) / rad_div_val)
                        inf_lrd = influence*learning_rate
                        delta_nodes[loc[0],loc[1]] += inf_lrd * train_vector[j] # Hebbian learning
                
                # Only update weights after a song ends
                self.nodes += delta_nodes
                # Ensure that weights never exceed 1 or -1
                high_value_indices = self.nodes > 1.0
                low_value_indices = self.nodes < -1.0
                self.nodes[high_value_indices] = 1.0
                self.nodes[low_value_indices] = -1.0
            
            # Score the accuracy of the model after each iteration    
            self.score() # Calculate and print scores after each iteration
            self.update_log()
        for sys in self.systems:
            self.log['final'][sys] = self.log['scores'][sys][-1]   
        self.save_log(log_file)
        
        
    # Returns a list of points which live within 'dist' of 'pt'
    # Uses the Chessboard distance
    # pt is (row, column)
    def find_neighborhood(self, pt, dist):
        min_y = max(int(pt[0] - dist), 0)
        max_y = min(int(pt[0] + dist), self.height)
        min_x = max(int(pt[1] - dist), 0)
        max_x = min(int(pt[1] + dist), self.width)
        neighbors = []
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                dist = abs(y-pt[0]) + abs(x-pt[1])
                neighbors.append((y,x,dist))
        return neighbors

    # Returns location of greatest activation
    def best_match(self, inputs):
        return scipy.unravel_index(scipy.argmax(scipy.multiply(self.nodes, inputs).sum(axis=2)), (self.height,self.width))

    def score(self):
        for sys in 'WCH':
            if sys not in self.log['scores']:
                self.log['scores'][sys] = []
            
            keynames = []
            keys = []
            
            #WESTERN KEYS
            if sys == 'W':
                #print '\nWESTERN SCORES:'
                keynames = ['C','G','D','A','E','A-','E-','B-','F']
                keys = [[1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0], [1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0], [1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0], [1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0], [1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0], [-1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0], [-1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0], [1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0], [1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0]]
    
            #CHINESE KEYS
            if sys == 'C':
                #print '\nCHINESE SCORES:'
                keynames = ['A*','A#*','B*','C*','D*','D#*','E*','F*','G*']
                keys = [[1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0], [-1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0], [-1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0], [1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0], [1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0], [-1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0], [1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0], [-1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0], [1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0]]
            
            #HINDUSTANI KEYS
            if sys == 'H':
                #print '\nHINDUSTANI SCORES:'
                keynames = ['Bilaval','Khamaj','Kafi','Asavari','Bhairavi','Kalyan','Todi','Purvi','Marva','Bhairav']
                keys = [[1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0], [1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0], [1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0], [-1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0], [-1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0], [1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0], [-1.0, -1.0, 1.0, 1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0], [-1.0, -1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0, 1.0], [1.0, -1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0], [-1.0, -1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0]]
    
            total_pitches = float(self.FV_size*len(keys))
            accurate9 = [[None for i in range(self.FV_size)] for j in range(len(keys))]
            thresh_score9 = 0
            act_score = 0.
            distance = 0.
            for i in range(len(keys)):
                key = keys[i]
                r,c = self.best_match(key)
                accurate9[i] = (abs(scipy.array(key) - self.nodes[r][c]) <= .1)
                for item in accurate9[i]:
                    if item == True:
                        thresh_score9 += 1
                act_score += sum(self.nodes[r][c] * key)
                distance += euclidean(key, self.nodes[r][c])
            thresh_score9 = round(thresh_score9/total_pitches*100,3)
            act_score = round(act_score/total_pitches*100,3)
            distance = distance/len(keys)
            self.log['scores'][sys].append((thresh_score9, act_score, distance))
            #print 'Threshold Score (.9): ', thresh_score9
            #print 'Activation Score: ', act_score
            #print 'Avg Euclidean Distance: ', distance

    def update_log(self):
        self.log['states'].append(deepcopy(self.nodes).tolist())
    
    def save_log(self, log_file):
        with open(log_file, 'w') as f:
            json.dump(self.log, f)
    
    def set_nodes(self,nodes):
        self.nodes = nodes
        
        