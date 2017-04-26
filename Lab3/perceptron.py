import perceptron
import matplotlib

#matplotlib.rcParams['text.usetex'] = True
#matplotlib.rcParams['text.latex.unicode'] = True
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time
import sys

# Global handles for the plot (necessary for plot animation)
figure_handle = None
plot_handle = None
line_handle = None
fill_handle = None


# Hard limiting function
#
# Input: input - value input to the function
#
# Returns: int - g(input) = 1 when input is positive or zero, and
#                 g(input) = 0 otherwise
def hardlim_function(input):
    if input >= 0:
        return 1
    else:
        return 0


# Computes the output of the perceptron
#
# Input: input - data to input to perceptron, must be a vector of 1 by num_attributes (for a single input point) or
#                a 2D array of num_points by num_attributes.
#        parameters - perceptron parameters, an (num_attributes+1) array where the last parameters is the bias.
#
# Returns:  num_points array of perceptron outputs
def hypothesis(input, parameters):
    # Read the data format - number of points and attributes per point
    num_points, num_attributes = input.shape

    # Check that parameters array is the right size - must be same number as attributes in the input + 1 for
    # bias parameter
    if not num_attributes + 1 == parameters.size:
        sys.exit(
            "The number of weights in then weight vector (currently %d) must match the number of attributes in "
            "the input+1 (currently %d)." % (parameters.size, num_attributes))

    # Create output array of num_points
    output = np.zeros((num_points,))

    # Compute perceptron output for each point n out of num_points
    for n in range(0, num_points, 1):
        # Initialise the activity to negative bias
        activity = -parameters[-1]
        # Add to activity the num_attributes of the nth input multiplied
        # by corresponding perceptron weights
        for m in range(0, num_attributes, 1):
            activity += parameters[m] * input[n, m]
        # Take the hard limiting function of the compute activity
        # for the nth output
        output[n] = hardlim_function(activity)

    return output


# Single adjustment of perceptron parameters using the learning rule.  If the passed in input is just an num_attributes
# array corresponding to a single input instance, the function does an online update based on just this point.  If the
# passed-in input is a two-dimensional array (like a table) of num_points by num_attributes, the function will do a
# batch update averaging the updates from num_points points.
#
# Input: input - data to input to perceptron, must be a vector of 1 by num_attributes (for a single input point) or a
#                2D array of num_points by num_attributes.
#        true_output - a num_points array of true (desired) outputs corresponding to the input
#        parameters - perceptron parameters, an (num_attributes+1) array where the last parameters is the bias
#        alpha - learning rate
#
# Returns: A (num_attributes+1) array of updated parameters after one training epoch

def learn(input, true_output, parameters, alpha):
    # Read the data format - number of points and attributes per point
    num_points, num_attributes = input.shape

    # Compute the output of the perceptron
    output = hypothesis(input, parameters)

    # Initialise a (num_attributes+1) array of parameter changes - set them to zero
    delta_parameters = np.zeros((num_attributes + 1,))

    # Sum all the changes to parameters over num_points
    for n in range(0, num_points, 1):
        # Compute the error of the nth output
        error = true_output[n] - output[n]
        # Compute the change in parameters based on that error and the nth input - add it to the total
        # of parameter chagnes
        delta_parameters[0:-1] += error * input[n, :]
        # Compute the change in the bias (index -1 indicates the last value in the array) of the parameters and
        # add it to the total of parameter chagnes
        delta_parameters[-1] -= error

    # Update the parameters with the average of parameter changes over num_points multiplied by the learning factor.
    # If num_points is one, the average is just the entire update due to one (input,target_ouptut) pair.
    parameters += alpha * delta_parameters / float(num_points)

    return parameters


# Visualisation for data and the perceptron.
#
# Inputs: input - data to input to perceptron, must be a vector of 1 by num_attributes (for a single input point) or
#                 a 2D array of num_points by num_attributes.  If num_attributes=2, then the visualisation will show the
#                 points in 2D space, otherwise it will reformat the input as an image.
#         output (optional) - if given with 2D data, it will label the data with different colors (blue for 0
#                             and red for 1), otherwise it will display labels as 'Even' for 0 or 'Odd' above the image.
#         parameters (optional) - if given with 2D data will show the separating line and mark the area that's labeled
#                                 as 0 in blue.
def show(input, output=None, parameters=None):
    global figure_handle, plot_handle, line_handle, fill_handle

    num_points, num_attributes = input.shape

    if plot_handle is None:
        pl.close('all')
        # Create a new (empty) figure
        figure_handle = pl.figure()

        if num_attributes == 2:
            plot_handle = figure_handle.add_subplot(111)
        else:
            plot_handle = list()
        pl.ion()
        pl.show()

        if output is not None and num_attributes == 2:
            indices_label1 = np.nonzero(output)[0]
            indices_label0 = np.nonzero(1 - output)[0]

            plot_handle.plot(input[indices_label0, 0], input[indices_label0, 1], 'bo')
            plot_handle.plot(input[indices_label1, 0], input[indices_label1, 1], 'ro')
            plot_handle.axis([-0.5, 1.5, -0.5, 1.5])

            line_handle, = pl.plot([], [], 'k')

    if not parameters is None and num_attributes == 2:
        x0 = np.array([-0.5, 1.5])

        y1 = (parameters[-1] - parameters[0] * x0) / parameters[1]
        line_handle.set_xdata(x0)
        line_handle.set_ydata(y1)
        y2 = (-500 + parameters[-1] - parameters[0] * x0) / parameters[1]
        if not fill_handle is None:
            fill_handle.remove()

        fill_handle = plot_handle.fill_between(x0, y1, y2, facecolor='blue', alpha=0.5)
    elif num_attributes > 2:
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
                if output is not None:
                    if output[n] == 1:
                        title_str = "Odd"
                    elif output[n] == 0:
                        title_str = "Even"

                n += 1
                plot_handle.append(figure_handle.add_subplot(num_rows, num_cols, n))
                plot_handle[-1].imshow(im)
                plot_handle[-1].xaxis.set_visible(False)
                plot_handle[-1].yaxis.set_visible(False)
                if title_str is not None:
                    plot_handle[-1].set_title(title_str)

    pl.pause(0.1)
    time.sleep(0.1)


# Mystery visualisation function
#
def show_Jplot(w1range, w2range, J):
    w1grid = np.zeros((len(w1range), len(w2range)))
    w2grid = np.zeros((len(w1range), len(w2range)))
    for i in range(len(w1range)):
        for j in range(len(w2range)):
            w1grid[i, j] = w1range[i]
            w2grid[i, j] = w2range[j]

    pl.close('all')
    figure_handle = pl.figure()
    axis_handle = Axes3D(figure_handle)
    axis_handle.plot_surface(w1grid, w2grid, J)
    axis_handle.view_init(elev=25, azim=30)
    pl.xlabel(r'$w_1$')
    pl.ylabel(r'$w_2$')
    pl.title(r'$J$')
    pl.show()
