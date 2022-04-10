import pandas as pd
import os

data_dir = os.path.dirname(__file__)

summer_fields_path = os.path.join(data_dir, "summer_fields.txt")
summer_fields = pd.read_csv(summer_fields_path, sep='\s+')

neutrino_prog_id = "2021A000"

summer_filters = ["u", "g", "r", "i"]