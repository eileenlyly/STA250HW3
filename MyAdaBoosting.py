import os, math
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score
import numpy as np
from numpy.random import rand

def sampleByWeight(array, weights, size):
    index = []
    maxidx = len(array)
    cs = np.cumsum(weights)
    while len(index) < size:
        index.append(sum(cs < rand()))
    
    return array[index]

class MyAdaBoosting:
    
    def __init__(self,classifier):
        self.classifier = classifier
        self.weak_classifier_ensemble = []
        self.alpha = []
    
    def train(self, X, Y, T, k):
        n = len(X)
        w = (1.0/n) * np.ones(n) 
        self.T = T
        self.weak_classifier_ensemble = []
        self.alpha = []     
        for t in range(T):
            weak_learner = self.classifier()
            x_sample = sampleByWeight(X,w,k)
            y_sample = sampleByWeight(Y,w,k)
            weak_learner.fit(x_sample,y_sample)
            Y_pdkt = weak_learner.predict(X)
            e = np.ones(n)
            error = 0
            for i in range(n):
                if Y_pdkt[i] != Y[i]:
                    e[i] = -1
                    error += 1
                        
            error = error * 1.0 / n
            alpha = 0.5 * math.log((1 - error) / error)
            w *= np.exp(-alpha * e)
            w /= sum(w)
            self.weak_classifier_ensemble.append(weak_learner)
            self.alpha.append(alpha) 
            if error < 0.1:
                print("Training complete after " + str(t) + " iterations")
                break
            
        print("Training complete after " + str(T) + " iterations")
        
        
    def predict(self, X, minY, maxY):
        n = len(X)
        Y = np.zeros(n)
        e = sum(self.alpha)
        for t in range(self.T):
            weak_learner = self.weak_classifier_ensemble[t]
            Y += weak_learner.predict(X) * self.alpha[t] / e
            
        for i in range(len(Y)):
            Y[i] = int(round(Y[i]))
            if Y[i] > maxY:
                Y[i] = maxY
            if Y[i] < minY:
                Y[i] = minY
                
        return Y
        
        
if __name__ == "__main__":
        
    os.chdir('/Users/eileenlyly/courses/STA250/HW3/data/')

    train_data = np.loadtxt('train-sample-output-binary.csv',dtype=np.object,delimiter=',')
    train_data = train_data[1:,:].astype(np.int)

    pdkt_data = np.loadtxt('pdkt-output-binary.csv',dtype=np.object,delimiter=',')
    pdkt_data = pdkt_data[1:,:].astype(np.int)
    pdkt_input = pdkt_data[:,1:]
    pdkt_true = np.ravel(pdkt_data[:,0:1])

    classes = np.ravel(train_data[:,0:1])
    predictors = train_data[:,1:]
        
    ab = MyAdaBoosting(GaussianNB)
    T = 100
    k = max(50, len(predictors) / 10000)
    ab.train(predictors, classes, T, k)
    pdkt_res = ab.predict(pdkt_input,0,1)
    #print(pdkt_res)
    acc_score = accuracy_score(pdkt_true,pdkt_res)
    prc_score = precision_score(pdkt_true,pdkt_res)

    print(acc_score)
    print(prc_score)
    