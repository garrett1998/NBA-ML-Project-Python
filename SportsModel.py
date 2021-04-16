# Copyright William Garrett White @ 2020 - 2021 [Educational use only]
import csv as csv
import numpy as np
# Module Imports

class Model():

    h0_layer = np.array([])
    h1_layer = np.array([])
    final_weights = np.array([])
    # Declaring numpy arrays to store data throughout the training and testing process

    def normalization(self, value, min_value, max_value):
        return (value - min_value) / (max_value - min_value)
        # Function that normalizes the value between 0 and 1 based on the objective minimum and maximum possible value.
        # For example, one of the features in the model is the military time of the game being played.
        # If the game time is the stat being normalized, example value = 1400;
        # example min_value = 0100; example max_value = 2400; Therefore, the normalized value would be 0.565...


    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
        # Math function that is predefined to use later in the backpropagation.


    def sigmoid_derivative(self, x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))
        # Math function that is predefined to use later in the backpropagation.


    def train_back(self, training_input, target_output, h0_weights, h1_weights, output_weights, eta_value):
        # Backwards propagation function

        single_input = np.array(training_input)
        h0_weights_array = np.array(h0_weights)
        h1_weights_array = np.array(h1_weights)
        output_weights_array = np.array(output_weights)
        # Because the arguments in the function are <list> type, we need to transform those in to numpy arrays.

        for x in range(3, 6):
            if x == 3:
                training_input[x] = self.normalization(training_input[x], 100, 2400)
            if x == 4:
                training_input[x] = self.normalization(training_input[x], 0, 7)
            if x == 5:
                training_input[x] = self.normalization(training_input[x], 0, 7)
        # Using a for loop to normalize training inputs 3, 4, and 5
        # because all the other features are in a format from 0 to 1.

        training_example_output = self.think_forward(training_input, h0_weights, h1_weights, output_weights)
        training_example_error = target_output - float(training_example_output)
        # After running the think forward function, we store the guessed output in variable
        # and get the error by subtracting it from the target/actual output.

        h0_weights_error = np.dot(h0_weights_array, training_example_error)
        h1_weights_error = np.dot(h1_weights_array, training_example_error)
        output_weights_error = np.dot(output_weights_array, training_example_error)
        # Getting the error with respect to the hidden weights in the model and storing them in variables^

        for x in range (4):
            adjustments = eta_value * h0_weights_error[x] *\
                                   self.sigmoid_derivative(self.h0_layer[x]) * single_input.T
            h0_weights_array[x] += adjustments
        for x in range (2):
            adjustments = eta_value * h1_weights_error[x] *\
                                   self.sigmoid_derivative(self.h1_layer[x]) * self.h0_layer.T
            h1_weights_array[x] += adjustments
        for x in range(1):
            adjustments = eta_value * output_weights_error[x] * self.sigmoid(training_example_output) * self.h1_layer.T
            output_weights_array[x] += adjustments
        # Using a series of for loops to run essentially the main back propagation
        # functions to find the weight adjustments needed for the model to continue training.
        # Then we add the adjustments layer to the weights array declared above ^

        new_weights = np.append(h0_weights_array, h1_weights_array)
        self.final_weights = np.append(new_weights, output_weights_array)
        # Using np.append() to combine all the layers' weights together after training and then setting
        # the combined array to the self.final weights that gets referenced or used in the main runtime function.


    def think_forward(self, input, h0_weights, h1_weights, output_weights):
        # Forwards propagation function
        self.h0_layer = np.array([])
        self.h1_layer = np.array([])
        output_layer = np.array([])
        # Declaring arrays to use as hidden and output layers in the function

        for x in range(4):
            h0_node = self.sigmoid(np.dot(input, h0_weights[x]))
            self.h0_layer = np.append(self.h0_layer, h0_node)
        for x in range(2):
            h1_node = self.sigmoid(np.dot(self.h0_layer, h1_weights[x]))
            self.h1_layer = np.append(self.h1_layer, h1_node)
        for x in range(1):
            output_node = self.sigmoid(np.dot(self.h1_layer, output_weights[x]))
            output_layer = np.append(output_layer, output_node)
        # Using a series of for loops to multiply forward the the values, weights, and nodes in the function.

        return output_layer
        # returning the final output


    def test_data(self, input, h0_weights, h1_weights, output_weights):
        # Data testing function
        # (essentially the same as 'think_forward' but modified for different argument data types.)

        single_input = np.array(input)
        h0_weights_array = np.array(h0_weights)
        h1_weights_array = np.array(h1_weights)
        output_weights_array = np.array(output_weights)
        # Converting the arguments from lists into arrays

        self.h0_layer = np.array([])
        self.h1_layer = np.array([])
        output_layer = np.array([])
        # Declaring hidden and output layers to use in forward propagation

        for x in range(4):
            h0_node = self.sigmoid(np.dot(single_input, h0_weights_array[x]))
            self.h0_layer = np.append(self.h0_layer, h0_node)
        for x in range(2):
            h1_node = self.sigmoid(np.dot(self.h0_layer, h1_weights_array[x]))
            self.h1_layer = np.append(self.h1_layer, h1_node)
        for x in range(1):
            output_node = self.sigmoid(np.dot(self.h1_layer, output_weights_array[x]))
            output_layer = np.append(output_layer, output_node)
        # Again, all the same multiplying/forward propagation code in 'think_forward' but the main
        # difference is we had to change the list values at the beginning of the function into numpy arrays.

        return output_layer
        # Returning the testing output


    def readme(self):
        # Readme function

        print(
            ''' 
            ==============================================================================
            |     NBA Game Neural Net by William Garrett White Copyright @2020-2021      | 
            | -------------------------------------------------------------------------- | 
            |    This machine learning model will train and learn how to predict the     | 
            |                       outcome of certain NBA games.                        | 
            |                                                                            | 
            |      The outcome will be a decimal number between 0.00 and 1.00.           |
            |  The outcome is the predicted probability that the 'HOME' team will win.   |
            |                                                                            |
            |                The model will have 8 features per game and                 |
            |  2 Hidden layers. The first one with 4 nodes and the second with 2 nodes   | 
            |               and the final output layer described above ^                 |
            |                                                                            |
            |                 Thank you so much for using the program!                   |
            |                         -Ω.Ω. (William G. White)                            |
            ==============================================================================
            '''
        )
        # This is the prompt to the user at the very beginning of the program
        # that explains what the program does and what is to be expected.
