"""Config file for setting shared paths, imports, etc across the project"""

import os
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr


scratch_dir = Path(os.getenv("SCRATCH_DIR"))
base_dir = Path(os.getenv("BASE_DIR"))
out_dir = Path(os.getenv("OUTPUT_DIR"))
# Auxiliary directory is for requested outputs that seem like they might
#  be a one-time or limited use item
aux_dir = out_dir.joinpath("auxiliary_content")
aux_dir.mkdir(exist_ok=True)

# path to directory containing CORDEX data
cordex_dir = base_dir.joinpath("arc_cordex/bias_corrected")

# path to dataset of extreme variables calculated on an annal basis
#  for the entire domain of the CORDEX data.
extremes_fp = out_dir.joinpath("annual_extremes.nc")


# path to extractions of extreme variables done for the main set of point locations
extr_era_summary_fp = out_dir.joinpath("extremes_era_extractions.xlsx")

# path to extractions of extreme variables done for the main set of point locations
extr_decade_summary_fp = out_dir.joinpath("extremes_decadal_extractions.xlsx")

# path to directory that will contain barplots of summaries over decades
era_summary_dir = out_dir.joinpath("era_sumamry_charts")
era_summary_dir.mkdir(exist_ok=True)

# path to directory that will contain barplots of summaries over decades
decadal_summary_dir = aux_dir.joinpath("decadal_sumamry_charts")
decadal_summary_dir.mkdir(exist_ok=True)

