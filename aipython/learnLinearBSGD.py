# learnLinearBSGD.py - Linear Learner with Batched Stochastic Gradient Descent
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from learnLinear import Linear_learner
import random, math

class Linear_learner_bsgd(Linear_learner):
    def __init__(self, *args, batch_size=10, **kargs):
        Linear_learner.__init__(self, *args, **kargs)
        self.batch_size = batch_size

    def learn(self,num_iter=None):
        if num_iter is None:
            num_iter = self.number_iterations
        batch_size = min(self.batch_size, len(self.train))
        d = {feat:0 for feat in self.weights}
        for it in range(num_iter):
            self.display(2,"prediction=",self.predictor_string())
            for e in random.sample(self.train, batch_size):
                predicted = self.predictor(e)
                error = self.target(e) - predicted
                update = self.learning_rate*error
                for feat in self.weights:
                    d[feat] +=  update*feat(e)
            for feat in self.weights:
                self.weights[feat] +=  d[feat]
                d[feat]=0

# from learnLinear import plot_steps
# from learnProblem import Data_from_file
# data = Data_from_file('data/holiday.csv', target_index=-1)
# learner = Linear_learner_bsgd(data)
# plot_steps(learner = learner, data=data)

# to plot polynomials with batching (compare to SGD)
# from learnLinear import plot_polynomials
# plot_polynomials(learner_class = Linear_learner_bsgd)

