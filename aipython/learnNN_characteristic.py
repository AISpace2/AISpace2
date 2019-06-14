# learnNN.py - Neural Network Learning
# Python 3 code. Full documentation at http://artint.info/code/python/code.pdf

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2016.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from learnProblem import Learner, Data_set, Data_from_file
from learnLinear import sigmoid, one
import random, math

class Layer(object):
    def __init__(self,nn,num_outputs=None):
        """Given a list of inputs, outputs will produce a list of length num_outputs.
        nn is the neural network this is part of
        num outputs is the number of outputs for this layer.
        """
        self.nn = nn
        self.num_inputs = nn.num_outputs # output of nn is the input to this layer
        if num_outputs:
            self.num_outputs = num_outputs
        else:
            self.num_outputs = nn.num_outputs  # same as the inputs

    def output_values(self,input_values):
        """Return the outputs for this layer for the given input values.
        input_values is a list of the inputs to this layer (of length num_inputs)
        returns a list of length self.num_outputs
        """
        raise NotImplementedError("output_values")    # abstract method

    def backprop(self,errors):
        """Backpropagate the errors on the outputs, return the errors on the inputs.
        errors is a list of errors for the outputs (of length self.num_outputs).
        Return the errors for the inputs to this layer (of length self.num_inputs).
        You can assume that this is only called after corresponding output_values, 
           and it can remember information information required for the backpropagation.
        """
        raise NotImplementedError("backprop")    # abstract method

class Linear_complete_layer(Layer):
    """a completely connected layer"""
    def __init__(self, nn, num_outputs, max_init=0.2):
        """A completely connected linear layer.
        nn is a neural network that the inputs come from
        num_outputs is the number of outputs
        max_init is the maximum value for random initialization of parameters
        """
        Layer.__init__(self, nn, num_outputs)
        # self.weights[o][i] is the weight between input i and output o
        self.weights = [[random.uniform(-max_init, max_init)
                          for inf in range(self.num_inputs+1)]
                        for outf in range(self.num_outputs)]

    def output_values(self,input_values):
        """Returns the outputs for the input values.
        It remembers the values for the backprop.

        Note in self.weights there is a weight list for every output,
        so wts in self.weights effectively loops over the outputs.
        """
        self.inputs = input_values + [1]
        return [sum(w*val for (w,val) in zip(wts,self.inputs))
                    for wts in self.weights]

    def backprop(self,errors):
        """Backpropagate the errors, updating the weights and returning the error in its inputs.
        """
        input_errors = [0]*(self.num_inputs+1)
        for out in range(self.num_outputs):
            for inp in range(self.num_inputs+1):
                input_errors[inp] += self.weights[out][inp] * errors[out]
                self.weights[out][inp] += self.nn.learning_rate * self.inputs[inp] * errors[out]
        return input_errors[:-1]   # remove the error for the "1"
                
class Sigmoid_layer(Layer):
    """sigmoids of the inputs.
    The number of outputs is equal to the number of inputs. 
    Each output is the sigmoid of its corresponding input.
    """
    def __init__(self, nn):
        Layer.__init__(self, nn)

    def output_values(self,input_values):
        """Returns the outputs for the input values.
        It remembers the output values for the backprop.
        """
        self.outputs= [sigmoid(inp) for inp in input_values]
        return self.outputs

    def backprop(self,errors):
        """Returns the derivative of the errors"""
        return [e*out*(1-out) for e,out in zip(errors, self.outputs)]

class ReLU_layer(Layer):
    """Rectified linear unit (ReLU) f(z) = max(0, z).
    The number of outputs is equal to the number of inputs. 
    """
    def __init__(self, nn):
        Layer.__init__(self, nn)

    def output_values(self,input_values):
        """Returns the outputs for the input values.
        It remembers the input values for the backprop.
        """
        self.input_values = input_values
        self.outputs= [max(0,inp) for inp in input_values]
        return self.outputs

    def backprop(self,errors):
        """Returns the derivative of the errors"""
        return [e if inp>0 else 0 for e,inp in zip(errors, self.input_values)]
    
class NN(Learner):
    def __init__(self, dataset, learning_rate=0.1):
        self.dataset = dataset
        self.learning_rate = learning_rate
        self.input_features = dataset.input_features
        self.num_outputs = len(self.input_features)
        self.layers = []

    def add_layer(self,layer):
        """add a layer to the network.
        Each layer gets values from the previous layer.
        """
        self.layers.append(layer)
        self.num_outputs = layer.num_outputs

    def predictor(self,ex):
        """Predicts the value of the first output feature for example ex.
        """
        values = [f(ex) for f in self.input_features]
        for layer in self.layers:
            values = layer.output_values(values)
        return values

    def predictor_string(self):
        return "not implemented"


    def learn(self,num_iter):
        """Learns parameters for a neural network using stochastic gradient decent.
        num_iter is the number of iterations
        """
        for i in range(num_iter):
            for e in random.sample(self.dataset.train,len(self.dataset.train)):
                # compute all outputs
                values = [f(e) for f in self.input_features]
                for layer in self.layers:
                    values = layer.output_values(values)
                # backpropagate
                errors = characteristic_error(self.dataset.target(e),values)
                for layer in reversed(self.layers):
                    errors = layer.backprop(errors)

def characteristic_error(target,prediction):
        return [1-prediction[i] if target==i else -prediction[i]
                        for i in range(len(prediction))]
    
def sum_squares_error(observed,predicted):
        """Returns the errors for each of the target features.
        """
        return [obsd-pred for obsd,pred in zip(observed,predicted)]


data = Data_from_file('data/training.txt', target_index=-1)
#data = Data_from_file('data/mail_reading_consis.csv', target_index=-1)
#data = Data_from_file('data/SPECT.csv',  prob_test=0.5, target_index=0)
#data = Data_from_file('data/holiday.csv', target_index=-1) #, num_train=19)
nn1 = NN(data)
nn1.add_layer(Linear_complete_layer(nn1,50))
nn1.add_layer(Sigmoid_layer(nn1))  # comment this or the next
# nn1.add_layer(ReLU_layer(nn1)) 
nn1.add_layer(Linear_complete_layer(nn1,10))
nn1.add_layer(Sigmoid_layer(nn1))
nn1.learning_rate=0.1
#nn1.learn(100)

from learnLinear import plot_steps
import time
start_time = time.perf_counter()
plot_steps(learner = nn1, data = data, num_steps=100, criterion="characteristic_ss")
#for eg in data.train:
#    print(eg,nn1.predictor(eg))
end_time = time.perf_counter()
print("Time:", end_time - start_time)

