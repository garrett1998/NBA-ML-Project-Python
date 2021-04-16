# Copyright William Garrett White @ 2020 - 2021 [Educational use only]

import numpy as np
from SportsModel import Model as model
from WebScraper import scrape as scraper
import csv as csv
import random as rand
# Importing Modules

if __name__ == "__main__":
    # main function that runs first

    model = model()
    scraper = scraper()
    # Creating instances of other modules used in this main script

    training_data = 'csv_basketball_reference.csv'
    # Defining the file path to the labeled training data

    h0_weights = []
    h1_weights = []
    output_weights = []
    # Weight lists

    input_data = []
    output_data = []
    # Data lists
    # Defining global lists for the weights and labeled data.

    def finalized_weights_to_csv(weights_at_the_end_of_training):
        all_h0_weights = np.array([])
        all_h1_weights = np.array([])
        all_output_weights = np.array([])
        # Declaring arrays to save weights at the end of training

        for x in range(32):
            all_h0_weights = np.append(all_h0_weights, weights_at_the_end_of_training[x])
        for x in range(32, 40):
            all_h1_weights = np.append(all_h1_weights, weights_at_the_end_of_training[x])
        for x in range(40, 42):
            all_output_weights = np.append(all_output_weights, weights_at_the_end_of_training[x])
        # The for loops are formatted this way because of the way the weights save at the end of training.
        # The finalized weights are just made into a 1 dimensional np.array() and because I know the indexes of the
        # weights for each layer I just use a for loop to seperate all the weights into each of their respective layers.

        all_h0_weights = np.split(all_h0_weights, 4)
        all_h1_weights = np.split(all_h1_weights, 2)
        # Using the np.split() function to separate the weights into the weights according to their nodes.

        csv_file = open('weights.csv', 'w')
        csv_writer = csv.writer(csv_file)
        # csv code needed to write file.

        for x in range(4):
            csv_writer.writerow(all_h0_weights[x])
        for x in range(2):
            csv_writer.writerow(all_h1_weights[x])
        csv_writer.writerow(all_output_weights)
        # writing the weights to rows of the csv file opened from above.

        csv_file.close()
        # Closing file. Self explanatory lol


    def training_data_parser():
        csv_file = open(training_data, 'r')
        reader = csv.reader(csv_file)
        next(reader)
        # Opening the csv file w/ the training data and skipping over the
        # first row of data that only contains the column labels.

        for row in reader:
            single_row = []
            for x in range(3, 11):
                single_row.append(row[x])
            input_data.append(single_row)
            output_data.append(row[11])
        # Using a for loop to add each value in each column of data
        # to both the input and output data lists.

        csv_file.close()
        # Closing the file when finished.

        for x in range(0, len(input_data)):
            for y in range(0, 8):
                input_data[x][y] = float(input_data[x][y])
        for x in range(0, len(output_data)):
            output_data[x] = float(output_data[x])
        # I need to have the all data in float format to keep a
        # consistent data type for when the math is computed later.
        # These for loops are for taking the float literal of each data value.


    def csv_weights_reader(path):

        csv_file = open(path, 'r')
        reader = csv.reader(csv_file)
        # Opening the csv file for reading

        count = 0
        for row in reader:
            if count < 4:
                h0_weights.append(row)
            if 4 <= count < 6:
                h1_weights.append(row)
            if 6 <= count < 7:
                output_weights.append(row)
            count += 1
        # Using a for loop and an outside loop counter to add each row of synaptic
        # weights to the corresponding layers list used for storing the weights.

        csv_file.close()
        # Closing the csv file

        for x in range(0, len(h0_weights)):
            for y in range(0, 8):
                h0_weights[x][y] = float(h0_weights[x][y])
        for x in range(0, len(h1_weights)):
            for y in range(0, 4):
                h1_weights[x][y] = float(h1_weights[x][y])
        for x in range(0, len(output_weights)):
            for y in range(0, 2):
                output_weights[x][y] = float(output_weights[x][y])
        # As stated before, I need all of these value to be in float format.
        # These 'for' loops are to take the float literals of each of these values
        # which are now technically stored in layer weights lists. Hence the indexing
        # when referencing the value in the lists. (Example: h0_weights[0][3])


    def csv__random_weights_writer(path):
        csv_file = open(path, 'w')
        csv_writer = csv.writer(csv_file)
        # Opening the csv file (if one is not created it will make one with the specified file path)

        h_00 = []
        h_01 = []
        h_02 = []
        h_03 = []
        h_10 = []
        h_11 = []
        o_o = []
        # Declaring lists for each node of the NN.
        # There is probably an easier way to do this ^ but
        # declaring all of these lists on one line kept throwing me errors.

        for x in range(0, 8):
            h_00.append(rand.uniform(0, 1))
            h_01.append(rand.uniform(0, 1))
            h_02.append(rand.uniform(0, 1))
            h_03.append(rand.uniform(0, 1))
        csv_writer.writerow(h_00)
        csv_writer.writerow(h_01)
        csv_writer.writerow(h_02)
        csv_writer.writerow(h_03)
        # Creating 4 random numbers between 0 and 1 and adding them to the
        # space for each node in the first hidden layer. The naming convention
        # is h = hidden layer; _ = just a separator; first number 0 = the 0th layer (or the first layer);
        # and the second number h_01 ... 1 = the second node in the first layer;

        for x in range(0, 4):
            h_10.append(rand.uniform(0, 1))
            h_11.append(rand.uniform(0, 1))
        csv_writer.writerow(h_10)
        csv_writer.writerow(h_11)
        # Using the same naming convention described above, creating two
        # random numbers and added them to nodes in the second hidden layer

        for x in range(0, 2):
            o_o.append(rand.uniform(0, 1))
        csv_writer.writerow(o_o)
        # Lastly creating a random number set for the weights that will make the output neuron or the 'output layer'.
        # o_o = output layer/neuron; Because it's the last result I used 'o_o' instead
        # of zeros to signify its importance and difference from the other neurons.

        csv_file.close()
        # Closing the csv file


    def error_handler():
        print('Oops! You entered an invalid entry. The program will end and you will need to restart.')
        exit()
        # Simple print statement that I use multiple times in the program.
        # Because of that, I just created it's own function:)


    def main_function():
        print(''' 
                     -------------------------------------------
                    |    To start, would you like to update     |
                    |          the current game data?           |
                    | _________________________________________ |
                    |        Enter 'y/n' - yes or no? :         |
                     -------------------------------------------
                    ''')
        choice = input()
        # Prompting the user whether or not they want to update the data being used

        if choice == 'y':
            scraper.GET_and_WRITE_data()
            print('The program has finished updating the data and will close now. Thanks so much!')
            print('-Ω.Ω.')
            quit()
            # If the answer is yes, I call the web scraper module's main function and because it
            # takes a while and because of the way I formatted the program,
            # the user will need to restart and enter 'n' on this section in order to continue.
            # New data is available once every day so prior to testing
            # anything the user should update and retrain new data if needed.

        if choice == 'n':
            print('Okay, let us keep going :) ')
            # Assuming all data is retrieved, the program continues

        else:
            error_handler()
            # Calling error handling script which will require a restart.

        training_data_parser()
        # Because we are assuming that all data is retrieved,
        # we are calling the training data parser to load all relevant
        # data into the lists declared at the very top of the program.

        print(''' 
             -------------------------------------------
            |    Now would you like random weights      |
            |   for all features to train the model ?   |
            |      Or input data manually for all       |
            |    synaptic weights to test the model?    |
            | _________________________________________ |
            |    Enter 'r' for random or 'm' manual :   |
             -------------------------------------------
            ''')
        starting_weight_prompt_value = str(input())
        # Asking the user whether or not they want random weights
        # (to then train the model), or manual weights (to then test the model).

        if starting_weight_prompt_value == "r":
            print(''' 
                                     -------------------------------------------
                                    |  We are starting with random weights to   |
                                    |    train the model. We will need to a     |
                                    |     file to save to once we are done.     |
                                    |   By default, the file will save to the   |
                                    |           main project folder.            |
                                    | _________________________________________ |
                                    |    Enter the preferred file name here :   |
                                     -------------------------------------------
                                    ''')
            csv_path = input('=')
            csv__random_weights_writer(csv_path)
            # User has chosen to train the model with random weights and enters the desired path of the csv file.
            # The function will create a csv file with random weights
            # and will show up as a sibling to all the other files in the main project folder/directory.

            print('The random weights have been created!')
            print('Given that you started w/ random weights, we are going to continue by training the model.')
            print('Please enter the amount of iterations to be trained: ')
            rotations = input()
            # Prompting the user that we will be training and they need
            # to enter how many epochs or training iterations they would like.

            print('Now enter the desired learning rate: (example: a value between 0.001 - 0.100')
            learn = input()
            # The user will input the learning rate,
            # (which determines how fast the training occurs after each training example)

            print('Okay we will begin training the model. Please wait a while for this to occur.')
            csv_weights_reader(csv_path)
            # Because we just wrote the file earlier in the program, we still need to
            # read the csv we just wrote with random weights. Because of this,
            # we are calling csv_weights_reader.

            for x in range(0, int(rotations)):
                training_example_index = x % len(input_data)
                # 'training_example_index' is created because the training iterations is not dependent on the
                # size of data collected for training. Meaning if the user wanted an odd number of iterations
                # its possible that the training example used at the end of the program could be something random.
                # For example, if we had 1000 training examples and the user wanted 1500 iterations,
                # the training would end on training example no. 500.

                model.train_back(input_data[training_example_index], output_data[training_example_index],
                                 h0_weights, h1_weights, output_weights, float(learn))
                # This for loop handles all of the training based
                # on how many iterations the user chose (referenced above)
            # Training done single training data row by single training data row.

            finalized_weights_to_csv(model.final_weights)
            # Calls the function defined above to write the weights at the end of training to csv file.

            print('Training is complete! The weights at the end of training are saved to (weights.csv).')
            print('To save the weights for later, rename the file in the project directory.')
            print('Otherwise when you run the program again (weights.csv) will be overridden.')
            # Prompting the user that training is done and they will need to restart to do testing.

            print('The model has finished! Thanks so much!')
            print('-Ω.Ω.')
            quit()
            # Prompting the user that the program will quit.

        elif starting_weight_prompt_value == "m":
            print(''' 
                         -------------------------------------------
                        |  Okay! This program takes in weights from |
                        |   a .csv file format. You will need to    |
                        |      enter a file path for your file.     |
                        | _________________________________________ |
                        |         Enter the file path here :        |
                         -------------------------------------------
                        ''')
            csv_path = str(input('='))
            csv_weights_reader(csv_path)
            # Calling the csv weights reader function for the manual weights.

            print('Great!')
            while True:
                print('We can now enter new values to predict... ')
                away_team_name = input('Enter the away team name:')
                home_team_name = input('Enter the home team name:')
                major_event = input('Enter a 1 if a major event occurred in the past 3 days (or 0 if not):')
                game_times = input('Enter the time of the game (Military hour format: 1400, 2100, etc.):')
                away_inactives = input('Enter the amount of away inactives:')
                home_inactives = input('Enter the amount of home inactives:')
                away_win_percentage = input('Enter the away team win %: 0.341, 0.761, etc.:')
                home_win_percentage = input('Enter the home team win %: 0.410, 0.822, etc.:')
                # Prompting the user on all of the values needed and storing the responses in the appropriate variables

                testing_example = np.array([0.0, 1.0, float(major_event),
                                            model.normalization(float(game_times), 100, 2400),
                                            model.normalization(float(away_inactives), 0, 7),
                                            model.normalization(float(home_inactives), 0, 7),
                                            float(away_win_percentage), float(home_win_percentage)])
                # Declaring an array with all of the info we just received

                guess = model.test_data(testing_example, h0_weights, h1_weights, output_weights)
                # calling the model.test_data() function to use the current weights to
                # make a guess on the outcome of the NBA game.

                print('The model predicts that ' + str(home_team_name)
                      + ' has a ' + str(guess) + ' chance of winning AND...')
                print('The model predicts that ' + str(away_team_name)
                      + ' has a ' + str((1 - guess)) + ' chance of winning :)')
                # Finally we prompt the user with what our model predicted represented
                # a decimal number meant to represent the percentage predicted of the event happening.

                answer = input('To quit press q, to keep trying new data press c: ')
                if answer == 'q':
                    print('Thanks so much for using the program :) Have a great day!')
                    print("Ω~Ω")
                    quit()
                if answer == 'c':
                    print('Okay great!')
                else:
                    error_handler()
                # Because all the code above is in a while loop we need to let the user decide when to exit the loop.
                # We prompt the user whether or not they would like to continue and use
                # the response to determine what to do going forward.
        else:
            error_handler()
        # Because most of this is still within the statement that gets whether or not the user enters 'r' or 'm',
        # this else statement is here in case when prompted about the weights the user enters an incorrect value.


    model.readme()
    main_function()
    # Because everything above are just function and variable definitions,
    # we still need to call the main function to run everything together.
    # We also prompt the user with the explanation/readme prompt prior to starting the program.