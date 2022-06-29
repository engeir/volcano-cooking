"""Test cases for module synthetic_volcanoes."""

import glob
import json
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
    data = {"dates": ["1850-01-17", "1860-01-01"], "emissions": ["400", "400"]}
    with runner.isolated_filesystem():
        with open("new_file.json", "w") as f:
            json.dump(data, f, indent=2)
        r = len(synthetic_volcanoes.__GENERATORS__)
        for v in range(r):
            file = "new_file.json" if v == 4 else None
            d = os.path.join("data", "output")
            out_npz = os.path.join(os.getcwd(), d, "synthetic_volcanoes_*.npz")
            out_nc = os.path.join(os.getcwd(), d, "synthetic_volcanoes_*.nc")
            synthetic_volcanoes.create_volcanoes(version=v, file=file)
            created_npz = glob.glob(out_npz)[0]
            created_nc = glob.glob(out_nc)[0]
            assert os.path.isfile(created_nc)
            assert os.path.isfile(created_npz)
            os.remove(created_nc)
            os.remove(created_npz)
