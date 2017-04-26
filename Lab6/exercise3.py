#Convolutional neural network.

from cnn import cnn
import dataset_mnist

x,y,xTest,yTest = dataset mnist.read()

# The height, width and colours arguments specify the size of the input image -MNIST dataset is grayscale 28x28 pixels
# layers parameter is a list of dictionaries, each specifying the configuration of a layer. Here we have 3 layers

h=cnn(height=28, width=28, colours=1,
      layers=[{'type':'conv', 'width':3, 'height':3, 'filters':14, 'strides':1,
        'activation':'relu'},
        # The above layer is convulutional. Width and height of the subimage that a filter takes as an input.
        #The number of filter, the number of pixels that convolution strides over and the activation function used


              {'type':'maxpool', 'height':2, 'width':4, 'strides':2},
              #This is a max pooling layer. Width and height of the pooling window as well as the number of pixels
              #in the feature map that the window strides over.

              {'type':'fc', 'neurons':3, 'activation':'softmax'}
              #This is a fully connected layer consisting of 3 neurons, using a softmax function activation.
            ]
      )

#The rest of the model operates the same as the MLP and SRN models. Whenever you provide input data to the model,
#just supply the x matrix (N x 784 data matrix). The CNN model will convert each sample to a 28x28x1 image that it
#needs for the first convultion.

#Train the model, test different architectures and learning parameters. See if you can get better performance on digit
#recognition task than the MLP or SRN model.






