from nuztf.ampel_api import ampel_api_name
from wintertoo.data import get_default_value
from wintertoo.schedule import schedule_ra_dec
from nuwinter.neutrino import neutrino_prog_id


def schedule_ztf_transient(
        ztf_name: str,
        prog_id: str = neutrino_prog_id,
        pi: str = "Stein",
        filters: list = None,
        t_exp: float = get_default_value("visitExpTime"),
        n_exp: int = 1,
        dither_bool: bool = get_default_value("dither"),
        dither_distance: float = get_default_value("ditherStepSize"),
        maximum_airmass: float = get_default_value("maxAirmass"),
        nights=[1],
        t_0=None,
        summer: bool = True,
        use_field: bool = True,
        target_priority: float = 1.
):

    res = ampel_api_name(ztf_name, with_history=False)[0]

    ra_deg = res["candidate"]["ra"]
    dec_deg = res["candidate"]["dec"]

    schedule = schedule_ra_dec(
        schedule_name=f"{ztf_name}_schedule",
        ra_deg=ra_deg,
        dec_deg=dec_deg,
        filters=filters,
        t_exp=t_exp,
        n_exp=n_exp,
        dither_bool=dither_bool,
        dither_distance=dither_distance,
        maximum_airmass=maximum_airmass,
        nights=nights,
        pi=pi,
        prog_id=prog_id,
        t_0=t_0,
        summer=summer,
        use_field=use_field,
        target_priority=target_priority
    )

    return schedule
