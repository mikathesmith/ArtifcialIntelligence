import numpy as np
import math
import math
import sys
import copy

# A class implementing an MLP hypothesis + steppest gradient training
class mlp:

    # When initialising the hypothesis, you can specify the number of layers and neurons per layer and
    # type of activation function in each layer.
    #
    # Input: layers - a list of dictionaries, each specifying the architecture of a layer.  The length of the list
    #                 determines the total number of layers.  The first item on the list describes the first layer,
    #                 the second the second layer, and so on.  THe last item on the list describes the last layer.
    #                 A given description of the layer, an item on the layers list, is a dictionary which needs to
    #                 contain the "neurons" key that specifies the number of neurons in the layer and the "activation"
    #                 key that is a string specifying activation function used in a given layer.  Valid string for
    #                 activation functions are: "sigmoid", "tanh", "lin", "relu".
    #        n_inputs=1 - by default this models a single-attribute input
    def __init__(self, layers, n_inputs=1):

        # Initialise the list of layer weight matrices
        self.W = list()
        # Initialise the list of layer bias vectos
        self.w0 = list()
        # Initialise the list of layer activation functions
        self.g = list()

        # For each layer...
        for l in layers:
            #...read the number of neurons and type of activation function
            neurons = l['neurons']
            activation = l['activation']

            # Create the weight matrix with random initial values.  The weight matrix is of n_inputs x neurons size
            self.W.append(np.random.normal(0.0, 1.0, (n_inputs, neurons))*0.3)
            # Create the bias vector with random initial values.  The size of the vector is same as numbe of neurons
            self.w0.append(np.random.normal(0.0, 1.0, neurons)*0.03)
            # Save the activation function string
            self.g.append(activation)
            # The number of neurons in this layer becomes the number of inputs to the next layer
            n_inputs = neurons


    # Computes the output of the MLP hypothesis
    #
    # Input: input - input data, a Nx1 vector where N is the number of input points (assuming 1-attribute input)
    #
    # Output: output - Nx1 vector of outputs h(x)
    def output(self, input):
        # For backpropagation, we need to compute and save output for each layer...but this function only returns
        # the output of the last layer - the output layer.  So this function invokes the output_compelte funciton that
        # returns a list containing otputs of all the layers...and just returns the last layer's output (index -1 means
        # the last item on the list)
        output = self.output_complete(input=input)[-1]
        return output[:,0]

    # Computes the output of each layer in MLP
    #
    # Input: input - input data, a Nx1 vector where N is the number of input points (assuming 1-attribute input)
    #
    # Output: output - a list of outputs from each layer of MLP
    def output_complete(self, input):
        # Assuming input is an array with N points...need to transoform this into an Nx1 matrix, so that
        # matrix multiplication with the first layer weight matrix works.  Since later on output just becomes
        # input to the next layer, treaing input here as output of layer 0.  The output is initialised as
        # a list
        output = [np.expand_dims(input, axis=1)]
        # Step forward through all the layers in the network
        for l in range(len(self.W)):
            # Compute the activity of the neurons in layer l from the last layers output times the
            # weight and plus the bias
            v = np.dot(output[-1], self.W[l]) + np.expand_dims(self.w0[l], axis=0)

            # Depending which activity function was specify, the computation of the layer output from
            # activity v is different
            if self.g[l] == 'sigmoid':
                out = 1.0 / (1.0 + np.exp(-v))
            elif self.g[l] == 'tanh':
                out = np.tanh(v)
            elif self.g[l] == 'lin':
                out = v
            elif self.g[l] == 'relu':
                out = v
                out[v < 0] = 0
            # Add layer l's output to the list of output - it will become the input of the next layer
            output.append(out)

        # Return the list of outputs of all the layers
        return output

    # Single epoch of steepest gradient descent backpropagation
    #
    # Input: input - input data, a Nx1 vector where N is the number of input points (assuming 1-attribute input)
    #        true-output - desired output, a Nx1 vector where  N is the number of points - each true_output[n] gives
    #                      the desired output for input[n]
    #        alpha - learning rate
    def learn(self, input, true_output, alpha):
        # How many points in the training dataset
        num_points = float(input.shape[0])

        # Compute the output of all the layers of the MLP (returned as a list).  The list has L+1 items (where L
        # is the number of layers) because the input to the network is also on that list (as layer 0)
        output = self.output_complete(input)
        # Compute the residual error by subtracting the output of the last layer from the desired output
        error = np.expand_dims(true_output,axis=1)-output[-1]
        # Compute the MSE cost
        J = np.sum(error**2)/num_points

        # Go backward from the last to the first layer and determine the parameter updates
        for l in range(len(self.W),0,-1):
            # self.W is a list of weights with 1 to L layers (L items total).  outputs is a list of outputs
            # with 0 to L layers (L+1 items total).  Hence, l-1 in self.g, self.W and self.w0 corresponds to
            # output l in outputs

            # Depending which activation function is used for layer, the derivative of the activation function
            # is different
            if self.g[l-1] == 'sigmoid':
                dout = output[l]*(1.0-output[l])
            elif self.g[l-1] == 'tanh':
                dout = (1.0+output[l])*(1.0-output[l])
            elif self.g[l-1] == 'lin':
                dout = np.ones(np.shape(output[l]))
            elif self.g[l-1] == 'relu':
                dout = np.ones(np.shape(output[l]))
                dout[output[l] < 0] = 0

            # Multiply the blame (error) times the derivative
            delta = error*dout

            # Update the weights based on steepest gradient descent rule
            deltaW = np.dot(output[l-1].transpose(),delta)/num_points
            deltaw0 = np.sum(delta,axis=0)/num_points

            # Compute the blame for the next layer
            error = np.dot(delta, self.W[l-1].transpose())

            # Update the weights and biases
            self.W[l-1] += alpha * deltaW
            self.w0[l-1] += alpha * deltaw0

        # Return MSE cost
        return J

