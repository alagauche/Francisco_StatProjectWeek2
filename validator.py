import pandas as pd
import os

def get_validation_key(set):
    validation_key = set.set_index('id').T.to_dict('list')
    return validation_key


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
    
    
def validate_by_columns(test_binarized, validation_key, headers):
    raw_stats = get_raw_stats_dict(headers)
    
    for column in test_binarized:
        if column == "id":
            continue
        raw_stats[column] = validate_column(column, validation_key, raw_stats)
        
    return raw_stats
    
    
def validate_column(column, validation_key, raw_stats):
    # header stats: true positive, true negative, false positive, false negative
    # dataset stats: all calls, not found, calls made
    #0, 1   2   3   4   5   6
    tp = tn = fp = fn = ac = nf = cm = 0
    key_index = 0
    column_stats = []

    for index, value in test_binarized[column].iteritems():
        ac += 1
        comment_id = test_binarized["id"].loc[index]
        correct_call = validation_key[comment_id]
        print correct_call
        print "about to check: ", comment_id
        try:
            correct_call = validation_key[comment_id][key_index]
            print comment_id
            if value == 1:
                if value == correct_call:         # true positive
                    tp += 1
                if correct_call == 0:             # false positive
                    fp += 1                       
            if value == 0:
                if value == correct_call:         # true negative
                    tn +=1                        
                if correct_call == 1:             # false negative
                    fn += 1                        
            cm += 1
        except:
            nf += 1
        key_index += 1
       
    column_stats.extend((tp, tn, fp, fn, ac, nf, cm))
    print "column: ", column_stats
    return column_stats
    
    
# create raw stats dictionary
def get_raw_stats_dict(headers):
    raw_stats = {}
    
    for header in headers:
        if header == "id":
            continue
        raw_stats[header] = []
    
    return raw_stats
    
def validate_calls(comment_id, calls, validation_key, headers):
    raw_stats_headers = get_raw_stats_dict(headers)
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

    return stats


def get_accuracy(stats):
    # 0,  1   2   3   4   5   6
    #tp, tn, fp, fn, ac, nf, cm
    tp = stats[0]
    tn = stats[1]
    fp = stats[2]
    fn = stats[3]
    accuracy = (tp + tn) / (tp + tn + fp +fn)
    return accuracy
    
def get_missclassification(stats):
    tp = stats[0]
    tn = stats[1]
    fp = stats[2]
    fn = stats[3]
    missclassification = (fp +fn) / (tp + tn + fp +fn)
    return missclassification
    
# aka recall
def get_sensitivity(stats):
    tp = stats[0]
    fn = stats[3]
    sensitivity = tp / (tp + fn)
    return sensitivity
    
def get_specificity(stats):
    tn = stats[1]
    fp = stats[2]
    specificity = tn / (tn + fp)
    return specificity

# aka ppv, positive predictive value
def get_precision(stats):
    tp = stats[0]
    fp = stats[2]
    precision = tp / (tp + fp)
    return precision
    
def get_prevalence(test_original, column):
    prevalence = test_original[column].sum()  
    return prevalence
     
def get_stats_by_column(test_original, raw_stats, headers):
    all_stats = {}    
        
    for header in headers:
        compound_stats = {}
        
        if header == "id":
            continue
        compound_stats["accuracy"] = get_accuracy(raw_stats[header])
        compound_stats["missclassification"]  = get_missclassification(raw_stats[header])
        compound_stats["sensitivity"] = get_sensitivity(raw_stats[header])
        compound_stats["specificity"] = get_specificity(raw_stats[header])
        compound_stats["precision"] = get_precision(raw_stats[header])
        compound_stats["prevalance"] = get_prevalence(test_original, header)
        all_stats[header] = compound_stats
        
    print all_stats
    return all_stats



# set global variables
dir_path = os.path.dirname(os.path.realpath(__file__))
headers = ["id", "toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]
dataset_stats = ["all calls", "not found", "calls made"]


# import datasets
test_original = pd.read_csv(dir_path + '/' + 'train.csv')
test_binarized = pd.read_csv(dir_path + '/' + 'binarized_10.csv')
print test_binarized.head(n= 10)

test_original['id'] = test_original['id'].astype(str)
test_binarized['id'] = test_original['id'].astype(str)

# output validated csv

test_original.drop('comment_text', axis=1, inplace = True)

validation_key = get_validation_key(test_original)
binarized_dict = get_validation_key(test_binarized)
prevalence_toxic = get_prevalence(test_binarized, "toxic")
prevalence_severe_toxic = get_prevalence(test_binarized, "severe_toxic")
prevalence_obscene = get_prevalence(test_binarized, "obscene")
prevalence_threat = get_prevalence(test_binarized, "threat")
prevalence_insult = get_prevalence(test_binarized, "insult")
prevalence_identity_hate = get_prevalence(test_binarized, "identity_hate")


print prevalence_toxic
print prevalence_severe_toxic
print prevalence_obscene
print prevalence_threat
print prevalence_insult
print prevalence_identity_hate

#raw_stats = validate_by_columns(test_binarized, validation_key, headers)
#print raw_stats
#compound_stats = get_stats_by_column(test_original, raw_stats, headers)

#print compound_stats



