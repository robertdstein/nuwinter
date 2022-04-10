import os
from nuztf.skymap_scanner import LOCALSOURCE

winter_data_dir = os.path.join(os.path.dirname(LOCALSOURCE), "nuwinter")

winter_schedule_dir = os.path.join(winter_data_dir, "schedule")


try:
    os.makedirs(winter_schedule_dir)
except OSError:
    pass
