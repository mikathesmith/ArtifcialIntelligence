from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
import matplotlib
import matplotlib.pyplot as pl
import time
import random
from sklearn import manifold

__author__ = "Lech Szymanski"
__email__ = "lechszym@cs.otago.ac.nz"

# Global handles for the plot (necessary for plot animation)
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

def show(input, labels=None, withVisOfVectorSpace=False, num_samples=500, num_images=16):
    num_points, num_attributes = np.shape(input)

    figure_handle = pl.figure()
    pl.ion()
    pl.show()


    if withVisOfVectorSpace:
        if num_points < num_samples:
            num_samples = num_points


        tsne = manifold.TSNE(n_components=2, init='pca', random_state=0, method='exact')
        x = tsne.fit_transform(input[0:num_samples,:])

        x_min, x_max = np.min(x, 0), np.max(x, 0)
        x = (x - x_min) / (x_max - x_min)

        ax = pl.subplot(1,2,1)
        if labels is None:
           pl.scatter(x[:, 0], x[:, 1])
        else:
           if labels.ndim == 1:
                c = np.max(labels[0:num_samples]) + 1
           else:
                c = labels.shape[1]

           for i in range(c):
              if labels.ndim == 1:
                 I = np.where(labels[0:num_samples] == i)
              else:
                 I = np.where(labels[0:num_samples, i] == 1)[0]
              pl.scatter(x[I, 0], x[I, 1], color=pl.cm.Set1(i / float(c)))


    if num_points < num_images:
        num_images = num_points

    num_rows = int(np.floor(np.sqrt(num_images)))
    num_cols = int(np.ceil(float(num_images) / float(num_rows)))

    im_height = int(np.sqrt(num_attributes))
    im_width = int(np.sqrt(num_attributes))

    n = 0
    title_str = None
    for r in range(num_rows):
        for c in range(num_cols):
            if n >= num_images:
                continue

            im = input[n, :].reshape(im_height, im_width)
            if labels is not None:
                if labels.ndim == 1:
                    title_str = "Label %d" % (labels[n] + 1)
                else:
                    if labelStrings is None:
                        title_str = np.argmax(labels[n,:])
                    else:
                        title_str = labelStrings[np.argmax(labels[n,:])]

            if withVisOfVectorSpace:
                h = figure_handle.add_subplot(num_rows, 2*num_cols, r*num_cols*2+num_cols+n%(num_cols)+1)
            else:
                h = figure_handle.add_subplot(num_rows, num_cols, n+1)

            n += 1

            h.imshow(im)
            h.xaxis.set_visible(False)
            h.yaxis.set_visible(False)
            if title_str is not None:
                h.set_title(title_str)

            pl.pause(0.01)
            time.sleep(0.01)

