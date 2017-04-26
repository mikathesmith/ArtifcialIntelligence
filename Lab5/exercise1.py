#Create an MLP model and train it on the MNIST dataset, a set of 28x28 images of hand-written digits.
#The task is to identify the digit from the mage.


import dataset_mnist
from mlp import mlp


#Read function returns variables; x is the training data N x M matrix, where N is the number of points
#and M is the size of a single input (784 attributes from a 28 x 28 image),
x, y, xTest, yTest = dataset_mnist.read();
dataset_mnist.show(input=x, labels=y)

#inputs argument specifies the number of input to the network - 784
#the layers parameter is a list of dictionaries, each specifying the configuration of a layer

h = mlp(n_inputs=784, layers= [ {'neurons': 7, 'activation': 'sigmoid'}, {'neurons': 3, 'activation': 'sigmoid'} ])

#x and y (training set data) is passed in. For the cost fnction we use mean squared error.
h.learn(input=x, labels=y, cost='mse', alpha=0.01, num_epochs=20)

#After the training, you can check the training and test error.
eTrain = h.error(input=x, labels=y)
eTest = h.error(input=xTest, labels=yTest)
print("Training error: %.2f%% " %eTrain)
print("Test error: %.2f%%" % eTest)

#To compute the output of the model
yhatTest = h.output(input=xTest)

#This output is actual output of the network, which you can interpet as the probability of a given neuron being on.
#To see how this output classifies a sample of the data, you can invoke the following function which shows 16 images
#and their labels
dataset_mnist.show(input=xTest, labels=yhatTest)

#Extract missclassified examples from a dataset and inspect them.
xm,ym= h.extract_misclassified_data(input=xTest, labels=yTest)
print("Num missed examples: %d" %xm.shape[0])
dataset_mnist.show(input=xm, labels=ym)

#save the trained model
h.save("mlpmodel")




