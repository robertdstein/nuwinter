import numpy as np
import logging
from nuztf.parse_nu_gcn import find_gcn_no, parse_gcn_circular
from wintertoo.fields import get_fields_in_box, plot_fields
from wintertoo.schedule import make_schedule
from wintertoo.models.too import (
    AllTooClasses,
    FullTooRequest,
    SummerFieldToO,
    WinterFieldToO,
    WinterRaDecToO,
    SummerRaDecToO
)
from wintertoo.data import WINTER_BASE_WIDTH, SUMMER_BASE_WIDTH
from astropy.time import Time
import pandas as pd

logger = logging.getLogger(__name__)

neutrino_nights = [0, 1, 2]
neutrino_priority = 150.


def parse_neutrino(
        nu_name: str,
        scale: float = 1.
):
    gcn_no = find_gcn_no(nu_name)

    logger.info(f"Found GCN {gcn_no} for {nu_name}")

    gcn_info = parse_gcn_circular(gcn_no)

    # nu_name = gcn_info["name"]
    # author = gcn_info["author"]
    nu_ra = gcn_info["ra"]
    ra_unc = scale * np.array([gcn_info["ra_err"][0], gcn_info["ra_err"][1]])

    nu_dec = gcn_info["dec"]

    dec_unc = scale * np.array([gcn_info["dec_err"][0], gcn_info["dec_err"][1]])
    nu_time = gcn_info["time"]

    ra_lim = (nu_ra + ra_unc[1], nu_ra + ra_unc[0])
    dec_lim = (nu_dec + dec_unc[1], nu_dec + dec_unc[0])

    return ra_lim, dec_lim, nu_time


def get_cross(ra_lim, dec_lim, summer: bool = False):

    if summer:
        width = SUMMER_BASE_WIDTH
    else:
        width = WINTER_BASE_WIDTH

    ra_mid = np.mean(ra_lim)
    dec_mid = np.mean(dec_lim)

    center = [ra_mid, dec_mid]
    centers = [center]
    for i in [-1., 1.]:
        for j in range(2):
            new = list(center)
            new[j] += width * i
            centers.append(new)

    df = pd.DataFrame({"RA": [x[0] for x in centers], "Dec": [x[1] for x in centers]})

    return df


def get_square(ra_lim, dec_lim, summer: bool = False):

    if summer:
        width = SUMMER_BASE_WIDTH
    else:
        width = WINTER_BASE_WIDTH

    ra_mid = np.mean(ra_lim)
    dec_mid = np.mean(dec_lim)

    dec_factor = 1./np.cos(np.deg2rad(dec_mid))

    center = [ra_mid, dec_mid]
    centers = []
    for i in [-1., 1.]:
        for j in [-1, 1.]:
            new = [ra_mid + 0.5*width * j * dec_factor, dec_mid + 0.5*width * i]
            centers.append(new)

    df = pd.DataFrame({"RA": [x[0] for x in centers], "Dec": [x[1] for x in centers]})

    return df


def get_pair(ra_lim, dec_lim, summer: bool = False):

    if summer:
        width = SUMMER_BASE_WIDTH
    else:
        width = WINTER_BASE_WIDTH

    ra_mid = np.mean(ra_lim)
    dec_mid = np.mean(dec_lim)

    ra_width = ra_lim[1] - ra_lim[0]
    dec_width = dec_lim[1] - dec_lim[0]

    centers = []

    if ra_width > dec_width:
        for i in [-1, 1.]:
            new = [ra_mid + 0.5*width * i, dec_mid]
            centers.append(new)

    else:
        for i in [-1., 1.]:
            new = [ra_mid, dec_mid + 0.5*width * i]
            centers.append(new)

    df = pd.DataFrame({"RA": [x[0] for x in centers], "Dec": [x[1] for x in centers]})

    return df


def schedule_neutrino(
        nu_name: str,
        scale: float = 1.,
        too_args: dict | None = None,
        nights: list = None,
        make_plot: bool = True,
        summer: bool = False,
        strict: bool = True,
        mode: str = "field"
):
    if nights is None:
        nights = neutrino_nights

    ra_lim, dec_lim, nu_time = parse_neutrino(nu_name, scale=scale)

    if mode == "field":
        res = get_fields_in_box(ra_lim, dec_lim, summer=summer)

    elif mode == "cross":
        res = get_cross(ra_lim, dec_lim, summer=summer)

    elif mode == "square":
        res = get_square(ra_lim, dec_lim, summer=summer)

    elif mode == "pair":
        res = get_pair(ra_lim, dec_lim, summer=summer)

    else:
        err = f"Mode {mode} not recognized"
        logger.error(err)
        raise ValueError(err)

    if strict:
        mask = (res["RA"] > ra_lim[0]) & (res["RA"] < ra_lim[1]) & (res["Dec"] > dec_lim[0]) & (res["Dec"] < dec_lim[1])
        res = res[mask].reset_index(drop=True)

    if make_plot:
        plot_fields(res, ra_lim, dec_lim)

    too_requests = []

    t_now = Time.now().mjd

    for j, offset in enumerate(nights):
        t_start = t_now + offset
        t_end = t_start + 7.

        for _, row in res.iterrows():

            kwargs = {
                "target_priority": neutrino_priority,
                "start_time_mjd": t_start,
                "end_time_mjd": t_end,
                "target_name": f"{nu_name}_{j}",
                "use_best_detector": False
            }

            if too_args is not None:
                kwargs.update(too_args)

            if mode == "field":

                if summer:
                    too_request = SummerFieldToO(
                        field_id=row["ID"],
                        **kwargs
                    )
                else:
                    too_request = WinterFieldToO(
                        field_id=row["ID"],
                        **kwargs
                    )

            else:
                if summer:
                    too_request = SummerRaDecToO(
                        ra_deg=row["RA"],
                        dec_deg=row["Dec"],
                        **kwargs
                    )
                else:
                    too_request = WinterRaDecToO(
                        ra_deg=row["RA"],
                        dec_deg=row["Dec"],
                        **kwargs
                    )

            too_requests.append(too_request)

    return too_requests

    # field_ids = res["#ID"].to_list()
    #
    # n_filters = len(filters)
    #
    # print(res)
    #
    # logger.info(
    #     f"Have {len(field_ids)} fields: \n {field_ids} \n With an exposure time of {t_exp}s, {n_filters} filter(s), "
    #     f"and {n_exp} cycles, this is approximately {n_exp * t_exp * n_filters * len(field_ids) / 60} minutes long."
    # )

    # ras = res["RA"].to_list()
    # decs = res["Dec"].to_list()
    #
    # schedule = make_schedule(
    #     ra_degs=ras,
    #     dec_degs=decs,
    #     field_ids=field_ids,
    #     target_priorities=[target_priority for _ in ras],
    #     filters=filters,
    #     t_exp=t_exp,
    #     n_exp=n_exp,
    #     dither_bool=dither_bool,
    #     dither_distance=dither_distance,
    #     maximum_airmass=maximum_airmass,
    #     nights=nights,
    #     t_0=nu_time,
    #     pi="Stein",
    #     program_name=neutrino_program_name,
    #     program_priority=neutrino_priority,
    # )

    return schedule
