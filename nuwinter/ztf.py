"""
Module to append ZTF data.
"""

from nuztf.api import api_name
import pandas as pd
from tqdm import tqdm

ZTF_NAME_KEY = "ztfname"
ZTF_HIST_KEY= "ztf_candidates"

def add_ztf_candidates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add in ZTF candidates to the DataFrame.

    :param df: DataFrame to add ZTF candidates to each winter source
    :return: DataFrame with ZTF candidates
    """
    ztf_hists = []

    for _, row in tqdm(df.iterrows(), total=len(df)):

        ztf_hist = None

        if pd.notnull(row[ZTF_NAME_KEY]):
            ztf_row = api_name(row[ZTF_NAME_KEY])
            if len(ztf_row) > 0:
                ztf_hist = pd.DataFrame([ztf_row[0]["candidate"]] + ztf_row[0]["prv_candidates"])
        ztf_hists.append(ztf_hist)

    df[ZTF_HIST_KEY] = ztf_hists
    df[ZTF_NAME_KEY] = df[ZTF_NAME_KEY].replace({"nan": None})
    return df