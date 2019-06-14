# learnCrossValidation.py - Cross Validation for Parameter Tuning
# Python 3 code. Full documentation at http://artint.info/code/python/code.pdf

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2016.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from learnProblem import Data_set, Data_from_file, error_example
from learnDT import DT_learner
import matplotlib.pyplot as plt
import random

class K_fold_dataset(object):
    def __init__(self, training_set, num_folds):
        self.data = training_set.train.copy()
        self.target = training_set.target
        self.input_features = training_set.input_features
        self.num_folds = num_folds
        random.shuffle(self.data)
        self.fold_boundaries = [(len(self.data)*i)//num_folds
                                for i in range(0,num_folds+1)]

    def fold(self, fold_num):
        for i in range(self.fold_boundaries[fold_num],
                       self.fold_boundaries[fold_num+1]):
            yield self.data[i]

    def fold_complement(self, fold_num):
        for i in range(0,self.fold_boundaries[fold_num]):
            yield self.data[i]
        for i in range(self.fold_boundaries[fold_num+1],len(self.data)):
            yield self.data[i]

    def validation_error(self, learner, criterion, **other_params):
        error = 0
        try:
            for i in range(self.num_folds):
                predictor = learner(self, train=list(self.fold_complement(i)),
                                    **other_params).learn()
                error += sum( error_example(predictor(example),
                                            self.target(example),
                                            criterion)
                              for example in self.fold(i))
        except ValueError:
            return float("inf")  #infinity
        return error/len(self.data)

def plot_error(data,criterion="sum_squares", num_folds=5,  xscale='log'):
    """Plots the error on the validation set and the test set 
    with respect to settings of the minimum number of examples.
    xscale should be 'log' or 'linear'
    """
    plt.ion()
    plt.xscale(xscale)  # change between log and linear scale
    plt.xlabel("min_number_examples")
    plt.ylabel(criterion+" error")
    folded_data = K_fold_dataset(data, num_folds)
    verrors = []   # validation errors
    terrors = []   # test set errors
    for mne in range(1,len(data.train)+2):
        verrors.append(folded_data.validation_error(DT_learner,criterion,
                                                    min_number_examples=mne))
        tree = DT_learner(data, criterion, min_number_examples=mne).learn()
        terrors.append(data.evaluate_dataset(data.test,tree,criterion))
    plt.plot(range(1,len(data.train)+2),verrors,ls='--',c='k',label="validation for "+criterion)
    plt.plot(range(1,len(data.train)+2),terrors,linestyle='-.',color='r',label="test set for "+criterion)
    plt.legend()
    plt.draw()

# Try
# data = Data_from_file('data/mail_reading.csv', target_index=-1)
# data = Data_from_file('data/SPECT.csv',target_index=0)
# data = Data_from_file('data/carbool.csv', target_index=-1)
# plot_error(data)    # warning, may take a long time depending on the dataset

