import pandas as pd
import os
     
# set global variables
dir_path = os.path.dirname(os.path.realpath(__file__))
test_mode = 1
headers = ["id", "toxic", "severely toxic", "obscene", "threat", "insult", "identity hate"]


# import datasets
test_original = pd.read_csv(dir_path + '/' + 'train.csv')
test_binarized = pd.read_csv(dir_path + '/' + 'submission_binarized.csv')

test_original['id'] = test_original['id'].astype(str)
test_binarized['id'] = test_original['id'].astype(str)

# output validated csv

test_original.drop('comment_text', axis=1, inplace = True)

print test_binarized.head(n=10)
print test_binarized["id"].loc[0]


# zero indexed

for column in test_binarized:
    if column == "id":
        continue
    for index, value in test_binarized[column].iteritems():
        print "index: ", index, "id: ", test_binarized["id"].loc[index], "value: ", value

