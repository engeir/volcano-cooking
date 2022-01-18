"""Script to change the volcanic forcing used in CESM.

Need to reset the time dimension, and the variables date, datesec and stratvolc.

`time` is easy, just counting events from 0 to N-1.
- Set to `np.arange(N)`
`date` are ints and formatted in YYYYMMDD
- Choose using implementation from `volcano-cooking`
`datesec` are ints with seconds since midnight info
- Choose noon (43200), for example

`stratvolc` is a bit more tricky, but not too bad. Set all events to some lat/lon (0, 0),
and find a suitable altitude (perhaps from `volcano-cooking`). Then the values are set
using the implementations from `volcano-cooking`.
"""
import numpy as np
import xarray as xr

file = "VolcanEESMv3.11_SO2_850-2016_Mscale_Zreduc_2deg_c191125"
f = xr.open_dataset(file + ".nc", decode_times=False)

# f["stratvolc"].data = f["stratvolc"].data * 10
new_eruptions = np.ones(20) * 20

n = 390
# f = f.squeeze("time")
f_new = f.drop_dims("time")
f_new = f_new.expand_dims({"time": np.arange(len(new_eruptions))})
# for v in f.dims:
#     if v == "time":
#         print(getattr(f, v))
for v in f.data_vars:
    # f_new.assign_attrs(f.v.data, )
    fv = getattr(f, v)
    f_new = f_new.assign({v: f[v][n : n + len(new_eruptions), ...]})
    # Need the same amount of attrs for CESM to accept the file
    # keep_attrs = f[v].attrs
    # if v == "stratvolc":
    #     # fv.data = np.zeros_like(fv.data)
    #     f[v] = fv[:20, :, :, :]
    #     # setattr(f, v, fv[:20, :, :, :])
    # elif v == "date":
    #     print(fv)
    # elif v == "datesec":
    #     print(fv)
    # print(fv.shape)
    # fv.assign_attrs(**keep_attrs)

    if v != "stratvolc":
        print(f"{v} is {f_new[v].data}")
f_new.to_netcdf(file + "editx10v2.nc", "w", format="NETCDF3_64BIT")


# class ReWrite(Data):
#     def make_dataset(self) -> None:
#         """Re-writes the original netCDF file with new variables."""
#         file = os.path.join(
#             "data",
#             "originals",
#             "VolcanEESMv3.11_SO2_850-2016_Mscale_Zreduc_2deg_c191125",
#         )
#         self.my_frc = xr.open_dataset(file + ".nc", decode_times=False)
#
#     def save_to_file(self) -> None:
#         pass
