from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
import matplotlib
import matplotlib.pyplot as pl
import time
import random

__author__ = "Lech Szymanski"
__email__ = "lechszym@cs.otago.ac.nz"

# Global handles for the plot (necessary for plot animation)
figure_handle = None
plot_handle = None
line_handle = None
fill_handle = None
labelStrings = None

# Read MNIST dataset (downloading it from Internet first time around)
def read(selectedLabels=[4, 8, 9], randomShift=True):
    global labelStrings

    # Read the data
    data = input_data.read_data_sets("./mnist", one_hot=True)
    x = data.train.images
    y = data.train.labels
    xTest = data.test.images
    yTest = data.test.labels

    # If selectedLabels not set to 'all', then select only certain
    # types of images from the data
    if selectedLabels != 'all':
        labelStrings = selectedLabels

        x, y = selectByLabel(x, y, selectedLabels)
        xTest, yTest = selectByLabel(xTest, yTest, selectedLabels)

    # To make the learning task a bit harder, randomly shift the images by +/-3 pixels in horizontal and
    # vertical direction
    if randomShift:
        N = np.shape(x)[0]

        for n in range(N):
            x[n,:] = shift(x[n,:],random.randint(-3,3),random.randint(-3,3))

        N = np.shape(xTest)[0]

        for n in range(N):
            xTest[n,:] = shift(xTest[n,:],random.randint(-3,3),random.randint(-3,3))

    # Print information about the data
    N, M = np.shape(x)
    _, K = np.shape(y)
    Ntest, _ = np.shape(xTest)

    print("Dataset info:")
    print("\tNumber of training points: %d" % N)
    print("\tNumber of test points: %d" % Ntest)
    print("\tNumber of attributes per point: %d" % M)
    print("\tNumber of classes: %d" % K)

    return x, y, xTest, yTest

def shift(x, sh_hor, sh_ver):

    #N = np.shape(x)[0]

    #x = np.reshape(x, (N, 28, 28))
    x = np.reshape(x, (28, 28))

    if sh_hor > 0:
        x = np.concatenate((x[:, sh_hor:], np.zeros((28,sh_hor))), axis=1)
    elif sh_hor < 0:
        x = np.concatenate((np.zeros((28,-sh_hor)),x[:, :sh_hor]), axis=1)


    if sh_ver > 0:
        x = np.concatenate((x[sh_ver:,:], np.zeros((sh_ver,28))), axis=0)
    elif sh_ver < 0:
        x = np.concatenate((np.zeros((-sh_ver,28)),x[:sh_ver,:]), axis=0)


    x = np.reshape(x, (28*28))

    return x

def selectByLabel(x, y, selectedLabels):

    yInd = np.argmax(y, axis=1)

    It = list()
    I = np.ones(len(yInd))==0
    for c in selectedLabels:
        I = np.logical_or(I,yInd==c)
        It.append(c)

    I = np.where(I==True)[0]
    x = x[I, :]
    y = y[I, :]
    y = y[:, It]

    return x, y

def show(input, labels=None, num_images=16):
    global figure_handle, plot_handle, line_handle, fill_handle
    global labelStrings

    num_points, num_attributes = np.shape(input)

    if plot_handle is None:
        pl.close('all')
        # Create a new (empty) figure
        figure_handle = pl.figure()
        plot_handle = list()
        pl.ion()
        pl.show()

    if num_points > num_images:
        num_points = num_images

    num_rows = int(np.floor(np.sqrt(num_points)))
    num_cols = int(np.ceil(float(num_points) / float(num_rows)))

    im_height = int(np.sqrt(num_attributes))
    im_width = int(np.sqrt(num_attributes))

    for i in range(len(plot_handle)):
        plot_handle[i].remove()
    plot_handle = list()

    n = 0
    title_str = None
    for r in range(num_rows):
        for c in range(num_cols):
            if n >= num_points:
                continue

            im = input[n, :].reshape(im_height, im_width)
            if labels is not None:
                if labelStrings is None:
                    title_str = np.argmax(labels[n,:])
                else:
                    title_str = labelStrings[np.argmax(labels[n,:])]

            n += 1
            plot_handle.append(figure_handle.add_subplot(num_rows, num_cols, n))
            plot_handle[-1].imshow(im)
            plot_handle[-1].xaxis.set_visible(False)
            plot_handle[-1].yaxis.set_visible(False)
            if title_str is not None:
                plot_handle[-1].set_title(title_str)

    pl.pause(0.1)
    time.sleep(0.1)

