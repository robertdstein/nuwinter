"""
Module for plotting a single candidate.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy import visualization
from matplotlib.colors import Normalize
from matplotlib.figure import Figure
from nuztf.cat_match import get_cross_match_info

from nuwinter.plot.compress import decode_img
from nuwinter.ztf import ZTF_HIST_KEY, ZTF_NAME_KEY


BAND_NAMES = {
    1: "Y",
    2: "J",
    3: "H",
    4: "Dark"
}

BAND_COLORS = {
    1: "yellow",
    2: "brown",
    3: "black",
    4: "gray"
}

ZTF_BAND_NAMES = {
    1: "g",
    2: "r",
    3: "i"
}

ZTF_BAND_COLORS = {
    1: "green",
    2: "red",
    3: "orange"
}


def generate_single_page(
        row: pd.Series,
        ann_fields: list[str],
        crossmatch: bool = False,
) -> Figure:
    """
    Generate a page for a given row of data.

    :param row: Single detection in the data
    :param ann_fields: Fields to annotate
    :param crossmatch: Whether to plot the crossmatch
    :return: Figure
    """
    cutouts = [x for x in row.index if "cutout" in x]

    base_width = 5.0

    fig = plt.figure(figsize=(len(cutouts) * base_width, 2.0 * base_width))

    for i, cutout in enumerate(cutouts):
        ax = plt.subplot(2, len(cutouts), i + 1)

        data = decode_img(row[cutout])

        vmin, vmax = np.nanpercentile(data, [0, 100])
        data_ = visualization.AsinhStretch()((data - vmin) / (vmax - vmin))
        ax.imshow(
            data_,
            norm=Normalize(*np.nanpercentile(data_, [0.5, 99.5])),
            aspect="auto",
        )
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(cutout.split("cutout")[1], fontdict={"fontsize": "small"})

    ax_l = plt.subplot(2, 3, 4)

    hist = row["prv_candidates"]

    for fid in set(hist["fid"]):
        df = hist[hist["fid"] == fid]
        plt.errorbar(
            df["jd"],
            df["magpsf"],
            abs(df["sigmapsf"]),
            fmt=".",
            label=BAND_NAMES[fid],
            color=BAND_COLORS[fid],
            mec="black",
            mew=0.5,
        )

    if ZTF_HIST_KEY in row:
        ztf = row["ztf_candidates"]
        if row["ztf_candidates"] is not None:
            for fid in set(ztf["fid"]):
                df = ztf[ztf["fid"] == fid]
                plt.errorbar(
                    df["jd"],
                    df["magpsf"],
                    abs(df["sigmapsf"]),
                    fmt=".",
                    label=ZTF_BAND_NAMES[fid],
                    color=ZTF_BAND_COLORS[fid],
                    mec="black",
                    mew=0.5,
                )

    plt.legend()

    plt.scatter(row["jd"], row["magpsf"])
    ax_l.set_xlabel("JD")
    ax_l.set_ylabel("mag")
    ax_l.invert_yaxis()

    ax = plt.subplot(2, 3, 6)
    ax.axis(False)

    plot_fields = []

    for field in ann_fields:
        val = row[field]
        if isinstance(val, float):
            plot_fields.append(f"{field}: {val:.3f}")
        else:
            plot_fields.append(f"{field}: {val}")

    if crossmatch:

        new = {
            "candidate": row.to_dict(),
            "objectId": row["objectid"]
        }

        xmatch_info = get_cross_match_info(
            raw=new,
        )

        ypos = 0.95

        if "[TNS NAME=" in xmatch_info:
            tns_name = (
                xmatch_info.split("[TNS NAME=")[1].split("]")[0].strip("AT").strip("SN")
            )
            ax_l.annotate(
                "See On TNS",
                xy=(0.5, 1),
                xytext=(0.78, 0.05),
                xycoords="figure fraction",
                verticalalignment="top",
                color="royalblue",
                url=f"https://www.wis-tns.org/object/{tns_name}",
                fontsize=22,
                bbox=dict(
                    boxstyle="round", fc="cornflowerblue", ec="royalblue", alpha=0.4
                ),
            )

        fig.text(
            0.5,
            ypos,
            xmatch_info,
            va="top",
            ha="center",
            fontsize="medium",
            alpha=0.5,
        )

    if ZTF_NAME_KEY in row:
        if not pd.isnull(row[ZTF_NAME_KEY]):

            ax_l.annotate(
                "See On Fritz (ZTF)",
                xy=(0.5, 1),
                xytext=(0.78, 0.05),
                xycoords="figure fraction",
                verticalalignment="top",
                color="royalblue",
                url=f"https://fritz.science/source/{row[ZTF_NAME_KEY]}",
                fontsize=12,
                bbox=dict(boxstyle="round", fc="cornflowerblue", ec="royalblue", alpha=0.4),
            )

    ax_l.annotate(
        "See On Fritz (WNTR)",
        xy=(0.5, 1),
        xytext=(0.63, 0.05),
        xycoords="figure fraction",
        verticalalignment="top",
        color="royalblue",
        url=f"https://fritz.science/source/{row['objectid']}",
        fontsize=12,
        bbox=dict(boxstyle="round", fc="cornflowerblue", ec="royalblue", alpha=0.4),
    )

    plt.annotate(
        "\n".join(plot_fields), xy=(0.35, 0.98), xycoords="axes fraction", va="top"
    )
    plt.suptitle(f"{row['objectid']}")
    return fig
