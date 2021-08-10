"""This script creates a .nc file consisting of volcanic eruptions and the
corresponding time of arrival down to the nearest day and the magnitude of the
eruption.

The lat/lon location is also included, but considered unimportant and thus the
same location is used for all volcanoes.
"""
import numpy as np
import xarray as xr

# ====================================================================================== #
# Need:
#
# Dimension(s):
## Eruption number (do not contain variable attributes)
#
# Variable(s):
## Eruption (dim: Eruption_Number)
## -  Volcano number (not important, used to classify real volcanoes)
## -  Volcano name (not important)
## -  Notes and references (not important)
## VEI (dim: Eruption_Number)
## Year_of_Emission (dim: Eruption_Number)
## Month_of_Emission (dim: Eruption_Number)
## Day_of_Emission (dim: Eruption_Number)
## Latitude (dim: Eruption_Number)
## Longitude (dim: Eruption_Number)
## Total_Emission (dim: Eruption_Number)
## Maximum_Injection_Height (dim: Eruption_Number)
## Minimum_Injection_Height (dim: Eruption_Number)
# ====================================================================================== #

# Now trying to re-create the same data set.
size = 251
eruptions = np.random.randint(1, high=20, size=size, dtype=np.int8)
# veis = np.random.randint(0, high=7, size=size, dtype=np.int8)
veis = np.random.normal(4, 1, size=size).round().astype(np.int8) % 7
yoes = np.cumsum(np.random.randint(0, high=2, size=size, dtype=np.int16)) + int(1850)
moes = np.random.randint(1, high=12, size=size, dtype=np.int8)
does = np.random.randint(1, high=28, size=size, dtype=np.int8)
# Make sure dates are increasing!
# idx = list of arrays of indexes pointing to the same year
idxs = [np.where(yoes == i)[0] for i in np.unique(yoes)]
# sort months with indexes
# sort days with indexes
for idx in idxs:
    moes[idx] = np.sort(moes[idx])
    does[idx] = np.sort(does[idx])
lats = np.zeros(size, dtype=np.float32)  # Equator
longs = np.ones(size, dtype=np.float32)
# This part is probably important. I need to make sure the ratio between sum of emission
# for a given volcano and the column emission is smaller than 1e-6.
tes = 1e-2 * 3**(np.random.normal(.1, 1., size=size).astype(np.float32) + veis)
scale_max = np.array([80 if v > 3 else 10 for v in veis])
scale_min = np.array([20 if v > 3 else 1 for v in veis])
mxihs = np.abs(np.random.normal(1, 2., size=size).astype(np.float32) * scale_max)
miihs = np.abs(np.random.normal(1, 2., size=size).astype(np.float32) * scale_min)
for idx, (i, j) in enumerate(zip(miihs, mxihs)):
    miihs[idx] = min(i, j)
    mxihs[idx] = max(i, j)

my_frc = xr.Dataset(
    data_vars=dict(
        Eruption=(["Eruption_Number"], eruptions),
        VEI=(["Eruption_Number"], veis),
        Year_of_Emission=(["Eruption_Number"], yoes),
        Month_of_Emission=(["Eruption_Number"], moes),
        Day_of_Emission=(["Eruption_Number"], does),
        Latitude=(["Eruption_Number"], lats),
        Longitude=(["Eruption_Number"], longs),
        Total_Emission=(["Eruption_Number"], tes),
        Maximum_Injection_Height=(["Eruption_Number"], mxihs),
        Minimum_Injection_Height=(["Eruption_Number"], miihs),
    ),
    # Global attributes
    attrs=dict(
        Creator="Eirik R. Enger",
        DOI="#####",
        Citation="#####",
        Notes="All emissions are created from a filtered Poisson process (FPP).",
    ),
)
names = ""
for i in range(size):
    names += "Dummy, "
names = names[:-2]
my_frc.Longitude.encoding["_FillValue"] = False
my_frc["Eruption"] = my_frc.Eruption.assign_attrs(
    Volcano_Number=np.ones(size) * 123456,
    Volcano_Name=names,
    Notes_and_References=names,
)
my_frc["VEI"] = my_frc.VEI.assign_attrs(
    Notes="Volcanic_Explosivity_Index_based_on_Global_Volcanism_Program"
)
my_frc["Latitude"] = my_frc.Latitude.assign_attrs(Units="-90_to_+90")
my_frc["Longitude"] = my_frc.Longitude.assign_attrs(Units="Degrees_East")
my_frc["Total_Emission"] = my_frc.Total_Emission.assign_attrs(Units="Tg_of_SO2")
my_frc["Maximum_Injection_Height"] = my_frc.Maximum_Injection_Height.assign_attrs(
    Units="km_above_mean_sea_level"
)
my_frc["Minimum_Injection_Height"] = my_frc.Minimum_Injection_Height.assign_attrs(
    Units="km_above_mean_sea_level"
)

my_frc.to_netcdf("volc_from_synthetic_volcanoes.nc", "w", format="NETCDF4")
