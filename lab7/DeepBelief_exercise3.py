import dataset_mnist
import numpy as np
from dbn import dbn

x, y, xTest, yTest = dataset_mnist.read(randomShift=False)
h=dbn(n_inputs=784,
      layers=[{'neurons':12, 'activation':'sigmoid'},
              {'neurons':3, 'activation':'softmax'}]
      )
#you cn first do unsupervised learning layer by layer training of
#the hidden layers like so. This treats the hidden layers as a stack
# of Restricted Boltzmann Machines (RBM) (if you remove this, equivalent to MLP model)
h.learn_unsupervised(input=x, alpha=0.01, num_epochs=50)
#unsupervised training can be followed by supervised training of the entire model
h.learn(input=x, labels=y, cost='ce', alpha=0.01, num_epochs=50)

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
