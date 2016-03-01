from prep_data import prep_data
from results_out import output_results
from json_loading import json_load_byteified as jlb
import scipy
from model import SOM

def genTest(som, iterations, mode, sys):
    keynames, keys, data = prep_data(mode, sys)
    som.train(iterations, data)
    output_results(som, keynames, keys)
    
def sim1(sys):
    keynames, keys, data = prep_data('M', sys)
    for i in range(10):
        som = SOM(30, 30, 12, .25, sys, 'M')
        som.train(100, data, '../LogFiles/Sim1/'+sys+'/log'+str(i)+'.json')
        output_results(som, keynames, keys)

def sim2(systems):
    keynames, keys, data = prep_data('M', systems)
    for i in range(10):
        som = SOM(30, 30, 12, .25, systems, 'M')
        som.train(100, data, '../LogFiles/Sim2/'+systems+'/log'+str(i)+'.json')
        output_results(som, keynames, keys)
        

def sim3(mode1, mode2, sys1, sys2):
    for i in range(10):
        f = open('../LogFiles/Sim1/'+sys1+'/log'+str(i)+'.json', 'r')
        json = jlb(f)
        nodes = scipy.array(json['states'][-1])
        som = SOM(30, 30, 12, .25, sys2, mode2, nodes)
        
        # Fix radius and learning rates
        som.learning_rate /= 100.
        som.radius = 1.
        som.fixedR = True
        som.fixedLR = True
        
        # Update dataset to include new system(s)
        keynames, keys, data = prep_data(mode2, sys2)
        som.train(100,data, '../LogFiles/Sim3a/'+sys2+'/log'+str(i)+'.json')
        output_results(som, keynames, keys)