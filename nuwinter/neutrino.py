import numpy as np
import logging
from nuztf.parse_nu_gcn import find_gcn_no, parse_gcn_circular
from wintertoo.fields import get_summer_fields_in_box, plot_summer_fields
from wintertoo.schedule import make_schedule
from wintertoo.data import summer_filters, get_default_value

logger = logging.getLogger(__name__)

neutrino_nights = [1, 2, 3]
neutrino_prog_id = "2021A000"
neutrino_pi = "Stein"
neutrino_priority = 10.


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

    ra_lim = [nu_ra + ra_unc[1], nu_ra + ra_unc[0]]
    dec_lim = [nu_dec + dec_unc[1], nu_dec + dec_unc[0]]

    return ra_lim, dec_lim, nu_time


def schedule_neutrino(
        nu_name: str,
        scale: float = 1.,
        filters: list = summer_filters,
        t_exp: float = get_default_value("visitExpTime"),
        n_exp: int = 1,
        dither_bool: bool = get_default_value("dither"),
        dither_distance: float = get_default_value("ditherStepSize"),
        maximum_airmass: float = get_default_value("maxAirmass"),
        nights: list = None,
        make_plot: bool = True,
        summer: bool = True,
):
    if nights is None:
        nights = neutrino_nights

    if summer:
        get_fields_in_box = get_summer_fields_in_box
        plot_fields = plot_summer_fields
    else:
        raise NotImplementedError

    ra_lim, dec_lim, nu_time = parse_neutrino(nu_name, scale=scale)

    res = get_fields_in_box(ra_lim, dec_lim)

    if make_plot:
        plot_fields(res, ra_lim, dec_lim)

    field_ids = res["#ID"].to_list()

    n_filters = len(filters)

    logger.info(
        f"Have {len(field_ids)} fields: \n {field_ids} \n With an exposure time of {t_exp}s, {n_filters} filter(s), "
        f"and {n_exp} cycles, this is approximately {n_exp * t_exp * n_filters * len(field_ids) / 60} minutes long."
    )

    ras = res["RA"].to_list()
    decs = res["Dec"].to_list()

    make_schedule(
        schedule_name=f"{nu_name}_schedule",
        ra_degs=ras,
        dec_degs=decs,
        filters=filters,
        t_exp=t_exp,
        n_exp=n_exp,
        dither_bool=dither_bool,
        dither_distance=dither_distance,
        maximum_airmass=maximum_airmass,
        nights=nights,
        t_0=nu_time,
        pi="Stein",
        prog_id=neutrino_prog_id,
        program_priority=neutrino_priority,
    )
