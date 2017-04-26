import tensorflow as tf
import numpy as np
import math
import sys
import os
import copy
from learner import learner

__author__ = "Lech Szymanski"
__email__ = "lechszym@cs.otago.ac.nz"


# A class implementing a Convolutional Neural Network (CNN) hypothesis
class cnn(learner):
    # When initialising the hypothesis, you can specify the image dimensions (height x width x colours) that is
    # the input to the CNN model, and layers

    # Input: height - height of the input image
    #        width - width of the input image
    #        colours - number of colours in the image
    #        layers - a list of dictionaries, each specifying the architecture of a layer.  The length of the list
    #                 determines the total number of layers.  The first item on the list describes the first layer,
    #                 the second the second layer, and so on.  The last item on the list describes the output layer.
    #                 A given description of the layer, an item on the layers list, is a dictionary which needs to
    #                 contain the "type" key that specifies the type of the layer.  Depending on the type, different
    #                 other parameters are expected.
    #
    #                l["type"] = "conv"  - convolutional layer, other expected keys are:
    #                                    - "height" - the height of the feature patch
    #                                    - "width" - the width of the feature patch
    #                                    - "filters" - number of filter maps generated in the layer
    #                                    - "strides" - the stride of the convolution - determines the size
    #                                                   of the output map
    #                                    - "activation" - activation function used - valid values are "sigmoid",
    #                                                                                 "tanh", "lin", "relu", "softmax".
    #
    #                l["type"] = "maxpool" - pooling layer, other expected keys are:
    #                                      - "height" - the height of the pool window
    #                                      - "width" - the width of the pool window
    #                                      - "strides" - the stride of the pooling windows - determines the size
    #                                                    of the output map
    #                l["type"] = "fc" - fully connected layer, other expected keys are:
    #                                 - "neurons" number of neruons in the layer
    #                                 - "activation" activation function - valid values are "sigmoid", "tanh", "lin",
    #                                                                      "relu", "softmax".
    #
    def __init__(self, height, width, colours, layers):
        # Save the input image size
        self.height = height
        self.width = width
        self.colours = colours

        # Map is the size of the current feature map and channels is the number of maps
        map = (height, width)
        channels = colours

        self.W = list()
        self.w0 = list()
        self.g = list()
        Winit = 0.1
        w0init = 0.1
        self.layers = copy.deepcopy(layers)

        wentFc = False

        # Walk over the layers to set up parameters
        for l, layerParams in enumerate(self.layers):
            # Convolutional layer
            if layerParams['type'] == 'conv':
                # Can't have a convolutional layer after a fully connected one
                if wentFc:
                    print(
                        "Error in layer %d! Can't put a convolutional layer after a fully connected one!" % (l+1))
                    sys.exit(-1)

                if "height" not in layerParams:
                    print(
                        "Error in layer %d! Convolutional layer requires the 'height' of the filter to be specified!" % (l+1))
                    sys.exit(-1)

                if "width" not in layerParams:
                    print(
                        "Error in layer %d! Convolutional layer requires the 'width' of the filter to be specified!" % (l+1))
                    sys.exit(-1)

                if "filters" not in layerParams:
                    print(
                        "Error in layer %d! Convolutional layer requires the 'filter' parameter specifying the number of filters!" % (l+1))
                    sys.exit(-1)

                if "strides" not in layerParams:
                    print(
                        "Error in layer %d! Convolutional layer requires the 'strides' of the convolution to be specified!" % (l+1))
                    sys.exit(-1)

                if "activation" not in layerParams:
                    print(
                        "Error in layer %d! Convolutional layer requires the 'activation' function to be specified!" % (l+1))
                    sys.exit(-1)


                height = layerParams['height']
                width = layerParams['width']
                nfilters = layerParams['filters']
                strides = layerParams['strides']
                actFunc = layerParams['activation']

                in_height = map[0]
                in_width = map[1]

                # Save parameters for the convolutional layer
                self.W.append(np.random.normal(0.0, Winit, (height, width, channels, nfilters)))
                self.w0.append(np.random.normal(0.0, w0init, nfilters))
                self.g.append(actFunc)

                # Compute the output size
                out_height = int(math.ceil(float(in_height) / float(strides)))
                out_width = int(math.ceil(float(in_width) / float(strides)))
                map = (out_height, out_width)
                channels = nfilters
            # Pooling layer
            elif layerParams['type'] == 'maxpool':
                if wentFc:
                    print(
                        "Error in layer %d! Can't put a pooling layer after a fully connected one!" % (l+1))
                    sys.exit(-1)

                if "height" not in layerParams:
                    print(
                        "Error in layer %d! Pooling layer requires the 'height' of the pooling window to be specified!" % (l+1))
                    sys.exit(-1)

                if "width" not in layerParams:
                    print(
                        "Error in layer %d! Pooling layer requires the 'width' of the pooling window to be specified!" % (l+1))
                    sys.exit(-1)

                if "strides" not in layerParams:
                    print(
                        "Error in layer %d! Pooling layer requires the 'strides' of the pooling window to be specified!" % (l+1))
                    sys.exit(-1)



                in_height = map[0]
                in_width = map[1]
                strides = layerParams['strides']

                # This layer has no trainable parameters, just compute
                # the output size...which is based on the input size and the strides
                # Number of channels remians the same
                out_height = int(math.ceil(float(in_height) / float(strides)))
                out_width = int(math.ceil(float(in_width) / float(strides)))
                map = (out_height, out_width)

            # Fully connected layer
            elif layerParams['type'] == 'fc':
                if "neurons" not in layerParams:
                    print(
                        "Error in layer %d! Fully connected layer requires the number of 'neurons' to be specified!" % (l+1))
                    sys.exit(-1)

                if "activation" not in layerParams:
                    print(
                        "Error in layer %d! Fully connected layer requires the 'activation' function to be specified!" % (l+1))
                    sys.exit(-1)


                wentFc = True
                n_outputs = layerParams['neurons']
                actFunc = layerParams['activation']
                self.g.append(actFunc)

                # Input is taken from every neuron from every map
                n_inputs = map[0] * map[1] * channels

                # Parameters for the layer
                self.W.append(np.random.normal(0.0, Winit, (n_inputs, n_outputs)))
                self.w0.append(np.random.normal(0.0, w0init, n_outputs))

                # Number of output is just the number of neurons in the layer
                map = (n_outputs, 1)
                channels = 1
            else:
                print(
                    "Error in layer %d! Unknon layer type '%s' (valid choices are 'conv', 'maxpool', 'fc')!" %
                    (l + 1, layerParams['type']))
                sys.exit(-1)

        # Print model info
        self.info()

    # Prints information about the model
    def info(self):
        print("CNN model info:")
        print("\tInput image size: %dx%dx%d" % (self.height, self.width, self.colours))

        map = (self.height, self.width)
        channels = self.colours

        for l, layerParams in enumerate(self.layers):
            if layerParams['type'] == 'conv':
                height = layerParams['height']
                width = layerParams['width']
                nfilters = layerParams['filters']
                strides = layerParams['strides']
                actFunc = layerParams['activation']
                in_height = map[0]
                in_width = map[1]

                out_height = int(math.ceil(float(in_height) / float(strides)))
                out_width = int(math.ceil(float(in_width) / float(strides)))

                map = (out_height, out_width)
                channels = nfilters

                print(
                    "\tLayer %d: conv of %d filters with %dx%d window and %d stride and %s activation; output size is %dx%dx%d "
                    % (l + 1, nfilters, height, width, strides, actFunc, out_height, out_width, channels))

            elif layerParams['type'] == 'maxpool':
                height = layerParams['height']
                width = layerParams['width']
                strides = layerParams['strides']

                in_height = map[0]
                in_width = map[1]

                out_height = int(math.ceil(float(in_height) / float(strides)))
                out_width = int(math.ceil(float(in_width) / float(strides)))

                print("\tLayer %d: pooling over %dx%d window and %d stride; output size is %dx%dx%d "
                      % (l + 1, height, width, strides, out_height, out_width, channels))

                map = (out_height, out_width)

            elif layerParams['type'] == 'fc':
                n_outputs = layerParams['neurons']
                actFunc = layerParams['activation']

                n_inputs = map[0] * map[1] * channels

                print("\tLayer %d: fully connected taking %d inputs and giving %d outputs with %s activation"
                      % (l + 1, n_inputs, n_outputs, actFunc))

                map = (n_outputs, 1)
                channels = 1
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

        # The size of the input map (size of the input image) and the number of channels (number of colours)
        map = (self.height, self.width)
        channels = self.colours

        # Build the graph
        with g.as_default():
            # Create a placeholder value for inpupt - input data is fed here
            g_x = tf.placeholder("float", [None, self.width * self.height * self.colours])

            # Initialise the lists for graph references to layer variables
            g_W = list()
            g_w0 = list()

            # Initialise previous type
            prevType = self.layers[0]['type']
            if prevType == 'fc':
                # If starting with fully connected, then input is in vector form
                g_y = g_x
            else:
                # If starting with a convolutional layer, then reshape NxM vector to
                # N x height x width x colours
                g_y = tf.reshape(g_x, shape=[-1, self.height, self.width, self.colours])

            # Go through all the layers
            j = 0
            for l, layerParams in enumerate(self.layers):

                # If building the graph of the convolutional layer...
                if layerParams['type'] == 'conv':
                    # ...get other conv layer parameters
                    nfilters = layerParams['filters']
                    strides = layerParams['strides']
                    actFunc = layerParams['activation']
                    padding = 'SAME'

                    # Get the size of the map over which the convolution is done
                    in_height = map[0]
                    in_width = map[1]

                    # Create the weight and bias variables for the layer
                    W = tf.Variable(self.W[j], name='W%d' % l, dtype='float32')
                    w0 = tf.Variable(self.w0[j], name='w0%d' % l, dtype='float32')
                    g_W.append(W)
                    g_w0.append(w0)

                    # Compute convolution output
                    g_v = tf.nn.conv2d(g_y, g_W[-1], strides=[1, strides, strides, 1], padding=padding)
                    # Add the bias
                    g_v = tf.nn.bias_add(g_v, g_w0[-1])

                    # Pass through activation function
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
                        print("Error in layer %d! Unrecognised activation function '%s' (valid choices are 'sigmoid', 'tanh', 'lin', 'relu', 'softmax')!" %
                              (l+1, actFunc))
                        sys.exit(-1)

                    # Compute the size of the output map of this layer
                    out_height = int(math.ceil(float(in_height) / float(strides)))
                    out_width = int(math.ceil(float(in_width) / float(strides)))

                    map = (out_height, out_width)
                    channels = nfilters
                    j += 1

                # If building the graph of the pooling layer...
                elif layerParams['type'] == 'maxpool':
                    # ... get the parameters
                    height = layerParams['height']
                    width = layerParams['width']
                    strides = layerParams['strides']
                    padding = 'SAME'

                    # Pooling has no variables, just an operation that selects one winner out of the pooling window
                    g_y = tf.nn.max_pool(g_y, ksize=[1, height, width, 1], strides=[1, strides, strides, 1],
                                         padding=padding)
                    # The size of the output map depends on the strides
                    _, out_height, out_width, _ = g_y._shape
                    map = (out_height.value, out_width.value)

                # If building the graph of a fully connected layer...
                elif layerParams['type'] == 'fc':
                    # ... get the parameters
                    n_outputs = layerParams['neurons']
                    actFunc = layerParams['activation']

                    # Fully connected takes input from all neurons, so it's the map height times its width and times
                    # the number of channels that forms the input size
                    n_inputs = map[0] * map[1] * channels

                    # Create weight matrix and bias vector variables in the tensorflow graph
                    W = tf.Variable(self.W[j], name='W%d' % l,
                                    dtype='float32')
                    w0 = tf.Variable(self.w0[j], name='w0%d' % l,
                                     dtype='float32')
                    g_W.append(W)
                    g_w0.append(w0)

                    map = (n_outputs, 1)
                    channels = 1

                    # If the previous layer was not a fully connected one, then reshape the height x width x channels
                    # tensor that is an output of a conv or pooling layer into a vector
                    if prevType != 'fc':
                        g_y = tf.reshape(g_y, [-1, n_inputs])

                    # Compute activity of the layer
                    g_v = tf.add(tf.matmul(g_y, g_W[-1]), g_w0[-1])

                    # Pass through activation function
                    if actFunc == 'relu':
                        g_y = tf.nn.relu(g_v)
                    elif actFunc == 'tanh':
                        g_y = tf.nn.tanh(g_v)
                    elif actFunc == 'sigmoid':
                        y = tf.nn.sigmoid(g_v)
                    elif actFunc == 'lin':
                        g_y = g_v
                    elif actFunc == 'softmax':
                        g_y = tf.nn.softmax(g_v)
                    else:
                        print("Error in layer %d! Unrecognised activation function '%s' (valid choices are 'sigmoid', 'tanh', 'lin', 'relu', 'softmax')!" %
                              (l+1, actFunc))
                        sys.exit(-1)
                    j += 1

                else:
                    print(
                        "Error in layer %d! Unknon layer type '%s' (valid choices are 'conv', 'maxpool', 'fc')!" %
                        (l + 1, layerParams['type']))
                    sys.exit(-1)

                # Save the previous layer's type
                prevType = layerParams['type']

        return g, g_y, g_v, g_x, g_W, g_w0
