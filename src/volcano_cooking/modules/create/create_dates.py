"""Script to put any function that creates correctly formatted dates."""

import datetime as dt
from itertools import cycle
from typing import List, Tuple, Union

import cftime
import numpy as np

from volcano_cooking.modules import create


def single_date_and_emission(
    init_year: int,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Create a single volcano three years after `init_year`.

    Parameters
    ----------
    init_year: int
        The first year dates should appear in

    Returns
    -------
    yoes: np.ndarray
        Array of length 'size' with the year of a date
    moes: np.ndarray
        Array of length 'size' with the month of a date
    does: np.ndarray
        Array of length 'size' with the day of a date
    veis: np.ndarray
        Array of length 'size' with the VEI as a 1D numpy array
    """
    yoes = np.array([init_year - 1, init_year + 2, init_year + 100], dtype=np.int16)
    moes = np.array([1, 1, 1], dtype=np.int8)
    does = np.array([15, 15, 15], dtype=np.int8)
    tes = np.array([1, 400, 1], dtype=np.float32)
    return yoes, moes, does, tes


def random_dates(
    size: int, init_year: Union[float, str]
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Create random dates and place them in order.

    The randomness do not follow a specific model. This is the simplest case where we just
    use the 'randint' function from 'numpy'.

    Parameters
    ----------
    size: int
        The total number of dates that should be made.
    init_year: float, str
        The first year dates should appear in

    Returns
    -------
    yoes: np.ndarray
        Array of length 'size' with the year of a date
    moes: np.ndarray
        Array of length 'size' with the month of a date
    does: np.ndarray
        Array of length 'size' with the day of a date

    Raises
    ------
    ValueError
        If `size` is non-positive.
    """
    if size < 1:
        raise ValueError(f"{size} = , but must be > 0.")
    yoes = np.cumsum(np.random.randint(0, high=2, size=size)).astype(np.int16) + int(
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

    return yoes, moes, does


def regular_intervals():
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


def fpp_dates_and_emissions(
    size: int, init_year: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Create random ordered dates and total emissions.

    Data is created from an FPP process, specifically the arrival time and amplitude is
    used to set dates and total emissions.

    Parameters
    ----------
    size: int
        The total number of dates that should be made.
    init_year: int
        The first year dates should appear in

    Returns
    -------
    yoes: np.ndarray
        Array of length 'size' with the year of a date
    moes: np.ndarray
        Array of length 'size' with the month of a date
    does: np.ndarray
        Array of length 'size' with the day of a date
    tes:
        Array of length 'size' with the Total_Emission as a 1D numpy array
    """
    f = create.StdFrc(fs=12, total_pulses=size)
    while True:
        ta, amp = f.get_frc()
        # Can't have years beyond 9999
        if int(ta[-1]) + init_year > 9999:
            prev_size = int(ta[-1]) + init_year
            mask = np.argwhere(ta + init_year < 9999)
            ta = ta[mask].flatten()
            amp = amp[mask].flatten()
            size = len(amp)
            print(
                "Can't create dates for years beyond 9999. Keep this in mind when "
                + f"setting `init_year` and `size`. Size: {prev_size} -> {size}."
            )
        # Go from float to YYYY-MM-DD
        dates: List[cftime.datetime] = []
        dates_ap = dates.append
        for n in ta:
            result = cftime.datetime(
                int(n) + init_year, 1, 1, calendar="noleap"
            ) + dt.timedelta(days=(n % 1) * 365)
            dates_ap(result)
        # Dates should be unique
        if not any(np.diff(dates) == dt.timedelta(days=0)):
            break
    yoes_l: List[int] = []
    yoes_ap = yoes_l.append
    moes_l: List[int] = []
    moes_ap = moes_l.append
    does_l: List[int] = []
    does_ap = does_l.append
    for d in dates:
        yoes_ap(d.year)
        moes_ap(d.month)
        does_ap(d.day)
    yoes = np.array(yoes_l, dtype=np.int16)
    moes = np.array(moes_l, dtype=np.int8)
    does = np.array(does_l, dtype=np.int8)
    del yoes_l
    del moes_l
    del does_l
    tes = np.array(amp, dtype=np.float32)
    return yoes, moes, does, tes


def from_json(table: dict, generator: create.Generate) -> create.Generate:
    """Create dates and total emissions from dictionary.

    Data is originally set in a json file, and read using the `json` library.

    Parameters
    ----------
    table: dict
        The dates and emissions as handles in the dictionary.
    generator: create.Generate
        A Generate object to which the table values are written.

    Returns
    -------
    yoes: np.ndarray
        Array of length 'size' with the year of a date
    moes: np.ndarray
        Array of length 'size' with the month of a date
    does: np.ndarray
        Array of length 'size' with the day of a date
    tes:
        Array of length 'size' with the Total_Emission as a 1D numpy array

    Raises
    ------
    KeyError
        If the sections in the loaded json file do not all have the same length.
    """
    _AVAILABLE_KEYS = {
        "dates",
        "emissions",
        "lat",
        "lon",
        "minimum injection height",
        "maximum injection height",
    }
    lens = map(len, table.values())
    if len(set(lens)) != 1:
        raise KeyError("All sections in json file must have the same length.")
    if not {"dates", "emissions"}.issubset(set(table)):
        raise KeyError("The keys 'dates' and 'emissions' must be present.")
    yoes_l: List[int] = []
    yoes_ap = yoes_l.append
    moes_l: List[int] = []
    moes_ap = moes_l.append
    does_l: List[int] = []
    does_ap = does_l.append
    tes_l: List[float] = []
    tes_ap = tes_l.append
    for dates in table.pop("dates"):
        y, m, d = dates.split("-")
        yoes_ap(int(y))
        moes_ap(int(m))
        does_ap(int(d))
    generator.yoes = np.array(yoes_l, dtype=np.int16)
    generator.moes = np.array(moes_l, dtype=np.int8)
    generator.does = np.array(does_l, dtype=np.int8)
    for emissions in table.pop("emissions"):
        tes_ap(float(emissions))
    generator.tes = np.array(tes_l, dtype=np.float32)
    if lats := table.pop("lat", False):
        lat_l: List[float] = []
        lat_ap = lat_l.append
        for lat in lats:
            lat_ap(lat)
        generator.lats = np.array(lat_l, dtype=np.float32)
    if lons := table.pop("lon", False):
        lon_l: List[float] = []
        lon_ap = lon_l.append
        for lon in lons:
            lon_ap(lon)
        generator.lons = np.array(lon_l, dtype=np.float32)
    if miihss := table.pop("minimum injection height", False):
        miihs_l: List[float] = []
        miihs_ap = miihs_l.append
        for miihs in miihss:
            miihs_ap(miihs)
        generator.miihs = np.array(miihs_l, dtype=np.float32)
    if mxihss := table.pop("maximum injection height", False):
        mxihs_l: List[float] = []
        mxihs_ap = mxihs_l.append
        for mxihs in mxihss:
            mxihs_ap(mxihs)
        generator.mxihs = np.array(mxihs_l, dtype=np.float32)
    _RED = "\033[0;31m"
    _BOLD = "\033[1m"
    _END = "\033[0m"
    if table:
        print(
            f"{_RED}{_BOLD}WARNING: some keys in the json table were not used: "
            + f"{table.keys()} Remember that the available keys are\n\t"
            + f"{_AVAILABLE_KEYS}.{_END}"
        )
    return generator
