# -*- coding: utf-8 -*-
import pandas as pd, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))


# import the files
set_number = "2"
train = pd.read_csv(dir_path + '/' + 'training_set_' + set_number + '.csv')
test = pd.read_csv(dir_path + '/' + 'testing_set_' + set_number + '.csv')
subm = pd.read_csv(dir_path + '/' + 'sample_submission.csv')


# skipped vis/analysis code

label_cols = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
train['none'] = 1-train[label_cols].max(axis=1)
train.describe()

# remove empty comments
COMMENT = 'comment_text'
train[COMMENT].fillna("unknown", inplace=True)
test[COMMENT].fillna("unknown", inplace=True)

# building the model
import re, string
re_tok = re.compile('([' + string.punctuation + '“”¨«»®´·º½¾¿¡§£₤‘’])')

def tokenize(s): return re_tok.sub(r' \1 ', s).split()

# use TF-IDF; better accuracy than CountVectorizer
# create sparse matrix with small number of non-zero elements
# this code takes some time, but is not the bottleneck
n = train.shape[0]
vec = TfidfVectorizer(ngram_range=(1,2), tokenizer=tokenize,
               min_df=3, max_df=0.9, strip_accents='unicode', use_idf=1,
               smooth_idf=1, sublinear_tf=1 )
trn_term_doc = vec.fit_transform(train[COMMENT])
test_term_doc = vec.transform(test[COMMENT])

# NB feature equation
# this code will extract log-count ratios from the ngram vectors, 
# turning them into features, which get plugged into the logistic regression
def pr(y_i, y):
    p = x[y==y_i].sum(0)
    return (p+1) / ((y==y_i).sum()+1)
    
x = trn_term_doc
test_x = test_term_doc

# fit a model for one dependent at a time
# this is probably the longest running function in the code
def get_mdl(y):
    y = y.values
    r = np.log(pr(1,y) / pr(0,y))
    m = LogisticRegression(C=4, dual=True)
    x_nb = x.multiply(r)
    return m.fit(x_nb, y), r

# make a matrix of zeros to plug results into 
preds = np.zeros((len(test), len(label_cols)))

# longest run time of code
# duration probably due to get_mdl, but could be the actual prediction
# this loop calculates the number that goes in each cell
for i, j in enumerate(label_cols):
    print('fit', j)
    m,r = get_mdl(train[j])
    preds[:,i] = m.predict_proba(test_x.multiply(r))[:,1]


submid = pd.DataFrame({'id': subm["id"]})
submission = pd.concat([submid, pd.DataFrame(preds, columns = label_cols)], axis=1)
submission.to_csv('submission_' + set_number + '.csv', index=False)

