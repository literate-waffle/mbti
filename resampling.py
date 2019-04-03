import pandas as pd
from sklearn.utils import resample


def upsample_minority(df):
    """
    Up-sampling is the process of randomly duplicating observations from the minority class in order to reinforce its
    signal.
    The resample method simply duplicates rows of the minority class to match the number of majority class rows.
    """
    class_names = df.type.unique()
    type_count = df.type.value_counts()

    # print(type_count)

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


if __name__ == "__main__":

    data = pd.read_csv("./data/mbti_1.csv", header=0)
    print(data[data['type'] == 'ESTJ'].sort_values(by=['posts']))

    data_upsampled = upsample_minority(data)
    # data_downsampled = downsample_majority(data)

    # print(data_upsampled.type.value_counts())
    print(data_upsampled[data_upsampled['type'] == 'ESTJ'].sort_values(by=['posts']))
