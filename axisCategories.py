import pandas as pd


def translate_personality(row):
    """
    Categorize by MBTI axis :
        - Introversion (I: 0) / Extraversion (E: 1)
        - INtuition (N: 0) / Sensation (S: 1)
        - Feeling (F: 0) / Thinking (T: 1)
        - Judgement (J: 0) / Perception (P: 1)
    """

    mbti_type = row['type']

    binary_axis = {'I': 0, 'E': 1, 'N': 0, 'S': 1, 'F': 0, 'T': 1, 'J': 0, 'P': 1}

    return pd.Series({
        'IE': binary_axis[mbti_type[0]],
        'NS': binary_axis[mbti_type[1]],
        'FT': binary_axis[mbti_type[2]],
        'JP': binary_axis[mbti_type[3]]
    })


if __name__ == "__main__":
    print('MBTI')
