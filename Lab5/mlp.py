import tensorflow as tf
import numpy as np
import os
import sys
from learner import learner

__author__ = "Lech Szymanski"
__email__ = "lechszym@cs.otago.ac.nz"

# A class implementing a Multi-layer Perceptron (MLP) hypothesis
class mlp(learner):

    # When initialising the hypothesis, you can specify the number of inputs into the model, layers and neurons per
    # layer and type of activation function in each layer.
    #
    # Input: n_inputs - number of attributes in a single input
    #        layers - a list of dictionaries, each specifying the architecture of a layer.  The length of the list
    #                 determines the total number of layers.  The first item on the list describes the first layer,
    #                 the second the second layer, and so on.  Tee last item on the list describes the output layer.
    #                 A given description of the layer, an item on the layers list, is a dictionary which needs to
    #                 contain the "neurons" key that specifies the number of neurons in the layer and the "activation"
    #                 key that is a string specifying activation function used in a given layer.  Valid string for
    #                 activation functions are: "sigmoid", "tanh", "lin", "relu", "softmax".
    #
    def __init__(self, n_inputs, layers):
        # Save the number of attribute in the input
        self.n_inputs = n_inputs

        # Initialise the list of layer weight matrices
        self.W = list()
        # Initialise the list of layer bias vectors
        self.w0 = list()
        # Initialise the list of layer activation functions
        self.g = list()

        # For each layer...
        for l, layerParams in enumerate(layers):
            if "neurons" not in layerParams:
                print(
                    "Error in layer %d! Layer requires the number of 'neurons' to be specified!" % (l + 1))
                sys.exit(-1)

            if "activation" not in layerParams:
                print(
                    "Error in layer %d! Layer requires must have its 'activation' function specified!" % (l + 1))
                sys.exit(-1)


            # ...read the number of neurons and type of activation function
            neurons = layerParams['neurons']
            activation = layerParams['activation']

            # Create the weight matrix with random initial values.  The weight matrix is of n_inputs x neurons size
            self.W.append(np.random.normal(0.0, 0.1, (n_inputs, neurons)))
            # Create the bias vector with random initial values.  The size of the vector is same as number of neurons
            self.w0.append(np.random.normal(0.0, 0.1, neurons))
            # Save the activation function string
            self.g.append(activation)
            # The number of neurons in this layer becomes the number of inputs to the next layer
            n_inputs = neurons

        self.info()

    # Prints information about the model
    def info(self):
        print("MLP model info:")
        print("\tInput size: %d" % self.n_inputs)
        for l in range(len(self.W)):
            n_inputs, n_outputs = np.shape(self.W[l])
            print("\tLayer %d: fully connected taking %d inputs and giving %d outputs with %s activation"
                  % (l + 1, n_inputs, n_outputs, self.g[l]))
        print("\tOutput size: %d" % np.shape(self.W[-1])[1])

    # The function implementing the MLP model as a tensorflow graph
    #
    # Returns:  g - the reference to the graph
    #           g_y - reference to the model's output in the graph
    #           g_v - reference to activity of the model's output
    #           g_x - reference to the graph's input placeholder
    #           g_W - list of references to graph's weight matrices of different layers
    #           g_w0 - list of refrences to graph's bias vectors of different layers
    def tensorflow_graph(self):

        # Disable tensorflow warnings
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

        # Create a new tensorflow graph
        g = tf.Graph()

        with g.as_default():
            # Create a placeholder value for inpupt - input data is fed here
            g_x = tf.placeholder("float", [None, self.n_inputs])

            # Initialise the lists for graph references to layer variables
            g_W = list()
            g_w0 = list()

            # The output of layer 0 is the input
            g_y = g_x
            # Create MLP layers in the graph
            for l in range(len(self.W)):
                # Create a tensorflow variable for layer l weight matrix
                W = tf.Variable(self.W[l], name='W%d' % l, dtype='float32')
                # Create a tensorflow variable for layer l bias vector
                w0 = tf.Variable(self.w0[l], name='w0%d' % l, dtype='float32')
                # Append references to layer l parameters to g_W and g_w0 lists
                g_W.append(W)
                g_w0.append(w0)

                # Create tensorflow graph that computes activity from previous layer's output and
                # this layer's weight matrix and bias
                g_v = tf.add(tf.matmul(g_y, g_W[-1]), g_w0[-1], name='v%d' % l)

                # Apply an activation function
                if self.g[l] == 'sigmoid':
                    g_y = tf.nn.sigmoid(g_v)
                elif self.g[l] == 'tanh':
                    g_y = tf.nn.tanh(g_v)
                elif self.g[l] == 'lin':
                    g_y = g_v
                elif self.g[l] == 'relu':
                    g_y = tf.nn.relu(g_v)
                elif self.g[l] == 'softmax':
                    g_y = tf.nn.softmax(g_v)
                else:
                    print(
                        "Error! Unrecognised activation function '%s' (valid choices are 'sigmoid', 'tanh', 'lin', 'relu', 'softmax')!" %
                        self.g[l])

            return g, g_y, g_v, g_x, g_W, g_w0
