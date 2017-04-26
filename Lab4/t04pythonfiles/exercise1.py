import pylab as pl
import numpy as np
from matplotlib.pyplot import show, ioff
import dataset_reg
from polynomial import polynomial
from coscos import coscos
from mlp import mlp

# Read the data and show it on a plot - you can read other data files by changing the name string
(x, y) = dataset_reg.read(name="t4dataset1.npz")
# Show a scatter plot of the data
dataset_reg.show(input=x, output=y, type="scatter")

# This number indicates the percentage split for training data.  0.8 means that 80% of the data will
# be used for training and 20% for testing
pTrain = 0.8

# Total number of points in the dataset
N = len(x)
# Create a random permutation of data sample indexes
I = np.random.permutation(N);
# Split the indexes into the training and testing indexes
I_train = I[1:int(np.floor(pTrain * N))]
I_test = I[int(np.floor(pTrain * N)) + 1:N]
# Create training and test sets
x_train = x[I_train]
y_train = y[I_train]
x_test = x[I_test]
y_test = y[I_test]

# Pick a hypothesis by uncommenting it

# Polynomial hypothesis
h = polynomial(k=1)

# Coscos hypothesis
#h = coscos(k=1)

# MLP hypothesis
#h = mlp(layers=[{'neurons': 4, 'activation': 'sigmoid'},
#                {'neurons': 2, 'activation': 'sigmoid'},
#                {'neurons': 1, 'activation': 'lin'}
#                ])


# Generate input points for ploting hypothesis
v = np.linspace(np.min(x), np.max(x), 200)

# Train the hypothesis
for epoch in range(20000):
    # One iteration of updates - might need to change alpha if
    # J is not going down or flying off to nan.  The parameters of
    # the hypothesis are going to change after this function according
    # with steepest gradient rule
    J_train = h.learn(input=x_train, true_output=y_train, alpha=0.1)

    # Compute the output of the hypothesis on the test data
    yhat_test = h.output(input=x_test)
    # Compute the residual error on the test data
    error = y_test - yhat_test
    # Compute the MSE cost (**2 in python means rais to power 2)
    J_test = np.mean(error ** 2)

    # Show training and test cost - if training cost is going up, you might
    # have to redue alpha.  Remember, steepest gradient updates guarantee that the
    # direction of the change reduces the cost...but if step is too big, it might
    # still make the cost after the change go up
    print("Epoch %d: train J=%.2f, test J=%.2f" % (epoch, J_train, J_test))

    # Every 100 epochs show visualistion of the hypothesis on a graph
    if epoch % 100 == 0:
        dataset_reg.show(input=v, output=h.output(input=v), type="line")
        pl.title("Epoch %d" % epoch)

# These command assure that the script doesn't terminate and close the figures automatically when it's finished
ioff()
show()
