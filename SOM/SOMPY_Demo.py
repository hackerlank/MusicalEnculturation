import pandas as pd
import time as time
import numpy as np
from matplotlib import pyplot as plt
pd.__version__
import sys
import SOMPY as SOM

#The critical factor which increases the computational time, but mostly the memory problem is the size of SOM (i.e. msz0,msz1), 
#other wise the training data will be parallelized  


#This is your selected map size 
msz0 = 30
msz1 = 30

#This is a random data set, but in general it is assumed that you have your own data set as a numpy ndarray 
Data = np.random.rand(10*1000,20)
print 'Data size: ', Data.shape


sm = SOM.SOM('sm', Data, mapsize = [msz0, msz1],norm_method = 'var',initmethod='pca')
sm.train(n_job = 1, shared_memory = 'no',verbose='final')

sm.view_map(text_size=7)

dlen = 200
Data1 = pd.DataFrame(data= 1*np.random.rand(dlen,2))
Data1.values[:,1] = (Data1.values[:,0][:,np.newaxis] + .42*np.random.rand(dlen,1))[:,0]


Data2 = pd.DataFrame(data= 1*np.random.rand(dlen,2)+1)
Data2.values[:,1] = (-1*Data2.values[:,0][:,np.newaxis] + .62*np.random.rand(dlen,1))[:,0]

Data3 = pd.DataFrame(data= 1*np.random.rand(dlen,2)+2)
Data3.values[:,1] = (.5*Data3.values[:,0][:,np.newaxis] + 1*np.random.rand(dlen,1))[:,0]


Data4 = pd.DataFrame(data= 1*np.random.rand(dlen,2)+3.5)
Data4.values[:,1] = (-.1*Data4.values[:,0][:,np.newaxis] + .5*np.random.rand(dlen,1))[:,0]


DataCL1 = np.concatenate((Data1,Data2,Data3,Data4))

fig = plt.figure()
plt.plot(DataCL1[:,0],DataCL1[:,1],'ob',alpha=0.2, markersize=4)
fig.set_size_inches(7,7)

sm2 = SOM.SOM('sm', DataCL1, mapsize = [msz0, msz1],norm_method = 'var',initmethod='pca')
sm2.train(n_job = 1, shared_memory = 'no',verbose='final')

sm2.view_map(text_size=7)


##Hit map
sm2.hit_map()