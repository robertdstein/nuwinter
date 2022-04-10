import pandas as pd
import os
from astropy.time import Time
from astropy import units as u
import logging
from nuwinter.paths import winter_schedule_dir
from nuwinter.data import base_prog_id, summer_filters

logger = logging.getLogger(__name__)


def to_date_string(
        time: Time
):
    return time.isot.split("T")[0]


def make_schedule(
        schedule_name,
        ra_degs: list,
        dec_degs: list,
        prog_id: str = base_prog_id,
        pi: str = "Somebody",
        filters=None,
        texp: float = 300,
        nexp: int = 1,
        dither_bool: bool = True,
        dither_distance="",
        maximum_airmass: float = 1.5,
        maximum_seeing: float = 3.0,
        nights=None,
        t_0: Time = None,
):

    if nights is None:
        nights = list([1, 2, 3])
    if filters is None:
        filters = summer_filters
    if t_0 is None:
        t_0 = Time.now()

    schedule = pd.DataFrame()

    for night in nights:
        start_date = to_date_string(t_0 + (night-1)*u.day)
        end_date = to_date_string(t_0 + (night*u.day))

        for i, ra_deg in enumerate(ra_degs):
            dec_deg = dec_degs[i]

            for f in filters:
                schedule = schedule.append({
                    "RA_deg": ra_deg,
                    "Dec_deg": dec_deg,
                    "Filter": f,
                    "Texp": texp,
                    "Nexp": nexp,
                    "Dither?": ["n", "y"][dither_bool],
                    "Dither distance": dither_distance,
                    "PI": pi,
                    "progID": prog_id,
                    "Start UT Date": start_date,
                    "Start UT Time": "00:00:00.01",
                    "End UT Date": end_date,
                    "End UT Time": "23:59:59.99",
                    "Maximum Airmass": maximum_airmass,
                    "Maximum Seeing": maximum_seeing
                }, ignore_index=True)

    out_path = os.path.join(
        winter_schedule_dir,
        f"{schedule_name}.csv"
    )

    logger.info(f"Saving schedule to {out_path}")

    schedule.to_csv(out_path, index=False)