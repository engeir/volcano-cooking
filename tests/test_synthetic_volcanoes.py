"""Test cases for module synthetic_volcanoes."""

import glob
import os

import pytest
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
        r = len(synthetic_volcanoes.__GENERATORS__)
        for v in range(r):
            d = os.path.join("data", "output")
            out_npz = os.path.join(os.getcwd(), d, "synthetic_volcanoes_*.npz")
            out_nc = os.path.join(os.getcwd(), d, "synthetic_volcanoes_*.nc")
            synthetic_volcanoes.create_volcanoes(version=v)
            created_npz = glob.glob(out_npz)[0]
            created_nc = glob.glob(out_nc)[0]
            assert os.path.isfile(created_nc)
            assert os.path.isfile(created_npz)
            os.remove(created_nc)
            os.remove(created_npz)
