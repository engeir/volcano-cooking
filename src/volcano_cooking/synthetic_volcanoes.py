"""This script creates a .nc file consisting of volcanic eruptions and the
corresponding time of arrival down to the nearest day and the magnitude of the
eruption.

The lat/lon location is also included, but considered unimportant and thus the
same location is used for all volcanoes.
"""
import numpy as np

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
    # as new events occur. If a volcanic eruption have several emissions listed in the
    # forcing file the number is repeated, giving a list similar to [1, 2, 3, 4, 4, 4, 5,
    # 5, 6, 7, ...].  Here, the fourth and fifth eruptions lasted long enough and to get
    # more samples in the forcing file. Anyways, its most likely not important, so I just
    # put gibberish in it.
    eruptions = np.random.randint(1, high=20, size=size, dtype=np.int8)

    # Create dates
    yoes, moes, does = create.random_dates(size, init_year)
    # Place all volcanoes at equator
    lats = np.zeros(size, dtype=np.float32)  # Equator
    lons = np.ones(size, dtype=np.float32)

    # We don't want eruptions that have a VEI greater than 7.
    # NOTE: should this be created from an FPP?
    veis = np.random.normal(4, 1, size=size).round().astype(np.int8) % 7

    # This part is probably important. I need to make sure the ratio between sum of
    # emission and the column emission for a given volcano is smaller than 1e-6.
    # NOTE: should this be created from an FPP?
    tes = convert.vei_to_totalemission(veis)

    miihs, mxihs = convert.vei_to_injectionheights(veis)

    frc_cls = create.Data(
        eruptions=eruptions,
        yoes=yoes,
        moes=moes,
        does=does,
        lats=lats,
        lons=lons,
        tes=tes,
        veis=veis,
        miihs=miihs,
        mxihs=mxihs,
    )
    frc_cls.make_dataset()
    frc_cls.save_to_file()


def main():
    create_volcanoes(size=300)


if __name__ == "__main__":
    main()
