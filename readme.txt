Name: Francisco McGee
Assignment: Stats Project, Week2
Github: https://github.com/alagauche/Francisco_StatProjectWeek2

OVERVIEW
This project takes comments from Wikipedia talk page edits and classifies each comment by toxicity in the following categories:
    1) toxic
    2) severely toxic
    3) insult
    4) obscene
    5) threat
    6) identity_hate
The predictive model used to classify the comments is NBSVM, naive bayes support vector machines.


SOURCE OF ALGORITHM, NBSVM
I took this NBSVM (naive bayes support vector machines) implementation from a Kaggle competition kernel:
Specific NBSVM implementation, by Jeremy Howard:
    https://www.kaggle.com/jhoward/nb-svm-strong-linear-baseline-eda-0-052-lb   
Kaggle Challenge Homepage, Toxic Comment Classification Challenge
    https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge
Academic paper introducing NBSVM 
    https://nlp.stanford.edu/pubs/sidaw12_simple_sentiment.pdf


NOTE ON SCALABILITY/LIMITATIONS
Currently, pipeline must be run manually due to current memory scaling limitations during model construction.
The file toxic_comments_nbsvm.py runs the model, and is the main culprit in scaling limitation.
In the meantime, this function will stress a computer with 16GB memory.
Only by halving the dataset was I able to run it locally running a single model.


WORKFLOW
The workflow needs to be run 10 times from steps 2-4 in order to cross-validate. Automated 10-fold cross-validation is currently precluded by scaling limitations.



HOW TO RUN THE CODE
Run these files in order:
(1) generate_sets.py
    - Splits train.csv into training and testing sets
    - This is because test.csv has empty calls, unusable for validation
    - Scaling limitations meant that the dataset had to be halved
    - Output: training_set_1.csv and testing_set_1.csv
(2) toxic_comments_nbsvm.py
    - Runs the nbsvm algorithm on output from (1) above
    - Output: submission.csv
(3) binarizer.py
    - The output for each entry in submission.csv is between 0 and 1
    - Binarizer.py floors and ceils each value according to a threshold
    - For now, the threshold is 0.9
    - Validation is simplified by binarizing each toxicity call
    - Output: submission_binarized.csv
(4) validator.py
    - Right now, the only stat calculated is accuracy by toxicity category 
    - Accuracy = successful calls / total calls
    - Only one accuracy per category
    - Output: results are printed to console


