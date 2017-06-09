# learnEM.py - EM Learning
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from learnProblem import Data_set, Learner, Data_from_file
import random
import math
import matplotlib.pyplot as plt

class EM_learner(Learner):
    def __init__(self,dataset, num_classes):
        self.dataset = dataset
        self.num_classes = num_classes
        self.class_counts = None
        self.feature_counts = None

    def em_step(self, orig_class_counts, orig_feature_counts):
        """updates the model."""
        class_counts = [0]*self.num_classes
        feature_counts = [{val:[0]*self.num_classes
                               for val in feat.frange}
                               for feat in self.dataset.input_features]
        for tple in self.dataset.train:
            if orig_class_counts:  # a model exists
                tpl_class_dist = self.prob(tple, orig_class_counts, orig_feature_counts)
            else:                  # initially, with no model, return a random distribution
                tpl_class_dist = random_dist(self.num_classes)
            for cl in range(self.num_classes):
                class_counts[cl] += tpl_class_dist[cl]
                for (ind,feat) in enumerate(self.dataset.input_features):
                    feature_counts[ind][feat(tple)][cl] += tpl_class_dist[cl]
        return class_counts, feature_counts
        
    def prob(self,tple,class_counts,feature_counts):
        """returns a distribution over the classes for the original tuple in the current model
        """
        feats = self.dataset.input_features
        unnorm = [prod(feature_counts[i][feat(tple)][c]
                        for (i,feat) in enumerate(feats))/(class_counts[c]**(len(feats)-1))
                    for c in range(self.num_classes)]
        thesum = sum(unnorm)
        return [un/thesum for un in unnorm]
        
    def learn(self,n):
        """do n steps of em"""
        for i in range(n):
            self.class_counts,self.feature_counts = self.em_step(self.class_counts,
                                                                 self.feature_counts)

    def show_class(self,c):
        """sorts the data by the class and prints in order.
        For visualizing small data sets
        """
        sorted_data = sorted((self.prob(tpl,self.class_counts,self.feature_counts)[c],
                              ind,   # preserve ordering for equal probabilities
                              tpl)
                             for (ind,tpl) in enumerate(self.dataset.train))
        for cc,r,tpl in sorted_data:
            print(cc,*tpl,sep='\t')

    def logloss(self,tple):
        """returns the logloss of the prediction on tple, which is -log(P(tple))
        based on the current class counts and feature counts
        """
        feats = self.dataset.input_features
        res = 0
        cc = self.class_counts
        fc = self.feature_counts
        for c in range(self.num_classes):
            res += prod(fc[i][feat(tple)][c]
                        for (i,feat) in enumerate(feats))/(cc[c]**(len(feats)-1))
        if res>0:
            return -math.log2(res/len(self.dataset.train))
        else:
            return float("inf")  #infinity
        
    def plot_error(self, maxstep=20):
        """Plots the logloss error as a function of the number of steps"""
        plt.ion()
        plt.xlabel("step")
        plt.ylabel("Ave Logloss (bits)")
        train_errors = []
        if self.dataset.test:
            test_errors = []
        for i in range(maxstep):
            self.learn(1)
            train_errors.append( sum(self.logloss(tple) for tple in self.dataset.train)
                                 /len(self.dataset.train))
            if self.dataset.test:
                test_errors.append( sum(self.logloss(tple) for tple in self.dataset.test)
                                     /len(self.dataset.test))
        plt.plot(range(1,maxstep+1),train_errors,
                 label=str(self.num_classes)+" classes. Training set")
        if self.dataset.test:
            plt.plot(range(1,maxstep+1),test_errors,
                     label=str(self.num_classes)+" classes. Test set")
        plt.legend()
        plt.draw()
     
def prod(L):
    """returns the product of the elements of L"""
    res = 1
    for e in L:
        res *= e
    return res
    
def random_dist(k):
    """generate k random numbers that sum to 1"""
    res = [random.random() for i in range(k)]
    s = sum(res)
    return [v/s for v in res]

data = Data_from_file('data/emdata2.csv', num_train=10, target_index=2000)
eml = EM_learner(data,2)
num_iter=2
print("Class assignment after",num_iter,"iterations:")
eml.learn(num_iter); eml.show_class(0)

# Plot the error
# em2=EM_learner(data,2); em2.plot_error(40)   # 2 classes
# em3=EM_learner(data,3); em3.plot_error(40)   # 3 classes
# em13=EM_learner(data,13); em13.plot_error(40) # 13 classes

# data = Data_from_file('data/carbool.csv', target_index=2000,boolean_features=False)
# [f.frange for f in data.input_features]
# eml = EM_learner(data,3)
# eml.learn(20); eml.show_class(0)
# em3=EM_learner(data,3); em3.plot_error(60)    # 3 classes
# em3=EM_learner(data,30); em3.plot_error(60)   # 30 classes

