# learnNoInputs.py - Learning ignoring all input features
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from learnProblem import Learner, Data_set
import math, random

selections = ["median", "mean", "Laplace"]

def point_prediction(target, training_data,
                     selection="mean" ):
    """makes a point prediction for a set of training data.
    target provides the target
    training_data provides the training data to use (often a subset of train).
    selection specifies what statistic of the data to use as the evaluation.
    to_optimize provides a criteria to optimize (used to guess selection)
    """
    assert len(training_data)>0
    if selection == "median":
        counts,total = target_counts(target,training_data)
        middle = total/2
        cumulative = 0
        for val,num in sorted(counts.items()):
            cumulative += num
            if cumulative > middle:
                break  # exit loop with val as the median
    elif selection == "mean":
        val = mean((target(e) for e in training_data))
    elif selection == "Laplace":
        val = mean((target(e) for e in training_data),len(target.frange),1)
    elif selection == "mode":
        raise NotImplementedError("mode")
    else:
        raise RuntimeError("Not valid selection: "+str(selection))
    fun = lambda x: val
    fun.__doc__ = str(val)
    return fun

def mean(enum,count=0,sum=0):
    """returns the mean of enumeration enum, 
       count and sum are initial counts and the initial sum.
       This works for enumerations, even where len() is not defined"""
    for e in enum:
        count += 1
        sum += e
    return sum/count

def target_counts(target, data_subset):
    """returns a value:count dictionary of the count of the number of
    times target has this value in data_subset, and the number of examples.
    """
    counts = {val:0 for val in target.frange}
    total = 0
    for instance in data_subset:
        total += 1
        counts[target(instance)] += 1
    return counts, total

class Data_set_random(Data_set):
    """A data set of a {0,1} feature generated randomly given a probability"""
    def __init__(self, prob, train_size, test_size=100):
        """a data set of with train_size training examples,
        test_size test examples
        where each examples in generated where prob i the probability of 1
        """
        train = [[1] if random.random()<prob else [0] for i in range(train_size)]
        test =  [[1] if random.random()<prob else [0] for i in range(test_size)]
        Data_set.__init__(self, train, test, target_index=0)
        
def test_no_inputs():
    num_samples = 1000  #number of runs to average over
    test_size = 100     # number of test examples for each prediction
    for train_size in [1,2,3,4,5,10,20,100,1000]:
        total_error = {(select,crit):0
                       for select in selections
                       for crit in Data_set.evaluation_criteria}
        for sample in range(num_samples):   # average over num_samples
            p = random.random()
            data = Data_set_random(p, train_size, test_size)
            for select in selections:
                prediction = point_prediction(data.target, data.train, selection=select)
                for ecrit in Data_set.evaluation_criteria:
                    test_error = data.evaluate_dataset(data.test,prediction,ecrit)
                    total_error[(select,ecrit)] += test_error
        print("For training size",train_size,":")
        for ecrit in Data_set.evaluation_criteria:
            print("    Evaluated according to",ecrit,":")
            for select in selections:
                print("        Average error of",select,"is",
                      total_error[(select,ecrit)]/num_samples)

if __name__ == "__main__":
    test_no_inputs()
        
