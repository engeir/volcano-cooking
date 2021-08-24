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

import volcano_cooking.modules.convert as convert
import volcano_cooking.modules.create as create

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

    Parameters
    ----------
    size: int
        The total number of eruptsions
    init_year: int
        Change the first year an eruption can happen
    """
    # This only (in the real data set) store a number for each volcanic event, increasing
    # as new events occur. If a volcanic eruption lasts over several dates (years?) the
    # number is repeated, giving a list similar to [1, 2, 3, 4, 4, 4, 5, 5, 6, 7, ...]
    # where the fourth and fifth eruptions lasted over more than one year. Anyways, its
    # most likely not important, so I just put gibberish in it.
    eruptions = np.random.randint(1, high=20, size=size, dtype=np.int8)

    # Create dates
    yoes, moes, does = create.random_dates(size, init_year)
    # Place all volcanoes at equator
    lats = np.zeros(size, dtype=np.float32)  # Equator
    longs = np.ones(size, dtype=np.float32)

    # We don't want eruptions that have a VEI greater than 7.
    # NOTE: should this be created from an FPP?
    veis = np.random.normal(4, 1, size=size).round().astype(np.int8) % 7
    # plt.hist(veis, bins=[0, 1, 2, 3, 4, 5, 6, 7, 8])
    # print(veis)

    # This part is probably important. I need to make sure the ratio between sum of
    # emission and the column emission for a given volcano is smaller than 1e-6.
    # NOTE: should this be created from an FPP?
    tes = convert.vei_to_totalemission(veis)

    miihs, mxihs = convert.vei_to_injectionheights(veis)

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
    for _ in range(size):
        names += "Dummy, "
    names = names[:-2]  # Removing the last comma and whitespace
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
