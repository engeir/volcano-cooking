"""Compare values in two .nc files.

A quick way of comparing all relevant information found in the forcing data file used by
CESM2 (or similar) with the values stored in the file with synthetic data. The latest
synthetically created file is used.
"""

import os
import pprint
import sys

import xarray as xr

original_file = "data/originals/volcan-eesm_global_2015_so2-emissions-database_v1.0.nc"
if not os.path.isfile(original_file):
    sys.exit(f"Can't find file {original_file}")
synth_dir = "data/output"
synth_files = [
    f for f in os.listdir(synth_dir) if os.path.isfile(os.path.join(synth_dir, f))
]
if len(synth_files) == 0:
    sys.exit("No output files found.")
synth_files.sort()
synthetic_file = os.path.join(synth_dir, synth_files[-1])

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
