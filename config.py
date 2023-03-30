"""Config file for setting shared paths, imports, etc across the project"""

import os
from pathlib import Path


out_dir = Path(os.getenv("OUTPUT_DIR"))
# path to directory containing CORDEX data
cordex_dir = Path(os.getenv("CORDEX_DIR"))
# Auxiliary directory is for requested outputs that seem like they might
#  be a one-time or limited use item
aux_dir = out_dir.joinpath("auxiliary_content")
aux_dir.mkdir(exist_ok=True)


# path to dataset of extreme variables calculated on an annal basis
#  for the entire domain of the CORDEX data.
indices_fp = out_dir.joinpath("annual_indices.nc")

# path to era-based summary extractions of indices done for the main set of point locations
# CSVs
idx_era_summary_dir = out_dir.joinpath("era_extractions")
idx_era_summary_dir.mkdir(exist_ok=True)
# Excel file
idx_era_summary_fp = out_dir.joinpath("indices_era_extractions.xlsx")

# path to decade-based summary extractions of indices done for the main set of point locations
# CSVs
idx_decade_summary_dir = out_dir.joinpath("era_extractions")
idx_decade_summary_dir.mkdir(exist_ok=True)
# Excel file
idx_decade_summary_fp = out_dir.joinpath("indices_decadal_extractions.xlsx")

# path to directory that will contain barplots of summaries over decades
era_summary_dir = aux_dir.joinpath("era_summary_charts")
era_summary_dir.mkdir(exist_ok=True)

# path to directory that will contain barplots of summaries over decades
decadal_summary_dir = aux_dir.joinpath("decadal_summary_charts")
decadal_summary_dir.mkdir(exist_ok=True)

# dict of WGS84 coords for each of the locations
locations = {
    # original locations
    "Kaktovik": (70.1, -143.6),
    "Stevens Village": (66.1, -149.1),
    "Igiugik Village": (59.3, -155.9),
    "Levelock": (59.1, -156.9),
    # "Nelson Lagoon": (55.9, -161.2),
    "Eyak": (60.5, -145.6),
    "Ketchikan": (55.6, -136.6),
    # "Unalaska": (53.9, -166.5),
    "Aleutians": (57.838, -159.995),
    
    # new locations provided on 3/6/23
    "Nanwalek": (59.31, -157.91),
    "Port Graham": (59.34, -151.83),
    "Qutekcak (Seward)": (60.10, -149.44),
    "Chenega Bay": (60.06, -148.01),
    "Tatitlek": (60.86, -146.68),
    "Valdez": (61.13, -146.35),
    "Cordova": (60.54, -145.76)
}

# models, scenarios, and base variable names as found in the base CORDEX data
models = [
    "CCCma-CanESM2_CCCma-CanRCM4",
    "CCCma-CanESM2_SMHI-RCA4",
    "CCCma-CanESM2_UQAM-CRCM5",
    "ICHEC-EC-EARTH_DMI-HIRHAM5",
    "ICHEC-EC-EARTH_SMHI-RCA4",
    "ICHEC-EC-EARTH_SMHI-RCA4-SN",
    "MPI-M-MPI-ESM-LR_MGO-RRCM",
    "MPI-M-MPI-ESM-LR_SMHI-RCA4",
    "MPI-M-MPI-ESM-LR_SMHI-RCA4-SN",
    "MPI-M-MPI-ESM-MR_UQAM-CRCM5",
    "NCC-NorESM1-M_SMHI-RCA4",
]

scenarios = ["hist", "rcp45", "rcp85"]

# not using all available model variables yet
# varnames = ["pr", "prsn", "sfcWind", "tas", "tasmax", "tasmin"]
varnames = ["pr", "prsn", "sfcWind", "tasmax", "tasmin"]

# map from model variable names to possible index variable names
idx_varname_lu = {
    "pr": ["rx1day", "rx5day", "r10mm", "cwd", "cdd"],
    "prsn": ["hsd"],
    "tasmax": ["hd", "su", "wsdi"],
    "tasmin": ["cd", "dw", "csdi"],
    "sfcWind": ["wndd"]
}

# template filename
temp_fn = "ARC44_{}_{}_{}_ERA5bc.nc"
