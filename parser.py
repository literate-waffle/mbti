import pandas as pd


def parse_posts(posts):
    return posts.split("|||")


def parse_data(data):
    """
    Split posts string and use its values as rows :
        1. Split posts on "|||"
        2. Split posts into new columns
        3. Merge columns with the rest of the dataset
        4. Drop old posts column
        5. Transform the numeric columns (corresponding to posts) into separate rows
        6. Drop variable column which contains the ids of the numeric columns
        7. Get rid of empty values

    :param data: data pandas dataframe
    :return: pandas dataframe where each user's posts is in separate rows
    """
    data['id'] = data.index
    parsed = data.posts.apply(parse_posts)\
        .apply(pd.Series)\
        .merge(data, left_index=True, right_index=True)\
        .drop(["posts"], axis=1)\
        .melt(id_vars=['id', 'type'], value_name="post")\
        .drop("variable", axis=1)\
        .dropna()\
        .sort_values(by=['id'])
    return parsed


if __name__ == "__main__":
    df = pd.read_csv("./data/mbti_1.csv", header=0)
    print(parse_data(df))

