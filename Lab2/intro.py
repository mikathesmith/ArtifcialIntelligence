# These commands import some of the scipy libraries we'll be using.
import pylab as pl
import numpy as np

# Define a uniformly spaced set of x values (n in total)
n = 50
x = np.linspace(0, 4, n)

# Define a set of corresponding y values
a = 2
b = 1
y = a * x + b

# Close any open figures, and start a new one
pl.close('all')
# Create a new (empty) figure
pl.figure()

# Plot the function (in greeen)
pl.plot(x, y, 'g')

# Add a legend and axis labels
pl.legend(['my function'])
pl.xlabel('x')
pl.ylabel('y')

# Display the figure
pl.show()
b