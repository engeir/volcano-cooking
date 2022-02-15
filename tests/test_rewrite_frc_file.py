"""Test cases for the compare_datasets module."""

import os

import numpy as np
import pytest
import xarray as xr
from click.testing import CliRunner

from volcano_cooking import synthetic_volcanoes


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces.

    Returns
    -------
    CliRunner
        Runner for creating isolated file  system.
    """
    return CliRunner()


def test_create_volcaoes(runner: CliRunner) -> None:
    """Test to see if files are created as expected.

    Parameters
    ----------
    runner: CliRunner
        Runner for creating isolated file  system.
    """
    with runner.isolated_filesystem():
        with pytest.raises(FileNotFoundError):
            synthetic_volcanoes.create_volcanoes(version=2, option=1)

    with runner.isolated_filesystem():
        # Create fake source data set
        os.mkdir("data")
        os.mkdir(os.path.join("data", "originals"))
        file = os.path.join(
            "data",
            "originals",
            "VolcanEESMv3.11_SO2_850-2016_Mscale_Zreduc_2deg_c191125.nc",
        )
        ds1 = xr.Dataset({"a": (["x", "y"], np.ones((2, 2)))})
        ds1.to_netcdf(file)
        with pytest.raises(IndexError):
            synthetic_volcanoes.create_volcanoes(version=2, option=1)
