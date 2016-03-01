from sims import *
from model import SOM
from os import rename, listdir

def main():
    '''CONTROL PANEL'''
    MODE = 'M' # 'K' to train on musical keys, 'M' to train on music datasets
    SYSTEMS = 'H' # Include 'W' for Western system, 'C' for Chinese system, 'H' for Hindustani system
    MODE2 = 'M'
    SYSTEMS2 ='HC'
    width = 30
    height = 30
    iterations = 100
    learning_rate = .25
    pitch_count = 12
    '''================'''
    
    # Generate model
    #print "Generating map..."
    #som = SOM(width, height, pitch_count, learning_rate, SYSTEMS, MODE)
    #genTest(som, iterations, MODE, SYSTEMS)
    
    #sim1(SYSTEMS)
    #sim2(SYSTEMS)
    sim3(MODE, MODE2, SYSTEMS, SYSTEMS2)
    
    
    
    
main()