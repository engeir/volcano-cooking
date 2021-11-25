"""Tests cases for the create_dates module."""

import numpy as np
import pytest

from volcano_cooking.modules.create import create_dates


def test_random_dates() -> None:
    s1 = -1
    s2 = 0
    s3 = "1"
    s4 = 1000
    with pytest.raises(ValueError):
        create_dates.random_dates(s1, s1)
        create_dates.random_dates(s2, s2)
    with pytest.raises(TypeError):
        create_dates.random_dates(s3, s3)
    out1, out2, out3 = create_dates.random_dates(s4, s3)
    assert out1.shape == out2.shape
    assert out2.shape == out3.shape
    assert out1.dtype == np.int16
    assert out2.dtype == np.int8
    assert out3.dtype == np.int8
    idxs = [np.where(out1 == i)[0] for i in np.unique(out1)]
    for idx in idxs:
        for i, (m, d) in enumerate(zip(out2[idx][:-1], out3[idx][:-1])):
            assert m <= out2[idx][i + 1]
            assert d <= out3[idx][i + 1]


def test_fpp_dates_and_emissions() -> None:
    s1 = -1
    s2 = 0
    s3 = "1"
    s4 = 100
    with pytest.raises(ValueError):
        create_dates.fpp_dates_and_emissions(s1, s1)
        create_dates.fpp_dates_and_emissions(s2, s2)
    with pytest.raises(TypeError):
        create_dates.fpp_dates_and_emissions(s3, s3)
    out1, out2, out3, out4 = create_dates.fpp_dates_and_emissions(s4, s4)
    assert out1.shape == out2.shape
    assert out2.shape == out3.shape
    assert out3.shape == out4.shape
    assert out1.dtype == np.int16
    assert out2.dtype == np.int8
    assert out3.dtype == np.int8
    assert out4.dtype == np.float32
    idxs = [np.where(out1 == i)[0] for i in np.unique(out1)]
    for idx in idxs:
        for i, (m, d) in enumerate(zip(out2[idx][:-1], out3[idx][:-1])):
            assert m <= out2[idx][i + 1]
            if m == out2[idx][i + 1]:
                assert d <= out3[idx][i + 1]


if __name__ == "__main__":
    test_random_dates()
    test_fpp_dates_and_emissions()
