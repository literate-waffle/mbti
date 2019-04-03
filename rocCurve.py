from itertools import cycle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

from scipy import interp

"""
https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
ROC curve and area on multi-class data => binarize the output

ROC curves typically feature true positive rate on the Y axis, and false positive rate on the X axis. 
This means that the top left corner of the plot is the “ideal” point - a false positive rate of zero, and a true 
positive rate of one. This is not very realistic, but it does mean that a larger area under the curve (AUC) is usually
better.

The “steepness” of ROC curves is also important, since it is ideal to maximize the true positive rate while minimizing 
the false positive rate.


ROC curves are typically used in binary classification to study the output of a classifier. In order to extend ROC 
curve and ROC area to multi-class or multi-label classification, it is necessary to binarize the output. One ROC curve 
can be drawn per label, but one can also draw a ROC curve by considering each element of the label indicator matrix as 
a binary prediction (micro-averaging).


https://stats.stackexchange.com/questions/132777/what-does-auc-stand-for-and-what-is-it 
AUC = Area Under the Curve.
AUROC = Area Under the Receiver Operating Characteristic curve.

The AUROC is between 0 and 1, and AUROC = 1 means the prediction model is perfect. In fact, further away the AUROC is
from 0.5, the better: if AUROC < 0.5, then you just need to invert the decision your model is making. As a result, if 
AUROC = 0, that's good news because you just need to invert your model's output to obtain a perfect model.



Note: if you got an AUROC of 0.47, it just means you need to invert the predictions because Scikit-Learn is 
misinterpreting the positive class. AUROC should be >= 0.5.
"""


def binarize_output(output, unique_labels):
    """
    :param output: data to binarize
    :param unique_labels:
    :return: binarized data labels
    """
    binarized_labels = label_binarize(output, classes=unique_labels)
    return binarized_labels


def plot_roc_curve(clf, unique_labels, x_train, x_test, y_train, y_test):

    # In order to extend ROC curve to multi-class classification, it is necessary to binarize the output
    y_train = binarize_output(y_train, unique_labels)
    y_test = binarize_output(y_test, unique_labels)

    n_classes = unique_labels.shape[0]

    # Learn to predict each class against the other
    classifier = OneVsRestClassifier(clf)
    y_score = classifier.fit(x_train, y_train).predict_proba(x_test)

    # Compute ROC curve and ROC area for each class
    fpr = dict()  # false positive rate
    tpr = dict()  # true positive rate
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_score.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

    # Compute macro-average ROC curve and ROC area

    # First aggregate all false positive rates
    all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

    # Then interpolate all ROC curves at this points
    mean_tpr = np.zeros_like(all_fpr)
    for i in range(n_classes):
        mean_tpr += interp(all_fpr, fpr[i], tpr[i])

    # Finally average it and compute AUC
    mean_tpr /= n_classes

    fpr["macro"] = all_fpr
    tpr["macro"] = mean_tpr
    roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

    # Plot all ROC curves
    lw = 2
    fig = plt.figure()
    ax = fig.add_subplot(111)

    colors = cycle(['aqua', 'darkorange', 'cornflowerblue', 'forestgreen', 'goldenrod', '#f4320c',
                    'slateblue', '#5ca904', 'lightgrey', '#af884a', '#75fd63',
                    '#ff5b00', '#cc7a8b', '#3c0008', '#d2bd0a', '#6b8ba4'])
    for i, color in zip(range(n_classes), colors):
        ax.plot(fpr[i], tpr[i], color=color, lw=lw,
                label='ROC of {0} ({1:0.2f})'
                      ''.format(unique_labels[i], roc_auc[i]))

    ax.plot(fpr["micro"], tpr["micro"],
            label='micro-average ROC ({0:0.2f})'
                  ''.format(roc_auc["micro"]),
            color='deeppink', linestyle=':', linewidth=4)

    ax.plot(fpr["macro"], tpr["macro"],
            label='macro-average ROC ({0:0.2f})'
                  ''.format(roc_auc["macro"]),
            color='navy', linestyle=':', linewidth=4)

    ax.plot([0, 1], [0, 1], 'k--', lw=lw)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.05)
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    # plt.legend(loc="lower right")

    # Shrink current axis by 20%
    # box = ax.get_position()
    # ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    handles, labels = ax.get_legend_handles_labels()
    lgd = ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.1))
    text = ax.text(0, 1, "", transform=ax.transAxes)

    ax.set_title('Some extension of Receiver operating characteristic to multi-class')

    fig.savefig('rocCurve', bbox_extra_artists=(lgd, text), bbox_inches='tight')

    plt.show()


if __name__ == "__main__":
    data = pd.read_csv("./data/mbti_1.csv", header=0)

    X = data['posts']
    y = data['type']
    class_names = y.unique()

    # shuffle and split training and test sets
    train_X, test_X, train_Y, test_Y = train_test_split(X, y, test_size=.4,
                                                        random_state=0)

    text_clf = Pipeline([('vect', CountVectorizer(stop_words='english')),
                         ('tfidf', TfidfTransformer()),
                         ('clf', MultinomialNB()),
                         ])

    plot_roc_curve(text_clf, class_names, train_X, test_X, train_Y, test_Y)
