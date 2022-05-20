"""Example script showing how to create a custom forcing generator."""

from itertools import cycle

import numpy as np

import volcano_cooking.modules.convert as convert
import volcano_cooking.modules.create as create

# We first need to create a generator class. This inherits from Generate. Let us just
# create the regular intervals generator again.


class GenerateRegularIntervals2(create.Generate):
    def gen_dates_totalemission_vei(self) -> None:
        self.yoes, self.moes, self.does, self.tes = regular_intervals2()
        self.veis = convert.totalemission_to_vei(self.tes)


def regular_intervals2():
    """Create dates with regular intervals.

    This function creates dates with regular intervals and a pre-defined magnitude as
    VEI.

    Returns
    -------
    yoes: np.ndarray
        Array of length 'size' with the year of a date
    moes: np.ndarray
        Array of length 'size' with the month of a date
    does: np.ndarray
        Array of length 'size' with the day of a date
    veis: np.ndarray
        Array of length 'size' with the VEI
    """
    year_sep = 2
    init_year = 1850
    month = 3
    day = 15
    size = 100
    te = cycle([5, 1000, 40, 200])
    yoes = np.zeros(size, dtype=np.int16) + init_year
    moes = np.zeros(size, dtype=np.int8) + month
    does = np.zeros(size, dtype=np.int8) + day
    tes = np.ones(size, dtype=np.float32)
    for i in range(size):
        yoes[i] += i * year_sep
        tes[i] = next(te)
    return yoes, moes, does, tes


def create_synthetic_file() -> None:
    # CREATE DATA -------------------------------------------------------------------- #
    size, init_year = 100, 1850
    g = GenerateRegularIntervals2(size, init_year)
    g.generate()
    all_arrs = g.get_arrays()

    # CREATE NETCDF FILE AND SAVE ---------------------------------------------------- #
    # The `-o` option you can provide to `volcano-cooking` decides whether to create
    # with `create.Data` or with `create.ReWrite`. `create.Data` is the default (in
    # `volcano-cooking`) and what I have used successfully.
    option = 0
    frc_cls = create.ReWrite(*all_arrs) if option == 1 else create.Data(*all_arrs)
    frc_cls.make_dataset()
    frc_cls.save_to_file()


if __name__ == "__main__":
    # Now, running this script will generate a new synthetic file with the same
    # properties as if you ran `volcano-cooking` using the `GenerateRegularIntervals`
    # class.
    create_synthetic_file()
