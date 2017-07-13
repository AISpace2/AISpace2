# learnLinear.py - Linear Regression and Classification
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from learnProblem import Learner
import random, math

class Linear_learner(Learner):
    def __init__(self, dataset, train=None, 
                 learning_rate=0.1, max_init = 0.2,
                 squashed=True):
        """Creates a gradient descent searcher for a linear classifier.
        The main learning is carried out by learn()
        
        dataset provides the target and the input features
        train provides a subset of the training data to use
        number_iterations is the default number of steps of gradient descent
        learning_rate is the gradient descent step size
        max_init is the maximum absolute value of the initial weights
        squashed specifies whether the output is a squashed linear function
        """
        self.dataset = dataset
        self.target = dataset.target
        if train==None:
            self.train = self.dataset.train
        else:
            self.train = train
        self.learning_rate = learning_rate
        self.squashed = squashed
        self.input_features = dataset.input_features+[one] # one is defined below
        self.weights = {feat:random.uniform(-max_init,max_init)
                        for feat in self.input_features}
        

    def predictor(self,e):
        """returns the prediction of the learner on example e"""
        linpred = sum(w*f(e) for f,w in self.weights.items())
        if self.squashed:
            return sigmoid(linpred)
        else:
            return linpred

    def predictor_string(self, sig_dig=3):
        """returns the doc string for the current prediction function
        sig_dig is the number of significant digits in the numbers"""
        doc = "+".join(str(round(val,sig_dig))+"*"+feat.__doc__
                        for feat,val in self.weights.items())
        if self.squashed:
            return "sigmoid("+ doc+")" 
        else:
            return doc

    def learn(self,num_iter=100):
        for it in range(num_iter):
            self.display(2,"prediction=",self.predictor_string())
            for e in self.train:
                predicted = self.predictor(e)
                error = self.target(e) - predicted
                update = self.learning_rate*error
                for feat in self.weights:
                    self.weights[feat] +=  update*feat(e)
        #self.predictor.__doc__ = self.predictor_string()
        #return self.predictor

def one(e):
    "1"
    return 1

def sigmoid(x):
    return 1/(1+math.exp(-x))

from learnProblem import Data_set, Data_from_file
import matplotlib.pyplot as plt
def test(**args):
    data = Data_from_file('data/SPECT.csv', target_index=0)
    # data = Data_from_file('data/mail_reading.csv', target_index=-1)
    # data = Data_from_file('data/carbool.csv', target_index=-1)
    learner = Linear_learner(data,**args)
    learner.learn()
    print("function learned is", learner.predictor_string())
    for ecrit in Data_set.evaluation_criteria:
        test_error = data.evaluate_dataset(data.test, learner.predictor, ecrit)
        print("    Average", ecrit, "error is", test_error)

def plot_steps(learner=None,
               data = None,
               criterion="sum-of-squares",
               step=1,
               num_steps=1000,
               log_scale=True,
               label=""):
    """
    plots the training and test error for a learner.
    data is the 
    learner_class is the class of the learning algorithm
    criterion gives the evaluation criterion plotted on the y-axis
    step specifies how many steps are run for each point on the plot
    num_steps is the number of points to plot
    
    """
    plt.ion()
    plt.xlabel("step")
    plt.ylabel("Average "+criterion+" error")
    if log_scale:
        plt.xscale('log')  #plt.semilogx()  #Makes a log scale
    else:
        plt.xscale('linear')
    if data is None:
        data = Data_from_file('data/holiday.csv', num_train=19, target_index=-1)
        #data = Data_from_file('data/SPECT.csv', target_index=0)
        # data = Data_from_file('data/mail_reading.csv', target_index=-1)
        # data = Data_from_file('data/carbool.csv', target_index=-1)
    random.seed(None)    # reset seed 
    if learner is None:
        learner = Linear_learner(data)
    train_errors = []
    test_errors = []
    for i in range(1,num_steps+1,step):
        test_errors.append(data.evaluate_dataset(data.test, learner.predictor, criterion))
        train_errors.append(data.evaluate_dataset(data.train, learner.predictor, criterion))
        learner.display(2, "Train error:",train_errors[-1],
                          "Test error:",test_errors[-1])
        learner.learn(num_iter=step)
    plt.plot(range(1,num_steps+1,step),train_errors,ls='-',c='k',label="training errors")
    plt.plot(range(1,num_steps+1,step),test_errors,ls='--',c='k',label="test errors")
    plt.legend()
    plt.draw()
    learner.display(1, "Train error:",train_errors[-1],
                          "Test error:",test_errors[-1])

