import tensorflow as tf
import numpy as np
import os
import time
import math
from mlp import mlp

__author__ = "Lech Szymanski"
__email__ = "lechszym@cs.otago.ac.nz"

# A class implementing a Deep Belief Net (DBN) hypothesis
class dbn(mlp):

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
    #                 activation functions are: "sigmoid", "tanh", "lin", "relu", "softmax"...though for DBN
    #                 it's best to stick with sigmoids for hidden layers
    #
    def __init__(self, n_inputs, layers):
        self.wgen = list()

        # For each layer, initialise generative bias (for information travelling backwards)
        neurons = n_inputs
        for l, layerParams in enumerate(layers):
            self.wgen.append(np.random.normal(0.0, 0.01, (neurons)))
            neurons = layerParams['neurons']

        # Initialise the reminder of the model (using MLPs constructor)
        super().__init__(n_inputs, layers)

    # Prints information about the model
    def info(self):
        print("DBN model info:")
        print("\tInput size: %d" % self.n_inputs)
        for l in range(len(self.W)):
            n_inputs, n_outputs = np.shape(self.W[l])
            print("\tLayer %d: fully connected taking %d inputs and giving %d outputs with %s activation"
                  % (l + 1, n_inputs, n_outputs, self.g[l]))
        print("\tOutput size: %d" % np.shape(self.W[-1])[1])

    # Runs unsupervised training of the hidden layers, layer by layer
    #
    # Input: input - an NxM input data matrix, where N is the number of points and M is number of attributes per point
    #        alpha - learning rate
    #        num_epochs - number of epochs to train for
    #        batch_size (optional) - mini-batch size.  Mini-batch training speeds up training a bit - leaving this
    #                                default value of 128 should be fine.
    def learn_unsupervised(self, input, alpha, num_epochs, batch_size=128):

        num_points = input.shape[0]

        # Determine the number of min-batches in the dataset
        num_batches = num_points // batch_size
        if num_batches < 1:
            num_batches = 1
            batch_size = num_points

        # Parameters for RBM training
        epsilon = alpha/batch_size
        weightcost = 0.0002
        initialmomentum = 0.5
        finalmomentum = 0.9

        xpos = input
        # Train layer by layer
        for l in range(len(self.W)-1):
            # Will train layer l
            print("\nUnsupervised training of layer %d..." % (l+1))

            if l>0:
                # For the 2nd hidden layer and ones following the input is the
                # output of the previous layer.  Create a sub-graph to compute the output
                # of the layer before
                Wsaved = list(self.W)
                self.W = self.W[0:l]
                g, g_yhat, g_vhat, g_x, g_W, g_w0 = self.tensorflow_graph()
                self.W = list(Wsaved)

                with tf.Session(graph=g) as sess:
                    # Initialise the graph
                    sess.run(tf.global_variables_initializer())
                    # Compute the output of layer l-1
                    xpos = sess.run(g_yhat, feed_dict={g_x: input})

            # Now create a subgraph for the RBM, with visible units being the neurons of layer l-1, clamped
            # to produce otput as computed above, and the neurons of layer l constituting the hidden neurons of the
            # RBM
            Wsaved = list(self.W)
            self.W = self.W[0:(l+1)]
            g, g_yhat, g_vhat, g_x, g_W, g_w0 = self.tensorflow_graph()
            self.W = list(Wsaved)

            # Augment the tensorflow graph
            with g.as_default():

                # Positive phase input is the output of layer l-1
                g_xpos = tf.placeholder("float", [None, xpos.shape[1]])
                # Compute positive phase state
                g_ypos = tf.nn.sigmoid(tf.add(tf.matmul(g_xpos, g_W[-1]), g_w0[-1]), 'y_pos')

                # Fetch generative weights
                g_wgen = tf.Variable(self.wgen[l], name='wgen%d' % l, dtype='float32')

                # Create variables for parameter changes
                momentum = tf.Variable(initial_value=initialmomentum)
                W_inc = tf.Variable(tf.zeros(self.W[l].shape))
                b_hid_inc = tf.Variable(tf.zeros(self.w0[l].shape))
                b_vis_inc = tf.Variable(tf.zeros(self.wgen[l].shape))

                # Compute the state of the hidden layer
                r = tf.random_uniform(tf.shape(g_ypos), minval=0, maxval=1)
                s = tf.to_float(tf.greater_equal(g_ypos, r, name=None))

                # Compute the negative phase input
                g_xneg = tf.nn.sigmoid(tf.add(tf.matmul(s, tf.transpose(g_W[-1])), g_wgen))
                # Compute the output from the negative phase input
                g_yneg = tf.nn.sigmoid(tf.add(tf.matmul(g_xneg, g_W[-1]), g_w0[-1]))

                # The cost is the difference between positive phase (the true) and negative phase (imagined) input
                g_cost = tf.reduce_sum(tf.reduce_sum(tf.pow(tf.subtract(g_xneg, g_xpos),2),1))

                # Compute weight updates
                W_pos = tf.matmul(tf.transpose(g_xpos), g_ypos)
                b_hid_pos = tf.reduce_sum(g_ypos, 0)
                b_vis_pos = tf.reduce_sum(g_xpos, 0)

                W_neg = tf.matmul(tf.transpose(g_xneg), g_yneg)
                b_hid_neg = tf.reduce_sum(g_yneg, 0)
                b_vis_neg = tf.reduce_sum(g_xneg, 0)

                W_delta = tf.subtract(W_pos, W_neg)
                b_hid_delta = tf.subtract(b_hid_pos,b_hid_neg)
                b_vis_delta = tf.subtract(b_vis_pos,b_vis_neg)

                W_inc_updated = W_inc.assign(momentum * W_inc + W_delta * epsilon)
                b_hid_inc_updated = b_hid_inc.assign(momentum * b_hid_inc + b_hid_delta * epsilon)
                b_vis_inc_updated = b_vis_inc.assign(momentum * b_vis_inc + b_vis_delta * epsilon)

                # Apply weight updtes
                W_update = g_W[-1].assign((1 - weightcost) * g_W[-1] + W_inc_updated)
                b_hid_update = g_w0[-1].assign(g_w0[-1] + b_hid_inc_updated)
                b_vis_update = g_wgen.assign(g_wgen + b_vis_inc_updated)

                start_time = time.time()

                # Start tensorflow session
                with tf.Session(graph=g) as sess:
                    # Initialise the graph
                    sess.run(tf.global_variables_initializer())

                    # Iterate over number of epochs.  Epoch 0 has no training, just evaluation of the cost
                    # before learning begins
                    for epoch in range(num_epochs+1):
                        J = 0.0

                        if epoch == 9:
                            sess.run(momentum.assign(finalmomentum))

                        # Split data into mini-batches
                        for b in range(num_batches):
                            x_batch = xpos[b*batch_size:(b+1)*batch_size,:]

                            if epoch > 0:
                                # For non-zero epochs do one epoch of optimisation and evaluate the cost
                                sess.run([W_update, b_hid_update, b_vis_update], feed_dict={g_xpos: x_batch})

                            # For epoch zero just compute the cost
                            Jb = sess.run(g_cost, feed_dict={g_xpos: x_batch})


                            # Add this mini-batch'es cost to the total cost
                            J += Jb
                        # Take the average of the cost accross mini-batches
                        J /= num_batches
                        if epoch==0:
                            remTimeStr = "?"
                            start_time = time.time()
                        else:
                            elapsed_time = time.time() - start_time
                            if elapsed_time == 0:
                                elapsed_time = 1

                            remTime = math.ceil(float(elapsed_time)/float(epoch) * (num_epochs-epoch))

                            if remTime <= 60.0:
                                remTimeStr = "%dsec" % remTime
                            elif remTime <= 3600.0:
                                remTimeSec = remTime % 60
                                remTimeStr = "%dmin, %dsec" % (remTime/60, remTimeSec)
                            else:
                                remTimeMin = remTime % 3600
                                remTimeStr = "%dhrs, %dmin" % (remTime/3600, (remTimeMin/60))


                        if epoch < num_epochs:
                            # Print the epoch number and the cost
                            print("Epoch %d: cost=%.2e (remaining trainig time for this layer %s)" % (epoch, J, remTimeStr))

                    # Once training is finished, take parameter data form the graph and save it
                    # in model's member variables
                    self.W[l] = sess.run(g_W[-1])
                    self.w0[l] = sess.run(g_w0[-1])
                    self.wgen[l] = sess.run(g_wgen)

    # Backpropagation learning over specified cost and number of epochs
    #
    # Input: input - an NxM input data matrix, where N is the number of points and M is number of attributes per point
    #        labels - an NxK true otuput data matrix, where N is the number of points and M is number of attributes
    #                 per point.
    #        cost - string value specifying the cost ('mse' and 'ce' costs are supported
    #        alpha - learning reate
    #        num_epochs - number of epochs to train for
    #        batch_size (optional) - mini-batch size.  Mini-batch training speeds up training a bit - leaving this
    #                                default value of 128 should be fine.
    def learn(self, input, labels, cost, alpha, num_epochs, batch_size=128):

        # First, the learning will be done just over the final layer (keeping the RBM learned weights constant).  This
        # puts the weights of the last layer in a better state than just starting from random values
        print("\nQuick supervised training of just the last layer %d..." % len(self.W))

        num_points = input.shape[0]

        # Determine the number of min-batches in the dataset
        num_batches = num_points // batch_size
        if num_batches < 1:
            num_batches = 1
            batch_size = num_points


        Wsaved = list(self.W)
        self.W = self.W[0:-1]
        g, g_yhat, g_vhat, g_x, g_W, g_w0 = self.tensorflow_graph()

        self.W = list(Wsaved)

        # Augment the tensorflow graph
        with tf.Session(graph=g) as sess:
           # Initialise the graph
           sess.run(tf.global_variables_initializer())
           xpos = sess.run(g_yhat, feed_dict={g_x: input})

        g = tf.Graph()

        with g.as_default():
            g_x = tf.placeholder("float", [None, xpos.shape[1]])
            g_y = tf.placeholder("float", [None, labels.shape[1]])

            W = tf.Variable(self.W[-1], dtype='float32')
            w0 = tf.Variable(self.w0[-1], dtype='float32')


            g_v = tf.add(tf.matmul(g_x, W), w0)
            g_cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=g_v, labels=g_y))

            g_optimizer = tf.train.AdamOptimizer(learning_rate=alpha).minimize(g_cost)

            # Start tensorflow session
            with tf.Session(graph=g) as sess:
                # Initialise the graph
                sess.run(tf.global_variables_initializer())

                # Iterate over jsut 10 epochs.  The training over the entire network will be done
                # for number of epochs specified in the argument
                for epoch in range(10):
                    J = 0.0
                    # Split data into min-batches
                    for b in range(num_batches):
                        x_batch = xpos[b * batch_size:(b + 1) * batch_size, :]
                        y_batch = labels[b * batch_size:(b + 1) * batch_size, :]
                        if epoch == 0:
                            # For epoch zero just compute the cost
                            Jb = sess.run(g_cost, feed_dict={g_x: x_batch, g_y: y_batch})
                        else:
                            # For non-zero opoch do one epoch of optimisation and evaluate the cost
                            _, Jb = sess.run([g_optimizer, g_cost], feed_dict={g_x: x_batch, g_y: y_batch})
                        # Add this mini-batch'es cost to the total cost
                        J += Jb
                    # Take the average of the cost accross mini-batches
                    J /= num_batches
                    if epoch == 0:
                        remTimeStr = "?"
                        start_time = time.time()
                    else:
                        elapsed_time = time.time() - start_time
                        if elapsed_time == 0:
                            elapsed_time = 1

                        remTime = math.ceil(float(elapsed_time) / float(epoch) * (10 - epoch))

                        if remTime <= 60.0:
                            remTimeStr = "%dsec" % remTime
                        elif remTime <= 3600.0:
                            remTimeSec = remTime % 60
                            remTimeStr = "%dmin, %dsec" % (remTime / 60, remTimeSec)
                        else:
                            remTimeMin = remTime % 3600
                            remTimeStr = "%dhrs, %dmin" % (remTime / 3600, (remTimeMin / 60))

                    if epoch < num_epochs:
                        # Print the epoch number and the cost
                        print("Epoch %d: cost=%.2e (remaining trainig time of this layer %s)" % (epoch, J, remTimeStr))

                # Once training is finished, take parameter data form the graph and save it
                # in model's member variables
                self.W[-1] = sess.run(W)
                self.w0[-1] = sess.run(w0)

        print(" ")
        # Train the entire netowrk
        super().learn(input, labels, cost, alpha, num_epochs, batch_size)




