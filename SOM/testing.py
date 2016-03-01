from random import *
from math import *
import sys
import scipy
from numpy import Inf
'''
nodes = scipy.array([[[random() for i in range(12)] for x in range(8)] for y in range(9)])
inputs = [1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0]
'''
'''
print nodes
print '\n'
print scipy.multiply(nodes, inputs)
print '\n'
'''
'''
print scipy.multiply(nodes, inputs).sum(axis=2)
print '\n'
loc = scipy.argmax(scipy.multiply(nodes, inputs).sum(axis=2))
r = 0
while loc >= 8:
    loc -= 8
    r += 1
c = loc
print (r,c)
print scipy.unravel_index(scipy.argmax(scipy.multiply(nodes, inputs).sum(axis=2)), (9,8))
'''
'''
for i in range(100):
    print random()*(choice(range(0,3,2))-1)
'''
'''
x=scipy.array([[-2, 3, .5, -.4], [1, 3, -6, .2]])
high_value_indices = x > 1.0
low_value_indices = x < -1.0
print high_value_indices
print low_value_indices
x[high_value_indices] = 1.0
x[low_value_indices] = -1.0
print x
'''
'''
radius = 10
iterations = 1000
time_constant = iterations/log(radius)
#time_constant = iterations/sqrt(radius)
#time_constant = iterations/radius
for i in range(iterations):
    print exp(-1.0*i/time_constant), exp(-1.0*i**1.25/time_constant), exp((-1.*i/time_constant)-i/100)
'''
map = {'A':0, 'A#':1, 'B-':1, 'B':2, 'C-':2, 'B#':3, 'C':3, 'C#':4, 'D-':4, 'D':5, 'D#':6, 'E-':6, 'E':7, 'E#':8, 'F':8, 'F#':9, 'G-':9, 'G':10, 'G#':11, 'A-':11}
print {v: k for k, v in map.items()}