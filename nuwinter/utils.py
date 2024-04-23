import pandas as pd


def deduplicate_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Deduplicate a dataframe by objectid.

    :param df: input dataframe
    :return: Deduplicated dataframe
    """
    new_df = []
    for name in list(set(df["objectid"])):
        mask = df["objectid"] == name
        new_df.append(df[mask].iloc[-1])

    return pd.concat(new_df, axis=1).transpose()