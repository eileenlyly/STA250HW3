import os
from sklearn import neighbors
from sklearn.metrics import accuracy_score, average_precision_score
from sklearn.metrics import classification_report
import numpy as np

os.chdir('/Users/eileenlyly/courses/STA250/HW3/data/')

train_data = np.loadtxt('train-output.csv',dtype=np.object,delimiter=',')
train_data = train_data[1:,:].astype(np.int)

pdkt_data = np.loadtxt('pdkt-output.csv',dtype=np.object,delimiter=',')
pdkt_data = pdkt_data[1:,:].astype(np.int)
pdkt_input = pdkt_data[:,1:]
pdkt_true = np.ravel(pdkt_data[:,0:1])

classes = np.ravel(train_data[:,0:1])
predictors = train_data[:,1:]

n_nbrs = max(10, len(classes)/1000)
clf = neighbors.KNeighborsClassifier(n_nbrs, weights = 'uniform')
clf.fit(predictors, classes)
pdkt_res = clf.predict(pdkt_input)

acc_score = accuracy_score(pdkt_true,pdkt_res)
prc_score = average_precision_score(pdkt_true,pdkt_res)

binary_hit = 0
class_hit = 0
