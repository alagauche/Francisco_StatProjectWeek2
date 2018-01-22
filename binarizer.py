import pandas as pd, numpy as np
import os, math

def binarize(item, validation_cutoff):
    if item <= 1:
        if item >= validation_cutoff:         
            return math.ceil(item)         
        else:
            return math.floor(item)
    else:
        return item

 
# global variables
validation_cutoff = 0.9
dir_path = os.path.dirname(os.path.realpath(__file__))

set_number = "10"
subm = pd.read_csv(dir_path + '/' + 'submission_10.csv')
subm = subm.applymap(lambda x: binarize(x, validation_cutoff))
subm.to_csv('binarized_' + set_number + '.csv', index=False)



