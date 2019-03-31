# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import warnings
from IPython.display import display

from preprocessing import format_text

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
# from config import current_file


warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("error", category=RuntimeWarning)

seed = 7

NUM_CLASSES = 16


def compare_classifiers():

    # Categorized data frame
    data = pd.read_csv("./data/mbti_1.csv", header=0)

    vectorizer = CountVectorizer()

    def vectorize_train(train_x):
        return vectorizer.fit_transform(train_x.apply(format_text))

    def vectorize_test(test_x):
        return vectorizer.transform(test_x.apply(format_text))

    k_value = 7
    dict_classifiers = {
        "Logistic Regression": LogisticRegression(),
        "KNN": KNeighborsClassifier(n_neighbors=k_value, weights='distance', algorithm='auto'),
        "Linear SVM": SGDClassifier(max_iter=1000, tol=1e-3),
        "Random Forest": RandomForestClassifier(),
        "Naive Bayes": MultinomialNB(),
        # "LDA": LinearDiscriminantAnalysis(),
        # "CART": DecisionTreeClassifier()
    }
    dict_models = {}

    HEADERS = data.columns.values.tolist()

    def split_dataset(x ,y , train_percentage):
        """
        Split dataset into train and test dataset
        """
        train_x, test_x, train_y, test_y = train_test_split(
            x,
            y,
            train_size=train_percentage)
        return train_x, test_x, train_y, test_y

    def evaluate(y, predicted_y):
        """
        Calculate metrics of the classifier. Since it is a multiclass model, found the formulas on
        https://stats.stackexchange.com/questions/51296/how-do-you-calculate-precision-and-recall-for-multiclass-classification-using-co
        then calculate the average of all precisions and recalls.
        :param y:
        :param predicted_y:
        :return: precision, recall and f1_score of classifier
        """
        # acc = accuracy_score(y, predicted_y)
        cm = pd.DataFrame(confusion_matrix(y, predicted_y))
        precision = np.int32(0)
        for mbti in range(NUM_CLASSES):
            try:
                precision += np.int32(cm[mbti][mbti]) / np.sum([cm[j][mbti] for j in range(NUM_CLASSES)])
            except RuntimeWarning:
                precision += 0
        precision = precision / NUM_CLASSES
        recall = np.int32(0)
        for mbti in range(NUM_CLASSES):
            try:
                recall += np.int32(cm[mbti][mbti]) / np.sum([cm[mbti][j] for j in range(NUM_CLASSES)])
            except RuntimeWarning:
                recall += 0
        recall = recall / NUM_CLASSES
        f_score = 2 * precision * recall / (precision + recall) if precision > 0 and recall > 0 else 0
        return precision, recall, f_score

    def classify(classifier_name, classifier, train_x, test_x, train_y, test_y, verbose=True):
        t_start = time.time()
        print(classifier_name)
        classifier.fit(train_x, train_y)
        t_end = time.time()

        t_diff = t_end - t_start
        train_score = classifier.score(train_x, train_y)
        test_score = classifier.score(test_x, test_y)

        dict_models[classifier_name] = {
            'model': classifier,
            'train_score': train_score,
            'test_score': test_score,
            'train_time': t_diff
        }

        if verbose:
            print("trained {c} in {f:.2f} s".format(c=classifier_name, f=t_diff))
        return classifier

    def display_dict_models(dict, sort_by='test_score'):
        cls = [key for key in dict.keys()]
        test_s = [dict[key]['test_score'] for key in cls]
        training_s = [dict[key]['train_score'] for key in cls]
        training_t = [dict[key]['train_time'] for key in cls]
        precision = [dict[key]['precision'] for key in cls]
        recall = [dict[key]['recall'] for key in cls]
        f_score = [dict[key]['f_score'] for key in cls]

        columns = ['classifier', 'train_score', 'test_score', 'train_time', 'precision', 'recall', 'f_score']

        df_ = pd.DataFrame(data=np.zeros(shape=(len(cls), len(columns))),
                           columns=columns)
        for ii in range(0, len(cls)):
            df_.loc[ii, 'classifier'] = cls[ii]
            df_.loc[ii, 'train_score'] = training_s[ii]
            df_.loc[ii, 'test_score'] = test_s[ii]
            df_.loc[ii, 'train_time'] = training_t[ii]
            df_.loc[ii, 'precision'] = precision[ii]
            df_.loc[ii, 'recall'] = recall[ii]
            df_.loc[ii, 'f_score'] = f_score[ii]

        pd.set_option('display.max_columns', None)

        display(df_.sort_values(by=sort_by, ascending=False))

    def predict(classifier, train_x, test_x, train_y, test_y):
        clf = classify(classifier, dict_classifiers[classifier], train_x, test_x, train_y, test_y)
        pred_y = clf.predict(vect_test_x)
        precision, recall, f_score = evaluate(test_y, pred_y)
        dict_models[classifier_name]['precision'] = precision
        dict_models[classifier_name]['recall'] = recall
        dict_models[classifier_name]['f_score'] = f_score

    def compare(dataset):
        """
        Evaluate each model in turn
        """
        results = []
        names = []
        # https://scikit-learn.org/stable/modules/model_evaluation.html
        scoring = 'accuracy'
        # scoring = 'f1_weighted'
        train_x, test_x, train_y, test_y = split_dataset(dataset['posts'], dataset['type'], 0.7)
        print(scoring)
        for name in dict_classifiers.keys():
            model = dict_classifiers[name]
            kfold = KFold(n_splits=10, random_state=seed)
            cv_results = cross_val_score(model, vectorize_train(train_x), train_y, cv=kfold, scoring=scoring)
            results.append(cv_results)
            names.append(name)
            msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
            print(msg)

        # boxplot algorithm comparison
        fig = plt.figure()
        fig.suptitle('Algorithm Comparison ({0})'.format(scoring))
        ax = fig.add_subplot(111)
        plt.boxplot(results)
        ax.set_xticklabels(names)
        plt.show()

    train_x, test_x, train_y, test_y = split_dataset(data['posts'], data['type'], 0.7)
    vect_train_x = vectorize_train(train_x)
    vect_test_x = vectorize_test(test_x)

    for classifier_name in dict_classifiers.keys():
        predict(classifier_name, vect_train_x, vect_test_x, train_y, test_y)

    print("\n==================================== Results ==================================== ")
    display_dict_models(dict_models)

    print()
    compare(data)


if __name__ == "__main__":
    compare_classifiers()
