import pandas as pd
import os, math


def generate_set(training_set, train_percent, total_percent):
    sets = []
    training_set = training_set.sample(frac = 1)
    
    total_count = int(math.floor(training_set.shape[0] * total_percent))
    training_count = int(math.floor(total_count * train_percent))
    
    new_training_set = training_set[0:training_count]
    testing_set = training_set[training_count:total_count]
    sets.append(new_training_set)
    sets.append(testing_set)
    return sets
    
    
    
# generate all training/testing sets as list of sets[training set, testing set]
def generate_sets(training_set, train_percent, set_count):
    all_sets = []
    for i in range (0, set_count):
        all_sets.append(generate_set(training_set, train_percent))
    return all_sets
    


# set global variables
dir_path = os.path.dirname(os.path.realpath(__file__))
training_percent = 0.7
total_percent = 0.5
set_number = "10"

# import datasets
train = pd.read_csv(dir_path + '/' + 'train.csv')

# generate training, testing sets
sets = generate_set(train, training_percent, total_percent)
testing_set = sets[1]

# zero out the columns for the testing set
testing_set['toxic'] = 0
testing_set['severe_toxic'] = 0
testing_set['obscene'] = 0
testing_set['threat'] = 0
testing_set['insult'] = 0
testing_set['identity_hate'] = 0

# output training and testing sets to csv
training_name = "training_set_" + set_number + ".csv"
testing_name = "testing_set_" + set_number + ".csv"
sets[0].to_csv(training_name, index=False)
testing_set.to_csv(testing_name, index=False)

