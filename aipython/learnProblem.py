# learnProblem.py - A Learning Problem
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

import math, random
import csv
from utilities import Displayable

boolean = [False, True]

class Data_set(Displayable):
    """ A data set consists of a list of training data and a list of test data.
    """
    seed = None #123456  # make it None for a different test set each time

    def __init__(self, train, test=None, prob_test=0.30, target_index=0, header=None):
        """A dataset for learning.
        train is a list of tuples representing the training examples
        test is the list of tuples representing the test examples
        if test is None, a test set is created by selecting each
            example with probability prob_test
        target_index is the index of the target. If negative, it counts from right.
            If target_index is larger than the number of properties,
            there is no target (for unsupervised learning)
        header is a list of names for the features
        """
        if test is None:
            train,test = partition_data(train, prob_test, seed=self.seed)
        self.train = train
        self.test = test
        self.display(1,"Tuples read. \nTraining set", len(train),
                    "examples. Number of columns:",{len(e) for e in train},
                    "\nTest set", len(test),
                    "examples. Number of columns:",{len(e) for e in test}
                    )
        self.prob_test = prob_test
        self.num_properties = len(self.train[0])
        if target_index < 0:   #allows for -1, -2, etc.
            target_index = self.num_properties + target_index
        self.target_index = target_index
        self.header = header
        self.create_features()
        self.display(1,"There are",len(self.input_features),"features")

    def create_features(self):
        """create the input features and target feature.
        This assumes that the features all have domain {0,1}.
        This should be overridden if the features have a different domain.
        """
        self.input_features = []
        for i in range(self.num_properties):
            def feat(e,index=i):
                return e[index]
            if self.header:
                feat.__doc__ = self.header[i]
            else:
                feat.__doc__ = "e["+str(i)+"]"
            feat.frange = [0,1]
            if i == self.target_index:
                self.target = feat
            else:
                self.input_features.append(feat)

    evaluation_criteria = ["sum-of-squares","sum_absolute","logloss"]
        
    def evaluate_dataset(self, data, predictor, evaluation_criterion):
        """Evaluates predictor on data according to the evaluation_criterion.
        predictor is a function that takes an example and returns a
                prediction for the target feature. 
        evaluation_criterion is one of the  evaluation_criteria.
        """
        assert evaluation_criterion in self.evaluation_criteria,"given: "+str(evaluation_criterion)
        if data:
            try:
                error = sum(error_example(predictor(example), self.target(example),
                                          evaluation_criterion) 
                            for example in data)/len(data)
            except ValueError:
                return float("inf")  # infinity 
            return error

def error_example(predicted, actual, evaluation_criterion):
    """returns the error of the for the predicted value given the actual value 
    according to evaluation_criterion.
    Throws ValueError if the error is infinite (log(0))
    """
    if evaluation_criterion=="sum-of-squares":
        return (predicted-actual)**2
    elif evaluation_criterion=="sum_absolute":
        return abs(predicted-actual)
    elif evaluation_criterion=="logloss":
        assert actual in [0,1], "actual="+str(actual)
        if actual==0:
            return -math.log2(1-predicted)
        else:
            return -math.log2(predicted)
    elif evaluation_criterion=="characteristic_ss":
        return sum((1-predicted[i])**2 if actual==i else predicted[i]**2
                       for i in range(len(predicted)))
    else:
        raise RuntimeError("Not evaluation criteria: "+str(evaluation_criterion))

def partition_data(data, prob_test=0.30, seed=None):
    """partitions the data into a training set and a test set, where
    prob_test is the probability of each example being in the test set.
    """
    train = []
    test = []
    if seed:     # given seed makes the partition consistent from run-to-run
        random.seed(seed)
    for example in data:
        if random.random() < prob_test:
            test.append(example)
        else:
            train.append(example)
    return train, test

