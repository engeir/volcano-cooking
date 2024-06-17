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
from collections.abc import Mapping
from typing import TYPE_CHECKING

import xarray as xr

if TYPE_CHECKING:
    from xarray.backends.api import T_NetcdfTypes


def add_attributes() -> None:
    """Fix the netCDF file with complete set of attributes."""
    # Read from standard input
    data = sys.stdin.readlines()
    new_path = data[0].strip("\n")
    if not isinstance(new_path, str) or new_path[-3:] != ".nc":
        raise TypeError(f"Are you sure {new_path} is a valid netCDF file?")
    if not os.path.exists(new_path):
        raise FileNotFoundError(f"Cannot find file named {new_path}.")

    f_new = xr.open_dataset(new_path, decode_times=False)

    f_new["altitude_int"] = f_new["altitude_int"].assign_attrs(
        **{
            "standard_name": "altitude interval",
            "units": "km",
            "long_name": "altitude interval",
        }
    )
    encoding: Mapping = {
        "lat": {"_FillValue": None},
        "lon": {"_FillValue": None},
        "altitude": {"_FillValue": None},
        "altitude_int": {"_FillValue": None},
        "stratvolc": {"_FillValue": 9.96921e36},
        "date": {"_FillValue": -2147483647},
        "datesec": {"_FillValue": -2147483647},
    }
    format: T_NetcdfTypes = "NETCDF3_64BIT"
    f_new.to_netcdf(
        path=f"{new_path[:-3]}_2.0.nc",
        format=format,
        encoding=encoding,
    )


if __name__ == "__main__":
    add_attributes()
