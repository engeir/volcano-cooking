"""Test cases for module synthetic_volcanoes."""

import datetime
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
            now = datetime.datetime.now().strftime("%Y%m%d_%H%M")
            out_npz = os.path.join(d, f"synthetic_volcanoes_{now}.npz")
            out_nc = os.path.join(d, f"synthetic_volcanoes_{now}.nc")
            synthetic_volcanoes.create_volcanoes(version=v)
            assert os.path.isfile(out_nc)
            assert os.path.isfile(out_npz)
            os.remove(out_nc)
            os.remove(out_npz)
