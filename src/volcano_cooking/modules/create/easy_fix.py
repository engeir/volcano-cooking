"""Add attributes to `altitude_int` coordinate.

Notes
-----

This script is run from the shell script `create_cesm_frc.sh`, but can be run manually as
```python
echo <input-file> | python src/volcano_cooking/modules/create/easy_fix.py
```
where `<input-file>` is the name of the netCDF file you want to edit.
"""

import os
import sys

import xarray as xr


def add_attributes() -> None:
    # Read from standard input
    data = sys.stdin.readlines()
    new_path = data[0].strip("\n")
    if not isinstance(new_path, str) or new_path[-3:] != ".nc":
        raise TypeError(f"Are you sure {new_path} is a valid netCDF file?")
    if not os.path.exists(new_path):
        raise FileNotFoundError(f"Cannot find file named {new_path}.")
    orig_path = os.path.join(
        "data",
        "originals",
        "VolcanEESMv3.11_SO2_850-2016_Mscale_Zreduc_2deg_c191125.nc",
    )

    f_orig = xr.open_dataset(orig_path, decode_times=False)
    f_new = xr.open_dataset(new_path, decode_times=False)

    f_new["altitude_int"] = f_new["altitude_int"].assign_attrs(
        **f_orig["altitude_int"].attrs
    )
    encoding = {
        "lat": {"_FillValue": None},
        "lon": {"_FillValue": None},
        "altitude": {"_FillValue": None},
        "altitude_int": {"_FillValue": None},
        "stratvolc": {"_FillValue": 9.96921e36},
        "date": {"_FillValue": -2147483647},
        "datesec": {"_FillValue": -2147483647},
    }
    f_new.to_netcdf(
        new_path[:-3] + "_2.0.nc", "w", format="NETCDF3_64BIT", encoding=encoding
    )


if __name__ == "__main__":
    add_attributes()
