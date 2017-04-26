import numpy as np
import sys
import os
import tensorflow as tf
from tensorflow.contrib import rnn
from learner import learner

__author__ = "Lech Szymanski"
__email__ = "lechszym@cs.otago.ac.nz"

# A class implementing a Simple Recurrent Network (SRN) hypothesis
class srn(learner):

    # This model process an image not as a single input vector, but as a sequence of subvectors that
    # make up the image.  When initialising the hypothesis,
    # you can specify the number of inputs into the model, layers and neurons per
    # layer and type of activation function in each layer.
    #
    # Input: n_inputs_image - number of attributes in the input of an image
    #        n_inputs_srn - size of the subvector processed at a time.  This value must be such that n_inputs_image
    #                       is divisible by n_inputs_srn.
    #        layers - a list of dictionaries, each specifying the architecture of a layer.   The length of the list
    #                 must be 2, as only one hidden and one output layer is allowed in this model.
    #                 The first item on the list describes the hidden layer, the second item on the list describes
    #                 the output layer.  A given description of the layer, an item on the layers list, is a dictionary
    #                 which needs to contain the "neurons" key that specifies the number of neurons in the layer and
    #                 the "activation" key that is a string specifying activation function used in a given layer.
    #                 Valid string for activation functions are: "sigmoid", "tanh", "lin", "relu", "softmax".
    #
    def __init__(self, n_inputs_image, n_inputs_srn, layers):

        # Check that model specified correctly...

        # Model can have only 2 layers
        if len(layers)!=2:
            print("Error! Expecting two layers and got %d." % len(layers))
            sys.exit(-1)

        # The SRN input must be smaller than the entire image vector and must divide it evenly
        if n_inputs_image %  n_inputs_srn != 0:
            print("Error! The n_inputs_srn=%d does not divide n_inputs_image=%d evenly." % (n_inputs_srn, n_inputs_image))
            sys.exit(-1)

        #Check whether all parameters in each layer were given
        for l, layerParams in enumerate(layers):
            if "neurons" not in layerParams:
                print(
                    "Error in layer %d! Layer requires the number of 'neurons' to be specified!" % (l + 1))
                sys.exit(-1)

            if "activation" not in layerParams:
                print(
                    "Error in layer %d! Layer requires must have its 'activation' function specified!" % (l + 1))
                sys.exit(-1)

        # Save model parameters
        self.n_inputs = n_inputs_image
        self.n_hidden = layers[0]['neurons']
        # Compute number of sequences from the size of the SRN input
        self.n_steps = n_inputs_image//n_inputs_srn
        self.n_outputs = layers[1]['neurons']

        # Initialise the list of layer bias vectors
        self.W = list()
        self.w0 = list()

        # Create weights for the input to hidden layer
        self.W.append(np.random.normal(0.0, 0.1, (self.n_inputs//self.n_steps+self.n_hidden, self.n_hidden)))
        self.w0.append(np.random.normal(0.0, 0.1, self.n_hidden))

        # Create weights for the input to hidden layer
        #self.W.append(np.random.normal(0.0, 0.1, (self.n_hidden, self.n_outputs)))
        #self.w0.append(np.random.normal(0.0, 0.1, self.n_outputs))

        # Create weights for the hidden to hidden layer
        self.W.append(np.random.normal(0.0, 0.1, (self.n_hidden, self.n_outputs)))
        self.w0.append(np.random.normal(0.0, 0.1, self.n_outputs))


        # Initialise the list of layer activation functions
        self.g = list()

        for l in layers:
            # ...read the number of neurons and type of activation function
            neurons = l['neurons']
            activation = l['activation']

            # Save the activation function string
            self.g.append(activation)

        self.info()

    def info(self):
        print("SNR model info:")
        print("\tInput size: %d (%d consecutive vectors from a %d-pixel image)" % (self.n_inputs//self.n_steps, self.n_steps, self.n_inputs))
        print("\tHidden neurons: %d" % self.n_hidden)
        for l in range(len(self.W)):
            n_inputs, n_outputs = np.shape(self.W[l])
            if l==0:
                print("\tLayer %d: fully connected taking %d+%d inputs (%d from model input and %d from the context) and giving %d outputs with %s activation"
                      % (l + 1, self.n_inputs//self.n_steps, self.n_hidden, self.n_inputs//self.n_steps, self.n_hidden, n_outputs, self.g[l]))
            else:
                print("\tLayer %d: fully connected taking %d inputs and giving %d outputs with %s activation"
                      % (l + 1, n_inputs, n_outputs, self.g[l]))
        print("\tOutput size: %d" % self.n_outputs)

    def tensorflow_graph(self):
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
        g = tf.Graph()

        g_W = list()
        g_w0 = list()

        with g.as_default():
            g_x = tf.placeholder("float", [None, self.n_inputs])

            g_v = tf.reshape(g_x, [-1, self.n_steps, self.n_inputs//self.n_steps])

            # Prepare data shape to match `rnn` function requirements
            # Current data input shape: (batch_size, n_steps, n_input)
            # Required shape: 'n_steps' tensors list of shape (batch_size, n_input)

            # Permuting batch_size and n_steps
            g_v = tf.transpose(g_v, [1, 0, 2])
            # Reshaping to (n_steps*batch_size, n_input)
            g_v = tf.reshape(g_v, [-1, self.n_inputs//self.n_steps])
            # Split to get a list of 'n_steps' tensors of shape (batch_size, n_input)
            g_v = tf.split(g_v, self.n_steps, 0)


            # Define an RNN cell with tensorflow
            rnn_cell = rnn.BasicRNNCell(self.n_hidden)

            # Get RNN cell output
            g_v, states = rnn.static_rnn(rnn_cell, g_v, dtype=tf.float32)

            # Add the RNN output to the list of tensorflow references
            [W, w0] = tf.global_variables()
            g_W.append(W)
            g_w0.append(w0)

            # Create variables for hidden to output layer mappoing
            W = tf.Variable(self.W[-1], name='W_out', dtype='float32')
            w0 = tf.Variable(self.w0[-1], name='w0_out', dtype='float32')
            g_W.append(W)
            g_w0.append(w0)

            # Activation, using rnn inner loop last output
            g_v = tf.matmul(g_v[-1], g_W[-1]) + g_w0[-1]

            actFunc = self.g[-1]
            if actFunc == 'relu':
                g_y = tf.nn.relu(g_v)
            elif actFunc == 'tanh':
                g_y = tf.nn.tanh(g_v)
            elif actFunc == 'sigmoid':
                g_y = tf.nn.sigmoid(g_v)
            elif actFunc == 'softmax':
                g_y = tf.nn.softmax(g_v)
            elif actFunc == 'lin':
                g_y = g_v
            else:
                print("Error! Unknown activation function")
                sys.exit(-1)

        return g, g_y, g_v, g_x, g_W, g_w0
