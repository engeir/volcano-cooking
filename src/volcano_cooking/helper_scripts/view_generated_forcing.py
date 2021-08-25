"""This script will create a plot of the forcing, i.e. total emission vs time.

The last saved file is used.
"""

import datetime

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

import volcano_cooking.helper_scripts.functions as fnc


def view_forcing(ext: str):
    """View the forcing found in the generated total emission against time.

    Parameters
    ----------
    ext: str
        Extension of the file type used. Valid values are 'npz' and 'nc'.

    Raises
    ------
    ValueError
        If the date created fails to be formatted from ints to string and datetime objects
    """
    yoes, moes, does, tes = load_forcing(ext)

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


def load_forcing(ext: str) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Load variables from the last saved file of given extension.

    Data about the date and total emission found in either the last npz or nc file.

    Parameters
    ----------
    ext: str
        Extension of the file that should be used

    Returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
        Dates and forcing in the form of total emissions is returnd in the order
        yoes, moes, does, tes

    Raises
    ------
    NameError
        If the extension is not either 'npz' or 'nc', no files can be found and the
        variables 'yoes', 'moes', 'does' and 'tes' cannot be found.
    """
    file = fnc.find_last_output(ext)
    if "npz" in ext:
        with np.load(file, "r", allow_pickle=True) as f:
            yoes = f["yoes"]
            moes = f["moes"]
            does = f["does"]
            tes = f["tes"]
            f.close()
    elif "nc" in ext:
        f = xr.open_dataset(file, decode_times=False)
        yoes = f.variables["Year_of_Emission"].data
        moes = f.variables["Month_of_Emission"].data
        does = f.variables["Day_of_Emission"].data
        tes = f.variables["Total_Emission"].data
    else:
        raise NameError(
            "Names 'yoes', 'moes', 'does' and 'tes' are not found. "
            + f"Extension was {ext = }, but shuld be 'npz' or 'nc'."
        )

    return yoes, moes, does, tes


def main():
    # Remember to remove plt.show() when timing
    # import timeit
    # t1 = timeit.timeit(lambda: view_forcing("nc"), number=1000)
    # t2 = timeit.timeit(lambda: view_forcing("npz"), number=1000)
    # print(f"{t1 = }, {t2 = }")
    view_forcing("npz")  # Twice as fast as nc


if __name__ == "__main__":
    main()
