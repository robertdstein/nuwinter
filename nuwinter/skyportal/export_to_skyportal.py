"""
Functionality to export sources to SkyPortal.
"""
import pandas as pd
from tqdm import tqdm
from nuwinter.skyportal.client import SkyportalClient
from nuwinter.skyportal.photometry import make_photometry
from nuwinter.skyportal.thumbnail import post_all_thumbnails

nuwinter_group_id = 1852

def export_one_source(row: pd.Series, client: SkyportalClient = None, group_id: int = nuwinter_group_id):
    """
    Export a source to SkyPortal.

    :param row: Pandas Series containing the source data
    :param client: SkyPortalClient instance (optional, will create a new one if None)
    :param group_id: ID of the group to which the source belongs (default is nuwinter_group_id)
    """
    if client is None:
        client = SkyportalClient()
        client.set_up_session()

    res = client.api("GET", f"source_exists/{row['objectid']}")
    res.raise_for_status()

    if not res.json()["data"]["source_exists"]:
        data = {
            "ra": row["ra"],
            "dec": row["dec"],
            "id": row["objectid"],
            "group_ids": [group_id],
            "origin": "nuwinter",
        }
        response = client.api("POST", "sources", data)
        response.raise_for_status()

        post_all_thumbnails(row, client=client)

    else:
        data = {
            "objId": row["objectid"],
            "inviteGroupIds": [group_id],
        }
        client.api("POST", "source_groups", data)

    df = make_photometry(row)
    photometry = df.to_dict("list")
    photometry["obj_id"] = row['objectid']
    photometry["instrument_id"] = 1087

    response = client.api("PUT", "photometry", photometry)
    response.raise_for_status()

def export_sources_to_skyportal(
    df: pd.DataFrame,
    client: SkyportalClient = None,
    group_id: int = nuwinter_group_id
):
    """
    Export multiple sources to SkyPortal.

    :param df: DataFrame containing the source data
    :param client: SkyPortalClient instance (optional, will create a new one if None)
    :param group_id: ID of the group to which the sources belong (default is nuwinter_group_id)
    """
    if client is None:
        client = SkyportalClient()
        client.set_up_session()

    for _, row in tqdm(df.iterrows(), total=len(df)):
        export_one_source(row, client=client, group_id=group_id)