class Data_from_file(Data_set):
    def __init__(self, file_name, separator=',', num_train=None, prob_test=0.3,
                 has_header=False, target_index=0, boolean_features=True,
                 categorical=[], include_only=None):
        """create a dataset from a file
        separator is the character that separates the attributes
        num_train is a number n specifying the first n tuples are training, or None 
        prob_test is the probability an example should in the test set (if num_train is None)
        has_header is True if the first line of file is a header
        target_index specifies which feature is the target
        boolean_features specifies whether we want to create Boolean features
            (if False, is uses the original features).
        categorical is a set (or list) of features that should be treated as categorical
        include_only is a list or set of indexes of columns to include
        """
        self.boolean_features = boolean_features
        with open(file_name,'r',newline='') as csvfile:
            # data_all = csv.reader(csvfile,delimiter=separator)  # for more complicted CSV files
            data_all = (line.strip().split(separator) for line in csvfile)
            if include_only is not None:
                data_all = ([v for (i,v) in enumerate(line) if i in include_only] for line in data_all)
            if has_header:
                header = next(data_all)
            else:
                header = None
            data_tuples = (make_num(d) for d in data_all if len(d)>1)
            if num_train is not None:
                # training set is divided into training then text examples
                # the file is only read once, and the data is placed in appropriate list
                train = []
                for i in range(num_train):     # will give an error if insufficient examples
                    train.append(next(data_tuples))
                test = list(data_tuples)
                Data_set.__init__(self,train, test=test, target_index=target_index,header=header)
            else:     # randomly assign training and test examples
                Data_set.__init__(self,data_tuples, prob_test=prob_test,
                                  target_index=target_index, header=header)

    def __str__(self):
        if self.train and len(self.train)>0: 
            return ("Data: "+str(len(self.train))+" training examples, "
                    +str(len(self.test))+" test examples, "
                    +str(len(self.train[0]))+" features.")
        else:
            return ("Data: "+str(len(self.train))+" training examples, "
                    +str(len(self.test))+" test examples.")

    def create_features(self, max_num_cuts=8):
        """creates boolean features from input features.
        max_num_cuts is the maximum number of binary variables
           to split a numerical feature into. 
        """
        ranges = [set() for i in range(self.num_properties)]
        for example in self.train:
            for ind,val in enumerate(example):
                ranges[ind].add(val)
        if self.target_index <= self.num_properties:
            def target(e,index=self.target_index):
                return e[index]
            if self.header:
                target.__doc__ = self.header[ind]
            else:
                target.__doc__ = "e["+str(ind)+"]"
            target.frange = ranges[self.target_index]
            self.target = target
        if self.boolean_features:
            self.input_features = []
            for ind,frange in enumerate(ranges):
                if ind != self.target_index and len(frange)>1:
                    if len(frange) == 2:
                        # two values, the feature is equality to one of them.
                        true_val = list(frange)[1] # choose one as true
                        def feat(e, i=ind, tv=true_val):
                            return e[i]==tv
                        if self.header:
                            feat.__doc__ = self.header[ind]+"=="+str(true_val)
                        else:
                            feat.__doc__ = "e["+str(ind)+"]=="+str(true_val)
                        feat.frange = boolean
                        self.input_features.append(feat)
                    elif all(isinstance(val,(int,float)) for val in frange):
                        # all numeric, create cuts of the data
                        sorted_frange = sorted(frange)
                        num_cuts = min(max_num_cuts,len(frange))
                        cut_positions = [len(frange)*i//num_cuts for i in range(1,num_cuts)]
                        for cut in cut_positions:
                            cutat = sorted_frange[cut]
                            def feat(e, ind_=ind, cutat=cutat):
                                return e[ind_] < cutat
                            
                            if self.header:
                                feat.__doc__ = self.header[ind]+"<"+str(cutat)
                            else:
                                feat.__doc__ = "e["+str(ind)+"]<"+str(cutat)
                            feat.frange = boolean
                            self.input_features.append(feat)
                    else:
                        # create an indicator function for every value
                        for val in frange:
                            def feat(e, ind_=ind, val_=val):
                                return e[ind_] == val_
                            if self.header:
                                feat.__doc__ = self.header[ind]+"=="+str(val)
                            else:
                                feat.__doc__= "e["+str(ind)+"]=="+str(val)
                            feat.frange = boolean
                            self.input_features.append(feat)
        else: # boolean_features is off
            self.input_features = []
            for i in range(self.num_properties):
                def feat(e,index=i):
                    return e[index]
                if self.header:
                    feat.__doc__ = self.header[i]
                else:
                     feat.__doc__ = "e["+str(i)+"]"
                feat.frange = ranges[i]
                if i == self.target_index:
                    self.target = feat
                else:
                    self.input_features.append(feat)
def make_num(str_list):
    """make the elements of string list str_list numerical if possible.
    Otherwise remove initial and trailing spaces.
    """
    res = []
    for e in str_list:
        try:
            res.append(int(e))
        except ValueError:
            try:
                res.append(float(e))
            except ValueError:
                res.append(e.strip())
    return res

class Data_set_augmented(Data_set):
    def __init__(self, dataset, unary_functions=[], binary_functions=[], include_orig=True):
        """creates a dataset like dataset but with new features
        unary_function is a list of  unary feature constructors
        binary_functions is a list of  binary feature combiners.
        include_orig specifies whether the original features should be included
        """
        self.orig_dataset = dataset
        self.unary_functions = unary_functions
        self.binary_functions = binary_functions
        self.include_orig = include_orig
        self.target = dataset.target
        Data_set.__init__(self,dataset.train, test=dataset.test,
                          target_index = dataset.target_index)

    def create_features(self):
        if self.include_orig:
            self.input_features = self.orig_dataset.input_features.copy()
        else:
            self.input_features = []
        for u in self.unary_functions:
            for f in self.orig_dataset.input_features:
                self.input_features.append(u(f))
        for b in self.binary_functions:
            for f1 in self.orig_dataset.input_features:
                for f2 in self.orig_dataset.input_features:
                    if f1 != f2:
                        self.input_features.append(b(f1,f2))

def square(f):
    """a unary  feature constructor to construct the square of a feature
    """
    def sq(e):
        return f(e)**2
    sq.__doc__ = f.__doc__+"**2"
    return sq

def power_feat(n):
    """given n returns a unary  feature constructor to construct the nth power of a feature.
    e.g., power_feat(2) is the same as square
    """
    def fn(f,n=n):
        def pow(e,n=n):
            return f(e)**n
        pow.__doc__ = f.__doc__+"**"+str(n)
        return pow
    return fn

def prod_feat(f1,f2):
    """a new feature that is the product of features f1 and f2
    """
    def feat(e):
        return f1(e)*f2(e)
    feat.__doc__ = f1.__doc__+"*"+f2.__doc__
    return feat

def eq_feat(f1,f2):
    """a new feature that is 1 if f1 and f2 give same value
    """
    def feat(e):
        return 1 if f1(e)==f2(e) else 0
    feat.__doc__ = f1.__doc__+"=="+f2.__doc__
    return feat

def xor_feat(f1,f2):
    """a new feature that is 1 if f1 and f2 give different values
    """
    def feat(e):
        return 1 if f1(e)!=f2(e) else 0
    feat.__doc__ = f1.__doc__+"!="+f2.__doc__
    return feat

# from learnProblem import Data_set_augmented,prod_feat
# data = Data_from_file('data/holiday.csv', num_train=19, target_index=-1)
## data = Data_from_file('data/SPECT.csv',  prob_test=0.5, target_index=0)
# dataplus = Data_set_augmented(data,[],[prod_feat])
# dataplus = Data_set_augmented(data,[],[prod_feat,xor_feat])
from utilities import Displayable
 
class Learner(Displayable):
    def __init__(self, dataset):
        raise NotImplementedError("Learner.__init__")    # abstract method

    def learn(self):
        """returns a predictor, a function from a tuple to a value for the target feature
        """
        raise NotImplementedError("learn")    # abstract method

