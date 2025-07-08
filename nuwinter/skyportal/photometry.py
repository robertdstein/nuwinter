"""
Module for generating photometry data for SkyPortal.
"""
import pandas as pd
from astropy.time import Time

sncosmo_filters = {
    1: "desy",
    2: "2massj",
    3: "2massh",
}

def make_photometry(source: pd.Series) -> pd.DataFrame:
    """
    Make a de-duplicated pandas.DataFrame with photometry of
    Modified from Kowalksi (https://github.com/dmitryduev/kowalski)

    :param source: source row
    :return: pandas.DataFrame with photometry
    """

    new = source["prv_candidates"].copy()
    new["mjd"] = Time(new["jd"], format="jd").mjd

    mapping = {
        "magpsf": "mag",
        "sigmapsf": "magerr",
        "diffmaglim": "limiting_mag",
    }

    new.rename(columns=mapping, inplace=True)
    new["magsys"] = "ab"
    filters = [sncosmo_filters[x] for x in new["fid"]]
    new["filter"] = filters

    new = new[["mjd", "magsys", "filter"] + list(mapping.values())]
    return new