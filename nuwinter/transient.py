from nuztf.ampel_api import ampel_api_name
from nuwinter.data import summer_filters, base_prog_id
from nuwinter.fields import get_best_summer_field
from nuwinter.schedule import make_schedule


def schedule_ztf_transient(
        ztf_name: str,
        filters: list = summer_filters,
        texp: float = 300.,
        nexp: int = 1,
        dither_bool: bool = True,
        dither_distance="",
        nights=[1],
        pi="Somebody",
        prog_id=base_prog_id,
        t_0=None,
        summer: bool = True,
        use_field: bool = True
):
    if summer:
        get_best_field = get_best_summer_field
    else:
        raise NotImplementedError

    res = ampel_api_name(ztf_name, with_history=False)[0]

    if use_field:
        best_field = get_best_field(res["candidate"]["ra"], res["candidate"]["dec"])
        ra_deg = best_field["RA"]
        dec_deg = best_field["Dec"]

    else:
        ra_deg = res["candidate"]["ra"]
        dec_deg = res["candidate"]["dec"]

    make_schedule(
        schedule_name=f"{ztf_name}_schedule",
        ra_degs=[ra_deg],
        dec_degs=[dec_deg],
        filters=filters,
        texp=texp,
        nexp=nexp,
        dither_bool=dither_bool,
        dither_distance=dither_distance,
        nights=nights,
        t_0=t_0,
        pi=pi,
        prog_id=prog_id
    )