"""
Function for converting a FITS image to a skyportal "thumbnail".
"""

import base64
import io

import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from astropy.visualization import (
    AsymmetricPercentileInterval,
    ImageNormalize,
    LinearStretch,
    LogStretch,
)
from nuwinter.skyportal.client import SkyportalClient
from nuwinter.plot import decode_img

matplotlib.use("agg")

thumbnail_map = {
    "science": "new",
    "template": "ref",
    "difference": "sub"
}


def make_thumbnail(
    image_data: np.ndarray,
    linear_stretch: bool = False,
) -> str:
    """
    Util function to convert a FITS image to a PNG image

    Skyportal requires, to quote the API:

        base64-encoded PNG image file contents.
        Image size must be between 16px and 500px on a side.

    :param image_data: Image data
    :param linear_stretch: boolean whether to use a linear stretch (default is log)
    :return: Skyportal-compliant PNG image string
    """
    with io.BytesIO() as buff:
        fig = plt.figure()
        fig.set_size_inches(4, 4, forward=False)
        ax_1 = plt.Axes(fig, [0.0, 0.0, 1.0, 1.0])
        ax_1.set_axis_off()
        fig.add_axes(ax_1)

        # replace nans with median:
        img = np.array(image_data)
        # replace dubiously large values
        xl_mask = np.greater(np.abs(img), 1e20, where=~np.isnan(img))
        if img[xl_mask].any():
            img[xl_mask] = np.nan
        if np.isnan(img).any():
            median = float(np.nanmean(img.flatten()))
            img = np.nan_to_num(img, nan=median)

        norm = ImageNormalize(
            img,
            stretch=LinearStretch() if linear_stretch else LogStretch(),
        )
        img_norm = norm(img)
        normalizer = AsymmetricPercentileInterval(
            lower_percentile=1, upper_percentile=100
        )
        vmin, vmax = normalizer.get_limits(img_norm)
        ax_1.imshow(img_norm, cmap="bone", origin="lower", vmin=vmin, vmax=vmax)
        plt.savefig(buff, dpi=42)

        buff.seek(0)
        plt.close()

        fritz_thumbnail = base64.b64encode(buff.read()).decode("utf-8")

    return fritz_thumbnail


def post_one_thumbnail(row: pd.Series, cutout_type: str, client: SkyportalClient | None = None):
    """
    Post a single thumbnail to Skyportal.

    :param row: Pandas Series containing the data for the thumbnail
    :param cutout_type: Type of cutout (e.g., 'science', 'template', 'difference')
    :param client: SkyportalClient instance (optional, will create a new one if None)

    """
    if client is None:
        client = SkyportalClient()
        client.set_up_session()

    cutout_data = row[f"cutout_{cutout_type}"]
    skyportal_type = thumbnail_map[cutout_type]

    linear_stretch = cutout_type.lower() in ["difference"]

    skyportal_thumbnail = make_thumbnail(
        image_data=decode_img(cutout_data),
        linear_stretch=linear_stretch,
    )

    thumbnail_dict = {
        "obj_id": row["objectid"],
        "data": skyportal_thumbnail,
        "ttype": skyportal_type,
    }
    response = client.api("POST", "thumbnail", thumbnail_dict)
    response.raise_for_status()


def post_all_thumbnails(row: pd.Series, client: SkyportalClient | None = None):
    """
    Post all thumbnails for a given row to Skyportal.

    :param row: Pandas Series containing the data for the thumbnails
    :param client: SkyportalClient instance (optional, will create a new one if None)

    """
    if client is None:
        client = SkyportalClient()
        client.set_up_session()

    for cutout_type in thumbnail_map:
        post_one_thumbnail(row, cutout_type, client)
