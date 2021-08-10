import os
import sys

import xarray as xr

year = 1865

synth_dir = "data/output"
synth_files = [
    f for f in os.listdir(synth_dir) if os.path.isfile(os.path.join(synth_dir, f))
]
if len(synth_files) == 0:
    sys.exit("No output files found.")
synth_files.sort()
file = os.path.join(synth_dir, synth_files[-1])
print(file)

f = xr.open_dataset(file, decode_times=False)

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
var_list_short = [
    "Eru",
    "VEI",
    "YoE",
    "MoE",
    "DoE",
    "Lat",
    "Lon",
    "TE",
    "MaxIH",
    "MinIH",
]

col_width = 12
print("".join(element.ljust(col_width) for element in var_list_short))
for i, y in enumerate(f.variables["Year_of_Emission"].data):
    if y <= year:
        p_list = [str(f.variables[var_list[j]].data[i])[:10] for j in range(10)]
        print("".join(element.ljust(col_width) for element in p_list))
