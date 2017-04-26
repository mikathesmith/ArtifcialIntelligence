import numpy as np
import math
import math
import sys


# A class implementing a polynomial hypothesis + steppest gradient training
#
# The hypothesis is of the form:
#  h(x) = w_0 + w1*x + w2*x^2 + ... + wk*x^k
class polynomial:
    # When initialising the hypothesis, you can specify the degree of the polynomial.
    #
    # Input: k - degree of the polynomial.
    def __init__(self, k):
        self.k = k
        # The number of parametrs depends on the degree of polynomial - initialise to
        # random values draw from normal distribution
        self.w = np.random.normal(0.0, 1.0, k + 1)

    # Computes the output of the hypothesis
    #
    # Input: input - input data, a Nx1 vector where N is the number of input points (assuming 1-attribute input)
    #
    # Output: output - Nx1 vector of outputs h(x)
    def output(self, input):
        num_points = input.shape[0]

        # Create output array of num_points
        output = np.zeros((num_points,))

        for n in range(0, num_points, 1):
            for j in range(self.k + 1):
                output[n] += self.w[j] * math.pow(input[n], j)

        return output

    # Single epoch of steepest gradient descent - modifies the parameters of the hypothesis
    #
    # Input: input - input data, a Nx1 vector where N is the number of input points (assuming 1-attribute input)
    #        true-output - desired output, a Nx1 vector where  N is the number of points - each true_output[n] gives
    #                      the desired output for input[n]
    #        alpha - learning rate
    def learn(self, input, true_output, alpha):
        # How many points in the input
        num_points = input.shape[0]

        # Compute the output of the hypothesis
        output = self.output(input)

        # Initialise an array that contain the parameter changes - set them to zero at first
        delta_parameters = np.zeros((self.w.size,))

        # The cost over the entire training set - set it to zero at first
        J = 0

        # Compute errors and parameter changes based on each input-true-output pair
        for n in range(0, num_points, 1):
            # Compute the residual error of the nth output
            error = true_output[n] - output[n]
            # Add the square of the error to the total cost
            J += error * error
            # Compute the parameter updates based on steepest gradient rule for MSE cost
            for j in range(self.k + 1):
                delta_parameters[j] += math.pow(input[n], j) * error

        # Update the parameters with the average of parameter changes over num_points multiplied by the learning factor.
        # If num_points is one, the average is just the entire update due to one (input,target_ouptut) pair.
        self.w += alpha * delta_parameters / float(num_points)

        # Return the average MSE
        return J / num_points
