"""This script will create a plot of the forcing, i.e. total emission vs time.

The last saved file is used.
"""

import datetime
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

synth_dir = "data/output"
if not os.path.isdir(synth_dir):
    os.makedirs(synth_dir)
synth_files = [
    f
    for f in os.listdir(synth_dir)
    if os.path.isfile(os.path.join(synth_dir, f)) and ".npz" in f
]
if len(synth_files) == 0:
    sys.exit("No output files found.")
synth_files.sort()
file = os.path.join(synth_dir, synth_files[-1])

with np.load(file, "r", allow_pickle=True) as f:
    yoes = f["yoes"]
    moes = f["moes"]
    does = f["does"]
    tes = f["tes"]
    f.close()

dates: list[datetime.datetime] = []
d_app = dates.append
for y, m, d in zip(yoes, moes, does):
    y = str("0" * (4 - len(str(y)))) + f"{y}"
    m = str("0" * (2 - len(str(m)))) + f"{m}"
    d = str("0" * (2 - len(str(d)))) + f"{d}"
    if len(y) != 4 or len(m) != len(d) != 2:
        raise ValueError(
            "Year, month and/or day is not formatted properly. "
            + f"{len(y) = }, {len(m) = }, {len(d) = }, need 4, 2, 2."
        )
    d_app(datetime.datetime.strptime(f"{y}{m}{d}", "%Y%m%d"))

plt.plot(dates, tes)
plt.show()
