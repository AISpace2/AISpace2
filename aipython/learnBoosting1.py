# learnBoosting.py - Functional Gradient Boosting
# Python 3 code. Full documentation at http://artint.info/code/python/code.pdf

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2016.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from learnProblem import Data_set, Learner

class Boosted_dataset(Data_set):
    def __init__(self, base_dataset, offset_fun):
        """new dataset which is like base_dataset,
           but offset_fun(e) is subtracted from the target of each example e
        """
        self.base_dataset = base_dataset
        self.offset_fun = offset_fun
        Data_set.__init__(self, base_dataset.train, base_dataset.test, 
                          base_dataset.prob_test, base_dataset.target_index)

    def create_features(self):
        self.input_features = self.base_dataset.input_features
        def newout(e):
            return self.base_dataset.target(e) - self.offset_fun(e)
        newout.frange = self.base_dataset.target.frange
        self.target = newout

class Boosting_learner(Learner):
    def __init__(self, dataset, base_learner_class):
        self.dataset = dataset
        self.base_learner_class = base_learner_class
        mean = sum(self.dataset.target(e) 
                   for e in self.dataset.train)/len(self.dataset.train)
        self.predictor = lambda e:mean     # function that returns mean for each example
        self.predictor.__doc__ = "lambda e:"+str(mean)
        self.offsets = [self.predictor]
        self.errors = [data.evaluate_dataset(data.test, self.predictor, "sum_squares")]
        self.display(1,"Predict mean test set error=", self.errors[0] )


    def learn(self, num_ensemble=10):
        """adds num_ensemble learners to the ensemble.
        returns a new predictor.
        """
        for i in range(num_ensemble):
            train_subset = Boosted_dataset(self.dataset, self.predictor)
            learner = self.base_learner_class(train_subset)
            new_offset = learner.learn()
            self.offsets.append(new_offset)
            def new_pred(e, old_pred=self.predictor, off=new_offset):
                return old_pred(e)+off(e)
            self.predictor = new_pred
            self.errors.append(data.evaluate_dataset(data.test, self.predictor,"sum_squares"))
            self.display(1,"After Iteration",len(self.offsets)-1,"test set error=", self.errors[-1])
        return self.predictor

# Testing

from learnDT import DT_learner
from learnProblem import Data_set, Data_from_file

def sp_DT_learner(min_prop=0.9):
    def make_learner(dataset):
        mne = len(dataset.train)*min_prop
        return DT_learner(dataset,min_number_examples=mne)
    return make_learner

data = Data_from_file('data/carbool.csv', target_index=-1)
#data = Data_from_file('data/SPECT.csv', target_index=0)
#data = Data_from_file('data/mail_reading.csv', target_index=-1)
#data = Data_from_file('data/holiday.csv', num_train=19, target_index=-1)
learner9 = Boosting_learner(data, sp_DT_learner(0.9))
#learner7 = Boosting_learner(data, sp_DT_learner(0.7))
#learner5 = Boosting_learner(data, sp_DT_learner(0.5))
predictor9 =learner9.learn(10)
for i in learner9.offsets: print(i.__doc__)
import matplotlib.pyplot as plt

def plot_boosting():
    learners = 
    learner1 = Boosting_learner(data, sp_DT_learner(0.1))
    learner1.learn(10)
    learner5 = Boosting_learner(data, sp_DT_learner(0.5))
    learner5.learn(10)
    plt.ion()
    plt.xscale('linear')  # change between log and linear scale
    plt.xlabel("number of trees")
    plt.ylabel(" error")
    plt.plot(range(len(learner9.errors)), learner9.errors, ls='-',c='k', label="90% min example threshold")
    #plt.plot(range(len(learner7.errors)), learner7.errors, ls='--',c='k', label="70% min example threshold")
    plt.plot(range(len(learner5.errors)), learner5.errors, ls='-.',c='k', label="50% min example threshold")
    plt.plot(range(len(learner1.errors)), learner1.errors, ls=':',c='k', label="10% min example threshold")
    plt.legend()
    plt.draw()

plot_boosting()
