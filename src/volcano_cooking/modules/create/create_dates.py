"""Sricpt to put any function that creates correcly formatted dates."""


# TODO: create the dates from an FPP.

import numpy as np


def random_dates(
    size: int, init_year: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Create random dates and place them in order.

    The randomness do not follow a specific model. This is the simplest case where we just
    use the 'randint' funciton from 'numpy'.

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

    Raises
    ------
    ValueError
        If years is not int16, months is not int8 or days is not int8
    """
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

    if yoes.dtype != np.int16 or moes.dtype != np.int8 or does.dtype != np.int8:
        raise ValueError(
            f"{yoes.dtype = }, {moes.dtype = }, {does.dtype = }. Need "
            + "int16, int8, int8."
        )
    return yoes, moes, does


# def fpp_dates(size: int, init_year: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
#     """Create random dates and place them in order.

#     These dates are created from an FPP process.

#     Args:
#         size: int
#             The total number of dates that should be made.
#         init_year: int
#             The first year dates should appear in

#     Returns:
#         yoes: np.ndarray
#             Array of length 'size' with the year of a date
#         moes: np.ndarray
#             Array of length 'size' with the month of a date
#         does: np.ndarray
#             Array of length 'size' with the day of a date
#     """
#     raise NotImplementedError
