from __future__ import division

## Kyle Dickerson
## kyle.dickerson@gmail.com
## Jan 15, 2008
##
## Self-organizing map using scipy
## This code is licensed and released under the GNU GPL

## This code uses a square grid rather than hexagonal grid, as scipy allows for fast square grid computation.
## I designed sompy for speed, so attempting to read the code may not be very intuitive.
## If you're trying to learn how SOMs work, I would suggest starting with Paras Chopras SOMPython code:
##  http://www.paraschopra.com/sourcecode/SOM/index.php
## It has a more intuitive structure for those unfamiliar with scipy, however it is much slower.

## If you do use this code for something, please let me know, I'd like to know if has been useful to anyone.

from random import *
from math import *
import sys
import scipy

class SOM:

    def __init__(self, height=10, width=10, FV_size=10, learning_rate=0.005):
        self.height = height
        self.width = width
        self.FV_size = FV_size
        self.radius = (height+width)/3
        self.learning_rate = learning_rate
        self.nodes = scipy.array([[[random() for i in range(FV_size)] for x in range(width)] for y in range(height)])

    # train_vector: [ FV0, FV1, FV2, ...] -> [ [...], [...], [...], ...]
    # train vector may be a list, will be converted to a list of scipy arrays
    def train(self, iterations=1000, train_vector=[[]]):
        for t in range(len(train_vector)):
            train_vector[t] = scipy.array(train_vector[t])
        time_constant = iterations/log(self.radius)
        delta_nodes = scipy.array([[[0.0 for i in range(self.FV_size)] for x in range(self.width)] for y in range(self.height)])
        
        for i in range(1, iterations+1):
            shuffle(train_vector)
            radius_decaying=self.radius*exp(-1.0*i/time_constant)
            rad_div_val = 2 * radius_decaying * i
            learning_rate_decaying=self.learning_rate*exp(-1.0*i/time_constant)
            sys.stdout.write("\rTraining Iteration: " + str(i) + "/" + str(iterations))
            
            for j in range(len(train_vector)):
                delta_nodes.fill(0)
                best = self.best_match(train_vector[j])
                #print best
                for loc in self.find_neighborhood(best, radius_decaying):
                    influence = exp( (-1.0 * (loc[2]**2)) / rad_div_val)
                    inf_lrd = influence*learning_rate_decaying
                    
                    delta_nodes[loc[0],loc[1]] += inf_lrd*(train_vector[j]-self.nodes[loc[0],loc[1]])
                    #print delta_nodes
                self.nodes += delta_nodes
            
            if (i-1)%1000 == 0:
                #sys.stdout.write("\rChecking Learning for Iteration: " + str(i-1) + "     ")
                done = self.check_learned()
                if done:
                    return i-1 
            
        sys.stdout.write("\n")
    
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
    
    # Returns location of best match, uses Euclidean distance
    # target_FV is a scipy array
    def best_match(self, target_FV):
        loc = scipy.argmin((((self.nodes - target_FV)**2).sum(axis=2))**0.5)
        r = 0
        while loc >= self.width:
            loc -= self.width
            r += 1
        c = loc
        return (r, c)

    # returns the Euclidean distance between two Feature Vectors
    # FV_1, FV_2 are scipy arrays
    def FV_distance(self, FV_1, FV_2):
        return (sum((FV_1 - FV_2)**2))**0.5

    
    def check_learned(self):
        keynames = []
        keys = []
        learned = []
        
        #WESTERN KEYS
        keynames += ['C','G','D','A','E','B','G-','D-','A-','E-','B-','F']
        keys += [[1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0], [1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0], [1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0], [1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0], [1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0], [0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0], [0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0], [0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0], [0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0], [0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0], [1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0], [1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0]]
        learned += [True for i in range(12)]
        
        #CHINESE KEYS
        #keynames += ['A*','A#*','B*','C*','C#*','D*','D#*','E*','F*','F#*','G*','G#*']
        #keys += [[1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0], [0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0], [0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0], [1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0], [1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0], [1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0], [0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0], [0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0], [1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0]]
        #learned += [False for i in range(12)]
        
        #HINDUSTANI KEYS
        #keynames += ['Bilaval','Khamaj','Kafi','Asavari','Bhairavi','Kalyan','Todi','Purvi','Marva','Bhairav']
        #keys += [[1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0], [1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0], [1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0], [0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0], [1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0], [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0], [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0], [1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0], [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0]]
        #learned += [False for i in range(10)]
        
        for i in range(len(keys)):
            key = keys[i]
            r,c = self.best_match(key)
            vals = self.nodes[r][c]
            for j in range(len(key)):
                pitch = key[j]
                if pitch == 0.0:
                    if vals[j] > .1:
                        learned[i] = False
                elif pitch == 1.0:
                    if vals[j] < .5:
                        learned[i] = False
                else:
                    print "Incorrect pitch value detected in a key."
        #print learned
        if False in learned:
            return False
        else:
            return True
        