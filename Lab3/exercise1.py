import perceptron
import numpy as np
from matplotlib.pyplot import show, ioff


# Binary input, formated as a matrix, with each column correspnding to different attribute (there are two) and each
# row cooresponding to different sample to learn from (there are four)
x = np.array([[0, 0],
              [0, 1],
              [1, 0],
              [1, 1]])

# True output for the above input implementing the boolean AND function - output is one when both inputs are one.
y = np.array([0,
              1,
              1,
              0])

# Initialise a weight vector to a random state using normal distribution centered at 0 and with standard deviation
# of 0.03.  The weight vector format is [w_1 w_2 w_0] - the last parameter is the bias.
w = np.random.randn(3) * 0.03

# Read the shape of the input matrix to determine the number of inputs.
num_points, _  = x.shape

# Train the perceptron for maximum of 1000 epochs
maxEpochs = 1000
for i in range(maxEpochs):
    # Get the new weights after exposing the perceptron to all inputs.  The expected weights are in format
    # [w_1 .... w_M w_0], where M is the number of attributes of a given input.  The returned, updated weight vector
    # is in the same format.  The learning parameter is specified by the the alpha parameter - you can change it to
    # something else, but it should be something < 1.
    w = perceptron.learn(input=x, true_output=y, parameters=w, alpha=0.01)

    # Show the perceptron as a 2D visualisation with region that corresponds to perceptron's output of 1 shaded in
    # blue
    perceptron.show(input=x,output=y,parameters=w)

    # Compute the output of the perceptron -activity
    yhat = perceptron.hypothesis(input=x, parameters=w)

    # Count the number of errors it makes
    nErrors = 0
    for n in range(num_points):
        if yhat[n] != y[n]:
            nErrors += 1

    print("Epoch %d...%d errors." % (i+1, nErrors))

    # If no errors are made, stop training - there will be no updates.
    if nErrors == 0:
        print("Converged.")
        break

print(w)
# This two lines assure that the script stops and waits for you to close the figure in order to terminate.  This
# way the plot doesn't disappear as soon as the training is done.
ioff()
show()