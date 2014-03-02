import os
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score, precision_score
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

n_estimators = max(10, len(classes)/1000)
clf = AdaBoostClassifier(n_estimators=100)
clf.fit(predictors, classes)
pdkt_res = clf.predict(pdkt_input)

acc_score = accuracy_score(pdkt_true,pdkt_res)
prc_score = precision_score(pdkt_true,pdkt_res)

print(acc_score)
print(prc_score)