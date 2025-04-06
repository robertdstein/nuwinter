import pandas as pd
from tqdm import tqdm


def deduplicate_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Deduplicate a dataframe by objectid.

    :param df: input dataframe
    :return: Deduplicated dataframe
    """

    new_df = []
    for name in list(set(df["objectid"])):
        mask = df["objectid"] == name
        if mask.sum() == 1:
            new_df.append(df[mask].iloc[0])
            continue

        # If there are multiple matches, take the latest
        match = df[mask].sort_values(by="jd")
        new = match.iloc[-1].copy()
        new_df.append(new)

    return pd.concat(new_df, axis=1).transpose().reset_index(drop=True)