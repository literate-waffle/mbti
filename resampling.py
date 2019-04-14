import pandas as pd
from parser import parse_data
from sklearn.utils import resample


def upsample_minority(df):
    """
    Up-sampling is the process of randomly duplicating observations from the minority class in order to reinforce its
    signal.
    """
    class_names = df.type.unique()
    type_count = df.type.value_counts()

    # Separate majority and minority classes
    majority_class = type_count.idxmax()
    df_minorities = {}
    for label in class_names:
        if label == majority_class:
            df_majority = df[df.type == label]
        else:
            df_minorities[label] = df[df.type == label]

    # Upsample minority class
    df_upsampled = df_majority.copy()
    for label in class_names:
        if label != majority_class:
            df_minority_upsampled = resample(df_minorities[label],
                                             replace=True,  # sample with replacement
                                             n_samples=df_majority.shape[0],  # to match majority class
                                             random_state=123)  # reproducible results

            # Combine majority class with upsampled minority class
            df_upsampled = pd.concat([df_upsampled, df_minority_upsampled])

    # Display new class counts
    # print(df_upsampled.type.value_counts())
    return df_upsampled


def downsample_majority(df):
    """
    Down-sampling involves randomly removing observations from the majority class to prevent its signal from dominating
    the learning algorithm.
    """
    class_names = df.type.unique()
    type_count = df.type.value_counts()

    # Separate majority and minority classes
    minority_class = type_count.idxmin()
    df_majorities = {}
    for label in class_names:
        if label == minority_class:
            df_minority = df[df.type == label]
        else:
            df_majorities[label] = df[df.type == label]

    # Upsample majority classes
    df_downsampled = df_minority.copy()
    for label in class_names:
        if label != minority_class:
            df_majority_downsampled = resample(df_majorities[label],
                                               replace=True,  # sample with replacement
                                               n_samples=df_minority.shape[0],  # to match minority class
                                               random_state=123)  # reproducible results

            # Combine majority class with downsampled majority classes
            df_downsampled = pd.concat([df_downsampled, df_majority_downsampled])

    # Display new class counts
    # print(df_downsampled.type.value_counts())
    return df_downsampled


def midsample(df):
    """
    We are trying a new resampling method : mid-sampling, where we up-sample the minority classes and down-sample the
    majority classes to a middle number of values.
    """
    class_names = df.type.unique()
    n_classes = len(class_names)
    type_count = df.type.value_counts()

    # print(type_count)

    middle_class = type_count.index[n_classes/2 - 1]
    df_other = {}

    for label in class_names:
        if label == middle_class:
            df_middle = df[df.type == label]
        else:
            df_other[label] = df[df.type == label]

    df_midsampled = df_middle.copy()
    for label in class_names:
        if label != middle_class:
            df_other_midsampled = resample(df_other[label],
                                           replace=True,  # sample with replacement
                                           n_samples=df_middle.shape[0],  # to match middle class
                                           random_state=123)  # reproducible results
            # Combine middle class with midsampled classes
            df_midsampled = pd.concat([df_midsampled, df_other_midsampled])

    # Display new class counts
    # print(df_midsampled.type.value_counts())
    return df_midsampled


if __name__ == "__main__":
    data = pd.read_csv("./data/mbti_1.csv", header=0)
    data_parsed = parse_data(data)
    data_upsampled = upsample_minority(data_parsed)
    data_downsampled = downsample_majority(data_parsed)
