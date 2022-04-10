from nuwinter.data import summer_fields
import matplotlib.pyplot as plt
import numpy as np

base_summer_width = 0.25


def get_summer_fields(ra_lim, dec_lim):
    res = summer_fields.query(
        f"(RA > {ra_lim[0]}) and (RA < {ra_lim[1]}) and (Dec > {dec_lim[0]}) and (Dec < {dec_lim[1]})"
    )
    return res


def plot_summer_fields(res, ra_lim, dec_lim):
    base_summer_width_deg = 0.25

    ax = plt.subplot(111)
    plt.scatter(res["RA"], res["Dec"], marker="+")

    rectangle = plt.Rectangle(
        (ra_lim[0], dec_lim[0]),
        (ra_lim[1] - ra_lim[0]),
        (dec_lim[1] - dec_lim[0]),
        fc="red", alpha=0.2
    )

    ax.add_patch(rectangle)

    for index, row in res.iterrows():
        summer_width_deg = base_summer_width_deg / np.cos(np.radians(row["Dec"]))
        rectangle = plt.Rectangle(
            (row["RA"] - 0.5 * summer_width_deg, row["Dec"] - 0.5 * summer_width_deg),
            summer_width_deg,
            summer_width_deg,
            fc="none", ec="k"
        )
        ax.add_patch(rectangle)

    return ax
