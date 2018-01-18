import pandas as pd, numpy as np
import os, math

def binarize(item, validation_cutoff, maybe_counter):
    if item <= 1:
        if item >= validation_cutoff:         
            return math.ceil(item)         
        else:
            if item > maybe:
                maybe_counter += 1
            return math.floor(item)
    else:
        return item

 
# global variables
validation_cutoff = 0.9
dir_path = os.path.dirname(os.path.realpath(__file__))

subm = pd.read_csv(dir_path + '/' + 'submission.csv')

subm = subm.applymap(lambda x: binarize(x, validation_cutoff))
subm.to_csv('submission_binarized.csv', index=False)



