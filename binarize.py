import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

from rocCurve import plot_roc_curve

"""
https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
ROC curve and area on multi-class data => binarize the output
"""


def binarize_output(labels):
    """

    :param labels: data labels
    :return: binarized data labels
    """
    unique_labels = labels.unique()
    binarized_labels = label_binarize(labels, classes=unique_labels)
    return binarized_labels


if __name__ == "__main__":
    data = pd.read_csv("./data/mbti_1.csv", header=0)

    X = data['posts']
    y = data['type']
    class_names = y.unique()

    # Binarize the output
    y = binarize_output(y)
    n_classes = y.shape[1]

    # shuffle and split training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.4,
                                                        random_state=0)

    text_clf = Pipeline([('vect', CountVectorizer(stop_words='english')),
                         ('tfidf', TfidfTransformer()),
                         ('clf', MultinomialNB()),
                         ])

    plot_roc_curve(text_clf, class_names, n_classes, X_train, X_test, y_train, y_test)
