"""
Module for plotting functions.
"""
from nuwinter.plot.plot_candidate import generate_single_page
from nuwinter.plot.compress import decode_img, encode_img

ann_fields = [
    "distpsnr1", "sgscore1", "ra", "dec", "fid", "fieldid", "candid",
    "nneg", "elong", "fwhm", "sumrat",
    "magzpsci", "magap", "magapbig", "magdiff", "magfromlim",
    "classtar", "nbad", "nmtchps", "scorr", "chipsf", "mindtoedge",
]
