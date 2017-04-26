import perceptron
import numpy as np


# Binary input, formated as a matrix, with each column correspnding to different attribute (there are two) and each
# row cooresponding to different sample to learn from (there are four)
x = np.array([[0, 0],
              [0, 1],
              [1, 0],
              [1, 1]])

# True output for the above input implementing the boolean AND function - output is one when both inputs are one.
y = np.array([0,
              1,
              1,
              1])

num_points, _  = x.shape
wrange = np.linspace(-1,1,100)
#0.01935724  0.0325014   0.04728984
J = np.zeros((len(wrange), len(wrange)))
w0 = 0.05
for i in range(len(wrange)):
    w1 = wrange[i]
    for j in range(len(wrange)):
        w2 = wrange[j]
        w = np.array([w1, w2, w0])
        yhat = perceptron.hypothesis(input=x, parameters=w)
        nErrors = 0
        for n in range(num_points):
            e = y[n]-yhat[n]
            if e != 0.0:
                J[i,j] += 1

perceptron.show_Jplot(w1range=wrange, w2range=wrange, J=J)