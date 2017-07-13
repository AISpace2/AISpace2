# learnDT.py - Learning a binary decision tree
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from learnProblem import Learner, error_example
from learnNoInputs import point_prediction, target_counts, selections
import math

class DT_learner(Learner):
    def __init__(self,
                 dataset,
                 to_optimize="sum-of-squares",
                 leaf_selection="mean",   # what to use for point prediction at leaves
                 train=None,              # used for cross validation
                 min_number_examples=10):
        self.dataset = dataset
        self.target = dataset.target
        self.to_optimize = to_optimize
        self.leaf_selection = leaf_selection
        self.min_number_examples = min_number_examples
        if train is None:
            self.train = self.dataset.train
        else:
            self.train = train

    def learn(self):
        return self.learn_tree(self.dataset.input_features, self.train)
        
    def learn_tree(self, input_features, data_subset):
        """returns a decision tree
        for input_features is a set of possible conditions
        data_subset is a subset of the data used to build this (sub)tree

        where a decision tree is a function that takes an example and
        makes a prediction on the target feature
        """
        if (input_features and len(data_subset) >= self.min_number_examples):
            first_target_val = self.target(data_subset[0])
            allagree = all(self.target(inst)==first_target_val for inst in data_subset)
            if not allagree:
                split, partn = self.select_split(input_features, data_subset)
                if split: # the split succeeded in splitting the data
                    false_examples, true_examples = partn
                    rem_features = [fe for fe in input_features if fe != split]
                    self.display(2,"Splitting on",split.__doc__,"with examples split",
                                   len(true_examples),":",len(false_examples))
                    true_tree = self.learn_tree(rem_features,true_examples)
                    false_tree =  self.learn_tree(rem_features,false_examples)
                    def fun(e):
                        if split(e):
                            return true_tree(e)
                        else:
                            return false_tree(e)
                    #fun = lambda e: true_tree(e) if split(e) else false_tree(e)
                    fun.__doc__ = ("if "+split.__doc__+" then ("+true_tree.__doc__+
                                   ") else ("+false_tree.__doc__+")")
                    return fun
        # don't expand the trees but return a point prediction
        return point_prediction(self.target, data_subset, selection=self.leaf_selection)
        
    def select_split(self, input_features, data_subset):
        """finds best feature to split on.

        input_features is a non-empty list of features.
        returns feature, partition
        where feature is an input feature with the smallest error as
              judged by to_optimize or
              feature==None if there are no splits that improve the error
        partition is a pair (false_examples, true_examples) if feature is not None
        """
        best_feat = None # best feature
        # best_error = float("inf")  # infinity - more than any error
        best_error = training_error(self.dataset, data_subset, self.to_optimize)
        best_partition = None
        for feat in input_features:
            false_examples, true_examples = partition(data_subset,feat)
            if false_examples and true_examples:  #both partitons are non-empty
                err = (training_error(self.dataset,false_examples,self.to_optimize)
                       + training_error(self.dataset,true_examples,self.to_optimize))
                self.display(3,"   split on",feat.__doc__,"has err=",err,
                          "splits into",len(true_examples),":",len(false_examples))
                if err < best_error:
                    best_feat = feat
                    best_error=err
                    best_partition = false_examples, true_examples
        self.display(3,"best split is on",best_feat.__doc__,
                               "with err=",best_error)
        return best_feat, best_partition

def partition(data_subset,feature):
    """partitions the data_subset by the feature"""
    true_examples = []
    false_examples = []
    for example in data_subset:
        if feature(example):
            true_examples.append(example)
        else:
            false_examples.append(example)
    return false_examples, true_examples


def training_error(dataset, data_subset, to_optimize):
    """returns training error for dataset on to_optimize.
    This assumes that we choose the best value for the optimization
    criteria for dataset according to point_prediction
    """
    select_dict = {"sum-of-squares":"mean", "sum_absolute":"median",
                       "logloss":"Laplace"}  # arbitrary mapping. Perhaps wrong.
    selection = select_dict[to_optimize]
    predictor = point_prediction(dataset.target, data_subset, selection=selection)
    error = sum(error_example(predictor(example),
                               dataset.target(example),
                               to_optimize)
                 for example in data_subset)
    return error

from learnProblem import Data_set, Data_from_file

def test(data):
    """Prints errors and the trees for various evaluation criteria and ways to select leaves.
    """
    for crit in Data_set.evaluation_criteria:
        for leaf in selections:
            tree = DT_learner(data, to_optimize=crit, leaf_selection=leaf).learn()
            print("For",crit,"using",leaf,"at leaves, tree built is:",tree.__doc__)
            if data.test:
                for ecrit in Data_set.evaluation_criteria:
                    test_error = data.evaluate_dataset(data.test, tree, ecrit)
                    print("    Average error for", ecrit,"using",leaf, "at leaves is", test_error)
    
if __name__ == "__main__":
    #print("carbool.csv"); test(data = Data_from_file('data/carbool.csv', target_index=-1))
    # print("SPECT.csv"); test(data = Data_from_file('data/SPECT.csv', target_index=0))
    print("mail_reading.csv"); test(data = Data_from_file('data/mail_reading.csv', target_index=-1))
    # print("holiday.csv"); test(data = Data_from_file('data/holiday.csv', num_train=19, target_index=-1))
    
