Name: Francisco McGee
Assignment: Stats Project, Week2
Github: https://github.com/alagauche/Francisco_StatProjectWeek2

NOTE ON SCALABILITY/LIMITATIONS
Currently, pipeline must be run manually due to current scaling limitations.
These can be resolved shortly. 
toxic_comments_nbsvm.py is the main culprit.
In the meantime, this function will stress a computer with 16GB memory.
Only by halving the dataset was I able to run it locally.

SOURCE OF ALGORITHM, NBSVM
I took this NBSVM (naive bayes support vector machines) implementation from Kaggle:
Specific NBSVM implementation, by Jeremy Howard:
    https://www.kaggle.com/jhoward/nb-svm-strong-linear-baseline-eda-0-052-lb   
Kaggle Challenge Homepage
    https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge

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


