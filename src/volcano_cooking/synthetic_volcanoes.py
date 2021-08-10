"""This script creates a .nc file consisting of volcanic eruptions and the
corresponding time of arrival down to the nearest day and the magnitude of the
eruption.

The lat/lon location is also included, but considered unimportant and thus the
same location is used for all volcanoes.
"""
import datetime
import os
import sys

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


def create_volcanoes(size: int = 251, init_year: int = 1850) -> None:
    """Create volcanoes starting at the year 1850.

    This will re-create the same data as can be found in forcing files used within the
    CESM2 general circulation model.

    Args:
        size: int
            The total number of eruptsions
        init_year: int
            The first year an eruption can happen
    """
    eruptions = np.random.randint(1, high=20, size=size, dtype=np.int8)
    # We don't want eruptions that have a VEI greater than 7.
    veis = np.random.normal(4, 1, size=size).round().astype(np.int8) % 7
    yoes = np.cumsum(np.random.randint(0, high=2, size=size, dtype=np.int16)) + int(
        init_year
    )
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
    # This part is probably important. I need to make sure the ratio between sum of
    # emission for a given volcano and the column emission is smaller than 1e-6.
    tes = 1e-2 * 3 ** (np.random.normal(0.1, 1.0, size=size).astype(np.float32) + veis)
    scale_max = np.array([80 if v > 3 else 10 for v in veis])
    scale_min = np.array([20 if v > 3 else 1 for v in veis])
    mxihs = np.abs(np.random.normal(1, 2.0, size=size).astype(np.float32) * scale_max)
    miihs = np.abs(np.random.normal(1, 2.0, size=size).astype(np.float32) * scale_min)
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
    # Names are unimportant. The real data set would list the name of the volcano here,
    # e.g. Mt. Pinatubo.
    names = ""
    for i in range(size):
        names += "Dummy, "
    names = names[:-2]
    my_frc.Longitude.encoding["_FillValue"] = False
    my_frc["Eruption"] = my_frc.Eruption.assign_attrs(
        # The volcano number is a reference to the geographical location of the eruption.
        # The volcano name is its name and the note/reference is where in the literature
        # you can find the values related to the eruption. All this is unimportant given
        # that this is just made up data.
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

    synth_dir = "data/output"
    if not os.path.isdir(synth_dir):
        os.makedirs(synth_dir)
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    out_file = f"{synth_dir}/synthetic_volcanoes_{now}.nc"
    if os.path.isfile(out_file):
        sys.exit(f"The file {out_file} already exists.")
    # The format is important for when you give the .nc file to the .ncl script that creates
    # the final forcing file.
    my_frc.to_netcdf(out_file, "w", format="NETCDF4")
