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


def test_file_exists(runner: CliRunner) -> None:
    """Test to see if expected error is raised when file does not exist.

    Parameters
    ----------
    runner: CliRunner
        Runner for creating isolated file  system.
    """
    with runner.isolated_filesystem():
        with pytest.raises(FileNotFoundError):
            synthetic_volcanoes.create_volcanoes(version=2, option=1)


def test_forcing_file_indexes(runner: CliRunner) -> None:
    """Test to see if expected error is raised when forcing file indexes are wrong.

    Parameters
    ----------
    runner: CliRunner
        Runner for creating isolated file  system.
    """
    with runner.isolated_filesystem():
        # Create bad source data set
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


# TODO: Add test for actually creating new, rewritten file.
# def test_create_volcaoes(runner: CliRunner) -> None:
#     """Test to see if files are created as expected.
#
#     Parameters
#     ----------
#     runner: CliRunner
#         Runner for creating isolated file  system.
#     """
#     with runner.isolated_filesystem():
#         # Create fake source data set
#         os.mkdir("data")
#         os.mkdir(os.path.join("data", "originals"))
#         file = os.path.join(
#             "data",
#             "originals",
#             "VolcanEESMv3.11_SO2_850-2016_Mscale_Zreduc_2deg_c191125.nc",
#         )
#         ds1 = xr.Dataset({"a": (["x", "y"], np.ones((2, 2)))})
#         ds1.to_netcdf(file)
#         d = os.path.join("data", "output")
#         now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#         out_npz = os.path.join(os.getcwd(), d, f"synthetic_volcanoes_{now}.npz")
#         out_nc = os.path.join(os.getcwd(), d, f"synthetic_volcanoes_{now}.nc")
#         synthetic_volcanoes.create_volcanoes(version=2, option=1)
#         assert os.path.isfile(out_nc)
#         assert os.path.isfile(out_npz)
#         os.remove(out_nc)
#         os.remove(out_npz)
