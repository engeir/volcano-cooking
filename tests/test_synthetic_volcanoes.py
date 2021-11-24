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
        d = "data/output"
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        out_npz = f"{d}/synthetic_volcanoes_{now}.npz"
        out_nc = f"{d}/synthetic_volcanoes_{now}.npz"
        synthetic_volcanoes.create_volcanoes()
        assert os.path.isfile(out_nc)
        assert os.path.isfile(out_npz)
