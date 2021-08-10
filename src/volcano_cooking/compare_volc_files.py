"""Compare values in two .nc files.

A quick way of printing all relevant information found in the forcing data file used by
CESM2 (or similar) and compare this to the values stored in the file with synthetic data.
"""

import pprint

import xarray as xr

original_file = "data/originals/volcan-eesm_global_2015_so2-emissions-database_v1.0.nc"
synthetic_file = "data/output/synthetic_volcanoes.nc"

forcing = xr.open_dataset(original_file, decode_times=False)
my_forcing = xr.open_dataset(synthetic_file, decode_times=False)
files = [forcing, my_forcing]

# Just np.arange(241), one integer for each volcano
print("Eruption_Number")
pprint.pprint([f["Eruption_Number"] for f in files])
print("")
# print(forcing)
# print(forcing.data_vars.keys())
var_list = [
    "Eruption",
    "VEI",
    "Year_of_Emission",
    "Month_of_Emission",
    "Day_of_Emission",
    "Latitude",
    "Longitude",
    "Total_Emission",
    "Maximum_Injection_Height",
    "Minimum_Injection_Height",
]
for v in var_list:
    print(v)
    pprint.pprint([f.variables[v].data for f in files])
    print("")
