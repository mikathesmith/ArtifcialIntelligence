import tensorflow as tf
import numpy as np
import sys
import os
import gzip
import pickle
import time
import math

__author__ = "Lech Szymanski"
__email__ = "lechszym@cs.otago.ac.nz"

# Base class for the mlp, srn and cnn models.  It provides methods
# for computing output, error and training the model
class learner():

    # Compute the output of the model
    #
    # Input: input - an NxM input data matrix, where N is the number of points and M is number of attributes per point
    #
    # Returns: output - an NxK output data matrix, where N is the number of pont and K is the number of model's outputs
    #
    def output(self, input):
        # Build the tensorflow graph - this method must be provided by the subclass
        #
        # g is the reference to the graph, g_y reference to the model's output in the graph, g_v reference to activity
        # of the model's output, g_x reference to the graph's input placeholder, g_W and g_w0 is a list of
        # references to model's parameters
        g, g_y, g_v, g_x, g_W, g_w0 = self.tensorflow_graph()

        # Check that the number of attributes, M, provided in the input is the same as the number of the attrbiutes
        # expected by the model
        num_attrib = np.shape(input)[1]
        num_attrib_model = g_x.get_shape()[1].value
        if num_attrib_model != num_attrib:
            print(
                "Error! Model was set up for %d attributes in the input, and there are %d attributes in the provied dataset!" % (num_attrib_model, num_attrib))
            sys.exit(-1)

        # Start tensorflow session
        with tf.Session(graph=g) as sess:
            # Initialise the variables in the graph
            sess.run(tf.global_variables_initializer())

            # Feed model parameters to the graph
            for l in range(len(self.W)):
                W = tf.assign(g_W[l], self.W[l])
                sess.run(W)

            for l in range(len(self.w0)):
                w0 = tf.assign(g_w0[l], self.w0[l])
                sess.run(w0)

            # Evaluate g_y, model's output feeding the input
            output = sess.run(g_y, feed_dict={g_x: input})

        return output

    # Compute classification error of the model
    #
    # Input: input - an NxM input data matrix, where N is the number of points and M is number of attributes per point
    #        labels - an NxK true otuput data matrix, where N is the number of points and M is number of attributes
    #                 per point.  This is the correct labelling of the data, against which model's output will be
    #                 evaluated.
    #
    # Returns: error - Percentage of the N points that are misclassified by the model
    #
    def error(self, input, labels):
        # Build the tensorflow graph - this method must be provided by the subclass
        #
        # g is the reference to the graph, g_y reference to the model's output in the graph, g_v reference to activity
        # of the model's output, g_x reference to the graph's input placeholder, g_W and g_w0 is a list of
        # references to model's parameters
        g, g_yhat, g_vhat, g_x, g_W, g_w0 = self.tensorflow_graph()

        # Perform check on the format of the provided input and labels - to make sure it will work fine with
        # the model
        num_points, _ , num_outputs = self.check_input_provided(input, g_x, labels, g_yhat)

        # Augment the tensorflow graph
        with g.as_default():
            # Add a placeholder point, where true output will be feed
            g_y = tf.placeholder("float", [None, num_outputs])

            # Compare the model's output to the true output.  For a given output 1xK and true output 1xK, for each
            # the label is the index with the largest attribute.  If the largest attribute for both is on the same
            # index, then classification is correct, otherwise it is not
            g_wrong_prediction = tf.not_equal(tf.argmax(g_yhat, 1), tf.argmax(g_y, 1))
            # Create tensorflow operation for evaluation of the error
            g_error = tf.reduce_sum(tf.cast(g_wrong_prediction, "float"))

            # Start tensorflow session
            with tf.Session(graph=g) as sess:
                # Initialise the variables in the graph
                sess.run(tf.global_variables_initializer())

                # Feed model parameters to the graph
                for l in range(len(self.W)):
                    W = tf.assign(g_W[l], self.W[l])
                    sess.run(W)

                for l in range(len(self.w0)):
                    w0 = tf.assign(g_w0[l], self.w0[l])
                    sess.run(w0)

                # Evaluate the error op feeding input data and target labels
                error = sess.run(g_error, feed_dict={g_x: input, g_y: labels})

        # Return error as percentatage of N - the number of points
        return error/num_points*100

    # Return part of the dataset along with incorrect labels that is misclassified by the model
    #
    # Input: input - an NxM input data matrix, where N is the number of points and M is number of attributes per point
    #        labels - an NxK true otuput data matrix, where N is the number of points and M is number of attributes
    #                 per point.  This is the correct labelling of the data, against which model's output will be
    #                 evaluated.
    #
    # Returns: misclassified_input, wrong_labels - data matrix and corresponding bad labels from input that get
    #                                              misclassified by the model
    def extract_misclassified_data(self, input, labels):
        # Build the tensorflow graph - this method must be provided by the subclass
        #
        # g is the reference to the graph, g_y reference to the model's output in the graph, g_v reference to activity
        # of the model's output, g_x reference to the graph's input placeholder, g_W and g_w0 is a list of
        # references to model's parameters
        g, g_yhat, g_vhat, g_x, g_W, g_w0 = self.tensorflow_graph()

        # Perform check on the format of the provided input and labels - to make sure it will work fine with
        # the model
        num_points, _, num_outputs = self.check_input_provided(input, g_x, labels, g_yhat)

        # Augment the tensorflow graph
        with g.as_default():
            # Add a placeholder point, where true output will be feed
            g_y = tf.placeholder("float", [None, num_outputs])
            # Add an op that determines indexes of the misclassified points
            g_I = tf.where(tf.not_equal(tf.argmax(g_yhat, 1), tf.argmax(g_y, 1)))

            # Start tensorflow session
            with tf.Session(graph=g) as sess:
                # Initialise the variables in the graph
                sess.run(tf.global_variables_initializer())

                # Feed model parameters to the graph
                for l in range(len(self.W)):
                    W = tf.assign(g_W[l], self.W[l])
                    sess.run(W)

                for l in range(len(self.w0)):
                    w0 = tf.assign(g_w0[l], self.w0[l])
                    sess.run(w0)

                # Evaluate the output of the model and indexes of misclassified data
                [yhat, I] = sess.run([g_yhat, g_I], feed_dict={g_x: input, g_y: labels})
                I = I[:,0]
        # Return input and model's output for misclassified points
        return input[I,:],  yhat[I,:]

    # Check whether the input and target labels are in correct format with respect to the tensorflow graph
    #
    # Input: input - an NxM input data matrix, where N is the number of points and M is number of attributes per point
    #        g_x - reference to tensorflow graph where input is to be fed
    #        labels - an NxK true otuput data matrix, where N is the number of points and M is number of attributes
    #                 per point.
    #        g_yhat - reference to tensorflow graph for model's output
    #
    # Returns: num_points, num_attrib, num_outputs - the value of N, M and K
    def check_input_provided(self, input, g_x, labels, g_yhat):
        # Read N and M from input data
        num_points, num_attrib = np.shape(input)
        # Check the M expected by the tensorflow graph's input
        num_attrib_model = g_x.get_shape()[1].value
        if num_attrib_model != num_attrib:
            print(
                "Error! Model was set up for %d attributes in the input, and there are %d attributes in the provied dataset!" % (
                    num_attrib_model, num_attrib))
            sys.exit(-1)

        # Check the provided input and labels have same number of points: N
        if num_points != np.shape(labels)[0]:
            print(
                "Error! The number of given input points in the training data is %d, and in the true output is %d - it needs to be the same!" % (
                    num_points, np.shape(labels)[0]))
            sys.exit(-1)

        # Check that N expected by the tensorflow graph's output
        num_outputs = np.shape(labels)[1]
        num_outputs_model = g_yhat.get_shape()[1].value
        if num_outputs_model != num_outputs:
            print(
                "Error! Model was set up for %d outputs in the final layer, and there are %d true otuputs per training in the provied dataset!" % (
                    num_outputs_model, num_outputs))
            sys.exit(-1)

        return num_points, num_attrib, num_outputs

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
        print("Training...")

        # Build the tensorflow graph - this method must be provided by the subclass
        #
        # g is the reference to the graph, g_y reference to the model's output in the graph, g_v reference to activity
        # of the model's output, g_x reference to the graph's input placeholder, g_W and g_w0 is a list of
        # references to model's parameters
        g, g_yhat, g_vhat, g_x, g_W, g_w0 = self.tensorflow_graph()

        # Perform check on the format of the provided input and labels - to make sure it will work fine with
        # the model
        num_points, _, num_outputs = self.check_input_provided(input, g_x, labels, g_yhat)

        # Augment the tensorflow graph
        with g.as_default():
            # Add a placeholder point, where true output will be feed
            g_y = tf.placeholder("float", [None, num_outputs])

            # Create tensorflow operation for the cost
            if cost=='ce':
                # Cross-entropy
                if self.g[-1]=="softmax":
                    # Tensorflow combines softmax and ce into one operation, so if otput of the last layer is softmax
                    # then need to apply softmax crosss entropy operation to last layer's activity...
                    g_cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=g_vhat,labels=g_y))
                else:
                    #...otherwise just apply sigmoid cross entropy to last layer's activity.  Need to work with
                    # activity and not the output, because tensorflow applies sigmoid function inside its operator
                    g_cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=g_vhat, labels=g_y))
            elif cost=='mse':
                # Mean squared error
                g_cost = tf.reduce_mean(tf.square(g_y-g_yhat))
            else:
                print(
                    "Error! Unrecognised cost function '%s' (valid choices are 'mse', 'ce')!" % cost)
                sys.exit(-1)

            # Create optimiser over the specified cost.  Adam optimiser is an implementation of steepest gradient
            # descent optimisation with numerous tricks to speed up optimisation.
            #g_optimizer = tf.train.AdamOptimizer(learning_rate=alpha).minimize(g_cost)
            g_optimizer = tf.train.GradientDescentOptimizer(learning_rate=alpha).minimize(g_cost)

            # Determine the number of min-batches in the dataset
            num_batches = num_points//batch_size
            if num_batches < 1:
                num_batches = 1
                batch_size = num_points

            start_time = time.time()

            # Start tensorflow session
            with tf.Session(graph=g) as sess:
                # Initialise the graph
                sess.run(tf.global_variables_initializer())

                # Feed model parameters to the graph
                for l in range(len(self.W)):
                    W = tf.assign(g_W[l], self.W[l])
                    sess.run(W)

                for l in range(len(self.w0)):
                    w0 = tf.assign(g_w0[l], self.w0[l])
                    sess.run(w0)

                # Iterate over number of epochs.  Epoch 0 has no training, just evaluation of the cost
                # before learning begins
                for epoch in range(num_epochs+1):
                    J = 0.0
                    # Split data into min-batches
                    for b in range(num_batches):
                        x_batch = input[b*batch_size:(b+1)*batch_size,:]
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
                        print("Epoch %d: cost=%.2e (remaining trainig time %s)" % (epoch, J, remTimeStr))

                # Once training is finished, take parameter data form the graph and save it
                # in model's member variables
                for l in range(len(self.W)):
                    self.W[l] = sess.run(g_W[l])
                for l in range(len(self.w0)):
                    self.w0[l] = sess.run(g_w0[l])



    # Saves model into a file
    #
    # Input: name - the name of the file
    def save(self, name):
        # Print save message
        sys.stdout.write("Saving model to '%s'..." % name)
        sys.stdout.flush()
        # Save and archive the model
        with gzip.open(name, 'w') as f:
            pickle.dump(self, f)
        sys.stdout.write("done\n")
        sys.stdout.flush()

    # Loads the model from a file.  This is a static method that creates a new instance of the model class
    #
    # Input: name - the name of the file
    @staticmethod
    def load(name):
        sys.stdout.write("Loading model from '%s'..." % name)
        sys.stdout.flush()
        # Check that the file exists
        if os.path.isfile(name):
            # Load and unarchive the model
            with gzip.open(name) as f:
                model = pickle.load(f)
        else:
            print("\nError! Cannot find file '%s'." % name)
            sys.exit(-1)
        sys.stdout.write("done\n")
        sys.stdout.flush()
        model.info()
        return model