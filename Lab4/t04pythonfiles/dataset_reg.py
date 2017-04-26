import pylab as pl
import numpy as np
import inspect, os
import matplotlib
import matplotlib.pyplot as pl
import time
import sys

# Global handles for the plot (necessary for plot animation)
figure_handle = None
plot_handle = None
line_handle = None
scatter_handle = None

# Reads data from file
#
# Input: name of the file to read from
#
# Output: (x,y) - tuple with input and corresponding true output samples

def read(name):

    #Load data from file found in the same directory where this script resides
    workingDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    npzfile = np.load(os.path.join(workingDir, name))
    # Extract input and target output samples
    x = npzfile['x']
    y = npzfile['y']

    return (x,y)

# Plots data
#
# Input: input: input values
#        output: output values
#        type: 'scatter' or 'line' - the latter draws a line through the points
def show(input, output, type='scatter'):
    global figure_handle, plot_handle, line_handle, scatter_handle

    if plot_handle is None:
        pl.close('all')
        # Create a new (empty) figure
        figure_handle = pl.figure()
        plot_handle = figure_handle.add_subplot(111)
        pl.ion()
        pl.show()


    if scatter_handle is None and type=="scatter":
        scatter_handle = pl.plot(input, output, 'k.')
        plot_handle.axis([np.min(input), np.max(input), np.min(output), np.max(output)])
    elif type=="line":
        if line_handle is None:
            line_handle, = pl.plot(input, output, 'b-')
        else:
            line_handle.set_xdata(input)
            line_handle.set_ydata(output)

    plot_handle.set_xlabel('x')
    plot_handle.set_ylabel('y')
    pl.pause(0.01)
    time.sleep(0.01)
