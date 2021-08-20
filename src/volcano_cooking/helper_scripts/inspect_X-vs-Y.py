"""Compare two variables across the original and synthetic forcing files."""
import os
import sys

import matplotlib.pyplot as plt
import xarray as xr

orig_dir = "data/originals"
if not os.path.isdir(orig_dir):
    os.makedirs(orig_dir)
yax_file = f"{orig_dir}/volcan-eesm_global_2015_so2-emissions-database_v1.0.nc"
if not os.path.isfile(yax_file):
    sys.exit(f"Can't find file {yax_file}")
synth_dir = "data/output"
if not os.path.isdir(synth_dir):
    os.makedirs(synth_dir)
synth_files = [
    f for f in os.listdir(synth_dir) if os.path.isfile(os.path.join(synth_dir, f))
]
if len(synth_files) == 0:
    sys.exit("No output files found.")
synth_files.sort()
xax_file = os.path.join(synth_dir, synth_files[-1])

f1 = xr.open_dataset(xax_file, decode_times=False)
l1 = "Synthetic"
f2 = xr.open_dataset(yax_file, decode_times=False)
l2 = "Data set"

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

x_ax = 1
y_ax = 7
x1 = f1.variables[var_list[x_ax]].data
y1 = f1.variables[var_list[y_ax]].data
x2 = f2.variables[var_list[x_ax]].data
y2 = abs(f2.variables[var_list[y_ax]].data)

plt.figure(figsize=(12, 9))
plt.semilogy()
plt.scatter(x1, y1, label=l1)
plt.scatter(x2, y2, label=l2)
plt.xlabel(var_list[x_ax])
plt.ylabel(var_list[y_ax])
plt.legend()
plt.show()
