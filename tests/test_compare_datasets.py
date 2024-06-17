"""Test cases for the compare_datasets module."""

import numpy as np
import pytest
import xarray as xr
from click.testing import CliRunner
from volcano_cooking.helper_scripts import compare_datasets


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces.

    Returns
    -------
    CliRunner
        Runner for creating isolated file  system.
    """
    return CliRunner()


def test_errors() -> None:
    """Test that errors are raised."""
    with pytest.raises(TypeError):
        compare_datasets(np.array([1, 2, 3]))  # type: ignore
    with pytest.raises(TypeError):
        compare_datasets(1.0)  # type: ignore
    with pytest.raises(TypeError):
        compare_datasets(1)  # type: ignore
    with pytest.raises(TypeError):
        compare_datasets("hello")


def test_comparison(runner: CliRunner) -> None:
    """It exits with a status code of zero.

    Parameters
    ----------
    runner : CliRunner
        Runner for creating isolated file systems.
    """
    with runner.isolated_filesystem():
        ds1 = xr.Dataset({"a": (["x", "y"], np.ones((2, 2)))})
        ds1.to_netcdf("ds1.nc")
        ds2 = xr.Dataset({"a": (["x", "y"], np.ones((2, 2)) * 2)})
        compare_datasets("ds1.nc", ds2)
