"""Sricpt to put any function that creates correctly formatted dates."""


# TODO: create the dates from an FPP.

import datetime as dt
from typing import Union

import numpy as np
import uit_scripts.shotnoise.gen_shot_noise as gsn


def random_dates(
    size: int, init_year: Union[float, str]
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
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
        raise ValueError(f"{size = }, but must be > 0.")
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


def fpp_dates_and_emissions(
    size: int, init_year: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
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
    # TODO: figure out which gamma and other parameters are appropriate
    mean_amp = 1.0
    gamma = 0.52  # Value from proj5 work, instrumental data set analysis
    while True:
        ins = gsn.make_signal(gamma, size, 0.1, ampta=True, mA=mean_amp)
        amp, ta = np.asarray(ins[2]), np.asarray(ins[3])
        dates: list[dt.date] = []
        dates_ap = dates.append
        for n in ta:
            result = (
                dt.datetime(int(n) + init_year, 1, 1) + dt.timedelta(days=(n % 1) * 365)
            ).date()
            dates_ap(result)
        # Dates should be unique
        if not any(np.diff(dates) == dt.timedelta(days=0)):
            break
    yoes_l: list[int] = []
    yoes_ap = yoes_l.append
    moes_l: list[int] = []
    moes_ap = moes_l.append
    does_l: list[int] = []
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
