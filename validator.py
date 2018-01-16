import pandas as pd
import os

def get_validation_key(set):
    validation_key = set.set_index('id').T.to_dict('list')
    return validation_key

# return validated list of lists
# are the ids here ok??
def validate(test_binarized, validation_key):
    validated = []
    validating = test_binarized.values.tolist()
    
    for row in validating:
        comment_id = row[0]
        calls = row[1:]
        validated_calls = validate_calls(comment_id, calls, validation_key)
        validated_row = new_call_row(comment_id, validated_calls)
        validated.append(validated_row)
        
    return validated
    

def validate_calls(comment_id, calls, validation_key):
    not_found = 0
    validated_calls = []
    for index, value in enumerate(calls):
        try:
            if value == validation_key[comment_id][index]:
                validated_calls.append(1)
            else:
                validated_calls.append(0)
        except:
            not_found += 1
            print not_found, "  Key not found: ", comment_id
        
    return validated_calls

# are the ids here ok??
# no they are not
def new_call_row(comment_id, calls):
    new_row = []
            
    new_row.append(comment_id)
    
    for call in calls:
        new_row.append(call)
    
    return new_row
 
# calculate accuracy of column    
def get_stats(validated, headers):
    stats = {}
    validated_df = pd.DataFrame(validated, columns=headers)
    
    for header in headers:
        if header == "id":
            continue
        else:
            # calc accuracy: successful calls / total calls
            successes = validated_df[header].sum()
            accuracy = successes / len(validated_df.index)
            stats[header] = accuracy
    #print stats
    return stats


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

validation_key = get_validation_key(test_original)
validated = validate(test_binarized, validation_key)
results = get_stats(validated, headers)

print results
'''
for key, value in results.items():
    print "key: ", key
    for item in value:
        print item
'''


