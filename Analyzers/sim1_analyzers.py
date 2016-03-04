import numpy as np
import os
import json
from json_loading import json_load_byteified as jlb
from matplotlib import pyplot

def avg_scores_sim1():
    print 'Starting...'
    score_log = {}
    for sys in 'WCH':
        total_scores = np.array([[0., 0., 0.] for i in range(101)])
        for file_name in os.listdir('../LogFiles/Sim1/' + sys):
            with open('../LogFiles/Sim1/' + sys + '/' + file_name, 'r') as f:
                data = jlb(f)
                print sys, file_name, data['scores'][sys][-1]
                scores = np.array(data['scores'][sys])
                total_scores += scores
        avg_scores = total_scores/10.
        score_log[sys] = (avg_scores).tolist()
    
    f = open('../LogFiles/Sim1/Extracted/Scores.json', 'w')
    json.dump(score_log, f)



def std_devs_sim1():
    print 'Starting...'
    dev_log = {}
    for sys in 'WCH':
        scores = np.empty((101,3,10))
        i = 0
        for file_name in os.listdir('../LogFiles/Sim1/' + sys):
            with open('../LogFiles/Sim1/' + sys + '/' + file_name, 'r') as f:
                data = jlb(f)
                scores[:,:,i] = np.array(data['scores'][sys])
            i += 1
        std_devs = np.empty((101,3))
        for x in range(101):
            for y in range(3):
                std_devs[x,y] = np.std(scores[x,y,:])
        dev_log[sys] = (std_devs).tolist()
    
    f = open('../LogFiles/Sim1/Extracted/Std_Devs.json', 'w')
    json.dump(dev_log, f)



def plot_scores_sim1(scores):
    W_scores = np.array(scores['W'])
    C_scores = np.array(scores['C'])
    H_scores = np.array(scores['H'])
    
    fig = pyplot.figure(figsize=(16,10))
    thresh = fig.add_subplot(211)
    act = fig.add_subplot(212)
    #dist = fig.add_subplot(313)
    
    thresh.set_title('% Correct Pitches')
    act.set_title('% Max Activation')
    #dist.set_title('Avg Euclidean Distance')
    
    x = range(101)
    
    linet1, = thresh.plot(x, W_scores[:,0], 'b', linewidth=2)
    linet2, = thresh.plot(x, C_scores[:,0], 'r', linewidth=2)
    linet3, = thresh.plot(x, H_scores[:,0], 'g', linewidth=2)
    
    linea1, = act.plot(x, W_scores[:,1], 'b', linewidth=2)
    linea2, = act.plot(x, C_scores[:,1], 'r', linewidth=2)
    linea3, = act.plot(x, H_scores[:,1], 'g', linewidth=2)
    
    #lined1, = dist.plot(x, W_scores[:,2], 'b', linewidth=2)
    #lined2, = dist.plot(x, C_scores[:,2], 'r', linewidth=2)
    #lined3, = dist.plot(x, H_scores[:,2], 'g', linewidth=2)
    
    thresh.set_ylim((0,100))
    act.set_ylim((0,100))
    
    pyplot.show()
        
        
        
def print_start_and_end_scores(scores, devs):
    W_scores = np.array(scores['W'])
    C_scores = np.array(scores['C'])
    H_scores = np.array(scores['H'])
    W_devs = np.array(devs['W'])
    C_devs = np.array(devs['C'])
    H_devs = np.array(devs['H'])
    
    print 'WESTERN SCORES:'
    print 'INITIAL\t\tFINAL'
    print W_scores[0,0], (W_devs[0,0]), '\t', W_scores[-1,0], (W_devs[-1,0])
    print W_scores[0,1], (W_devs[0,1]), '\t', W_scores[-1,1], (W_devs[-1,1])
    #print W_scores[0,2], (W_devs[0,2]), '\t', W_scores[-1,2], (W_devs[-1,2])
    
    print '\nCHINESE SCORES:'
    print 'INITIAL\t\tFINAL'
    print C_scores[0,0], (C_devs[0,0]), '\t', C_scores[-1,0], (C_devs[-1,0])
    print C_scores[0,1], (C_devs[0,1]), '\t', C_scores[-1,1], (C_devs[-1,1])
    #print C_scores[0,2], (C_devs[0,2]), '\t', C_scores[-1,2], (C_devs[-1,2])
    
    print '\nHINDUSTANI SCORES:'
    print 'INITIAL\t\tFINAL'
    print H_scores[0,0], (H_devs[0,0]), '\t', H_scores[-1,0], (H_devs[-1,0])
    print H_scores[0,1], (H_devs[0,1]), '\t', H_scores[-1,1], (H_devs[-1,1])
    #print H_scores[0,2], (H_devs[0,2]), '\t', H_scores[-1,2], (H_devs[-1,2])
    

def print_scores():
    print 'Starting...'
    for sys in 'WCH':
        for file_name in os.listdir('../LogFiles/Sim1/' + sys):
            with open('../LogFiles/Sim1/' + sys + '/' + file_name, 'r') as f:
                data = jlb(f)
                print sys, file_name, data['scores'][sys][-1]
                
                
def print_initial():
    print 'Starting...'
    for sys in 'WCH':
        for file_name in os.listdir('../LogFiles/Sim1/' + sys):
            with open('../LogFiles/Sim1/' + sys + '/' + file_name, 'r') as f:
                data = jlb(f)
                print data['scores'][sys][0][0], '\t', data['scores'][sys][0][1]
'''
print_initial()
#print_scores()

avg_scores_sim1()
std_devs_sim1()
'''
with open('../LogFiles/Sim1/Extracted/Scores.json', 'r') as f:
    scores = jlb(f)
    with open('../LogFiles/Sim1/Extracted/Std_Devs.json', 'r') as f2:
        devs = jlb(f2)
        print_start_and_end_scores(scores, devs)
    plot_scores_sim1(scores)
