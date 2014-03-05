import os, scipy.stats
import numpy as np

os.chdir('/Users/eileenlyly/courses/STA250/HW3/data/')

train_data = np.loadtxt('train-sample-output.csv',dtype=np.object,delimiter=',')
train_data = train_data[1:,:].astype(np.int)

classes = np.ravel(train_data[:,0:1])
predictors = train_data[:,1:]

row, col = predictors.shape

rhos = []

c = classes.reshape(1,row)[0]

for i in range(col):
    p = predictors[:,i:i+1].reshape(1,row)[0]
    rho, pval = scipy.stats.spearmanr(p,c)
    rhos.append(rho)
    
print rhos
    


