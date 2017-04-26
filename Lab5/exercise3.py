#Simple Recurrent network performing the MNIST classification.
# Pays attention a temporal pattern in the data by processing a sequence of
#subimages in order to make a classification. Eg a 28x28 sample image from
#the dataset can also be processed as a sequence of 28 vectors, each of size
#28.

#Starting with a sample input t1 and through to input t27, the output of the
#model is ignored; only the context from the hidden layer of the previous input
#is saved and used to augment the input of the next sequence. After input t28,
#the classifcation at the output is measured.
#
# SRN model converts each sample to a set of vectors of n_inputs_srn size.
import dataset_mnist
from srn import srn

x, y, xTest, yTest = dataset_mnist.read();
dataset_mnist.show(input=x, labels=y)


#instantiate an object that implements an SRN hypothesis function
#n_inputs_image:  specifies total number of pixels in a single image
#n_inputs_srn : size of a suub-image vector that gets fed to SRN at a given point
#(ensure it divides by 784 without a remainder)

#When processing a 28x28 image, the model will divide it into a sequence of
#n_inputs_image/n_inputs_srn vectors of size n_inputs_srn, and the set of those
#vectors as a sequence.

#layers: list of dictionaries, each specifying the configuration of a layer
#for the SRN model, only two layers are allowed: one to specify the size of
#the hidden layer and the second the output layer.

#both layers are using sigmoid activation functions.
h=srn(n_inputs_image=784, n_inputs_srn=28,
      layers = [
          {'neurons':2, 'activation': 'sigmoid'}, #hidden layer : feedsback on itself
          #so the effective input size to the hidden layer will be n_inputs_srn + the
          #number of neurons in the hidden layer - 28+2 = 30
          {'neurons':3, 'activation':'sigmoid'} #output, 3 neurons each to specify a digit
          #being identified.
      ]
    )

#x matrix = Nx784 data matrix.

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

