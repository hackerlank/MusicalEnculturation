import numpy as np
import os
import json
from json_loading import json_load_byteified as jlb
from matplotlib import pyplot

def avg_scores_sim2():
    print 'Starting...'
    score_log = {}
    for systems in ('WCH', 'WC','WH','CH'):
        score_log[systems] = {}
        for sys in systems:
            total_scores = np.array([[0., 0., 0.] for i in range(101)])
            for file_name in os.listdir('../LogFiles/Sim2/' + systems):
                with open('../LogFiles/Sim2/' + systems + '/' + file_name, 'r') as f:
                    data = jlb(f)
                    scores = np.array(data['scores'][sys])
                    total_scores += scores
            avg_scores = total_scores/10.
            score_log[systems][sys] = (avg_scores).tolist()
    
    f = open('../LogFiles/Sim2/Extracted/Scores.json', 'w')
    json.dump(score_log, f)



def std_devs_sim2():
    print 'Starting...'
    dev_log = {}
    for systems in ('WCH', 'WC','WH','CH'):
        dev_log[systems] = {}
        for sys in systems:
            scores = np.empty((101,3,10))
            i = 0
            for file_name in os.listdir('../LogFiles/Sim2/' + systems):
                with open('../LogFiles/Sim2/' + systems + '/' + file_name, 'r') as f:
                    data = jlb(f)
                    scores[:,:,i] = np.array(data['scores'][sys])
                i += 1
            std_devs = np.empty((101,3))
            for x in range(101):
                for y in range(3):
                    std_devs[x,y] = np.std(scores[x,y,:])
            dev_log[systems][sys] = (std_devs).tolist()
    
    f = open('../LogFiles/Sim2/Extracted/Std_Devs.json', 'w')
    json.dump(dev_log, f)



def plot_scores_sim2(scores):
    fig = pyplot.figure(figsize=(30,50))    
    x = range(101)
    i = 1
    for systems in scores:
        thresh = fig.add_subplot(4,2,i)
        act = fig.add_subplot(4,2,i+1)
        thresh.set_title('Pitch Accuracy: ' + str(systems))
        act.set_title('Activation Accuracy: ' + str(systems))  
        if 'W' in systems:
            W_scores = np.array(scores[systems]['W'])
            linet1, = thresh.plot(x, W_scores[:,0], 'b', linewidth=2, label='Western')
            linea1, = act.plot(x, W_scores[:,1], 'b', linewidth=2, label='Western')
        if 'C' in systems:        
            C_scores = np.array(scores[systems]['C'])
            linet2, = thresh.plot(x, C_scores[:,0], 'r', linewidth=2, label='Chinese')
            linea2, = act.plot(x, C_scores[:,1], 'r', linewidth=2, label='Chinese')
        if 'H' in systems:
            H_scores = np.array(scores[systems]['H'])
            linet3, = thresh.plot(x, H_scores[:,0], 'g', linewidth=2, label='Hindustani')
            linea3, = act.plot(x, H_scores[:,1], 'g', linewidth=2, label='Hindustani')

        thresh.set_ylim((0,100))
        thresh.legend(loc=4)
        act.set_ylim((0,100))
        act.legend(loc=4)
        i +=2
        
    pyplot.show()
    
        
def print_start_and_end_scores(scores, devs):
    for systems in scores:
        print 'RESULTS FOR SYSTEMS: ' + systems
        if 'W' in systems:
            W_scores = np.array(scores[systems]['W'])
            W_devs = np.array(devs[systems]['W'])
            print 'WESTERN SCORES:'
            print 'INITIAL\t\tFINAL'
            print W_scores[0,0], (W_devs[0,0]), '\t', W_scores[-1,0], (W_devs[-1,0])
            print W_scores[0,1], (W_devs[0,1]), '\t', W_scores[-1,1], (W_devs[-1,1])
            #print W_scores[0,2], (W_devs[0,2]), '\t', W_scores[-1,2], (W_devs[-1,2])
        
        if 'C' in systems:
            C_scores = np.array(scores[systems]['C'])
            C_devs = np.array(devs[systems]['C'])
            print '\nCHINESE SCORES:'
            print 'INITIAL\t\tFINAL'
            print C_scores[0,0], (C_devs[0,0]), '\t', C_scores[-1,0], (C_devs[-1,0])
            print C_scores[0,1], (C_devs[0,1]), '\t', C_scores[-1,1], (C_devs[-1,1])
            #print C_scores[0,2], (C_devs[0,2]), '\t', C_scores[-1,2], (C_devs[-1,2])
        
        if 'H' in systems:
            H_scores = np.array(scores[systems]['H'])
            H_devs = np.array(devs[systems]['H'])
            print '\nHINDUSTANI SCORES:'
            print 'INITIAL\t\tFINAL'
            print H_scores[0,0], (H_devs[0,0]), '\t', H_scores[-1,0], (H_devs[-1,0])
            print H_scores[0,1], (H_devs[0,1]), '\t', H_scores[-1,1], (H_devs[-1,1])
            #print H_scores[0,2], (H_devs[0,2]), '\t', H_scores[-1,2], (H_devs[-1,2])
        print '__________________________________________________________'
    


def print_scores():
    print 'Starting...'
    for systems in ('WCH', 'WC','WH','CH'):
        for file_name in os.listdir('../LogFiles/Sim2/' + systems):
            with open('../LogFiles/Sim2/' + systems + '/' + file_name, 'r') as f:
                data = jlb(f)
                for sys in systems:
                    print systems, sys, file_name, data['scores'][sys][-1]

def print_initial():
    print 'Starting...'
    for systems in ('WCH', 'WC','WH','CH'):
        for file_name in os.listdir('../LogFiles/Sim2/' + systems):
            with open('../LogFiles/Sim2/' + systems + '/' + file_name, 'r') as f:
                data = jlb(f)
                for sys in systems:
                    print systems, '\t', sys, '\t', data['scores'][sys][0][0], '\t', data['scores'][sys][0][1]

'''
print_initial()
#print_scores()

avg_scores_sim2()
std_devs_sim2()
'''
with open('../LogFiles/Sim2/Extracted/Scores.json', 'r') as f:
    scores = jlb(f)
    with open('../LogFiles/Sim2/Extracted/Std_Devs.json', 'r') as f2:
        devs = jlb(f2)
        print_start_and_end_scores(scores, devs)
    plot_scores_sim2(scores)