if __name__ == "__main__":
    test()

# This generates the figure
# from learnProblem import Data_set_augmented,prod_feat
# data = Data_from_file('data/SPECT.csv', prob_test=0.5, target_index=0)
# dataplus = Data_set_augmented(data,[],[prod_feat])
# plot_steps(data=data,num_steps=10000)
# plot_steps(data=dataplus,num_steps=10000)  # warning very slow
def arange(start,stop,step):
    """returns enumeration of values in the range [start,stop) separated by step.
    like the built-in range(start,stop,step) but allows for integers and floats.
    Note that rounding errors are expected with real numbers.
    """
    while start<stop:
        yield start
        start += step

def plot_prediction(learner=None,
               data = None,
               minx = 0,
               maxx = 5,
               step_size = 0.01,    # for plotting
               label="function"):
    plt.ion()
    plt.xlabel("x")
    plt.ylabel("y")
    if data is None:
        data = Data_from_file('data/simp_regr.csv', prob_test=0, 
                              boolean_features=False, target_index=-1)
    if learner is None:
        learner = Linear_learner(data,squashed=False)
    learner.learning_rate=0.001
    learner.learn(100)
    learner.learning_rate=0.0001
    learner.learn(1000)
    learner.learning_rate=0.00001
    learner.learn(10000)
    learner.display(1,"function learned is", learner.predictor_string(),
              "error=",data.evaluate_dataset(data.train, learner.predictor, "sum-of-squares"))
    plt.plot([e[0] for e in data.train],[e[-1] for e in data.train],"bo",label="data")
    plt.plot(list(arange(minx,maxx,step_size)),[learner.predictor([x])
                                          for x in arange(minx,maxx,step_size)],
                                        label=label)
    plt.legend()
    plt.draw()
    
from learnProblem import Data_set_augmented, power_feat
def plot_polynomials(data=None,
                learner_class = Linear_learner,
                max_degree=5,
                minx = 0,
                maxx = 5,
                num_iter = 100000,
                learning_rate = 0.0001,
                step_size = 0.01,   # for plotting
                ):
    plt.ion()
    plt.xlabel("x")
    plt.ylabel("y")
    if data is None:
        data = Data_from_file('data/simp_regr.csv', prob_test=0, 
                              boolean_features=False, target_index=-1)
    plt.plot([e[0] for e in data.train],[e[-1] for e in data.train],"ko",label="data")
    x_values = list(arange(minx,maxx,step_size))
    line_styles = ['-','--','-.',':']
    colors = ['0.5','k','k','k','k']
    for degree in range(max_degree):
        data_aug = Data_set_augmented(data,[power_feat(n) for n in range(1,degree+1)],
                                          include_orig=False)
        learner = learner_class(data_aug,squashed=False)
        learner.learning_rate=learning_rate
        learner.learn(num_iter)
        learner.display(1,"For degree",degree,
                     "function learned is", learner.predictor_string(),
                     "error=",data.evaluate_dataset(data.train, learner.predictor, "sum-of-squares"))
        ls = line_styles[degree % len(line_styles)]
        col = colors[degree % len(colors)]
        plt.plot(x_values,[learner.predictor([x]) for x in x_values], linestyle=ls, color=col,
                          label="degree="+str(degree))
        plt.legend(loc='upper left')
        plt.draw()

# Try:
# plot_prediction()
# plot_polynomials()
#data = Data_from_file('data/mail_reading.csv', target_index=-1)
#plot_prediction(data=data)

