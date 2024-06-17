"""Test cases for module sparse_to_lin."""

import datetime
import os

import numpy as np
import pytest
from click.testing import CliRunner
from volcano_cooking import sparse_to_lin, synthetic_volcanoes


def test_sparse_to_lin() -> None:
    """Test the conversion from sparse to linear time."""
    t = np.array(
        [
            0,
            1e-3,
            2e-3,
            3e-3,
            4e-3,
            5e-3,
            4,
            6,
            7.85,
            7.91,
            7.92,
            7.925,
            7.93,
            7.96,
            7.99,
            8.001,
            8.002,
            8.003,
        ]
    )
    correct = np.array([0, 4, 6, 7.85, 7.92, 8.001])
    t2, t_m, t2_m = sparse_to_lin.sparse_to_lin(t)
    assert t[t_m].shape == t2[t2_m].shape
    assert np.array_equal(t[t_m], correct)
    # Check that all integer years are there (i.e. we hit January each year).
    for i in range(int(t[0]), int(t[-1])):
        assert i in t2
    # Finally, the masked arrays should be equal to within half a month.
    assert np.allclose(t[t_m], t2[t2_m], atol=1 / 24)


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces.

    Returns
    -------
    CliRunner
        Runner for testing CLI.
    """
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero.

    Parameters
    ----------
    runner : CliRunner
        Runner for creating isolated file systems.
    """
    with runner.isolated_filesystem():
        d = os.path.join("data", "output")
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        out_npz = os.path.join(d, f"synthetic_volcanoes_{now}.npz")
        v = len(synthetic_volcanoes.__GENERATORS__) - 2
        synthetic_volcanoes.create_volcanoes(version=v)
        result = runner.invoke(sparse_to_lin.main, [out_npz])
        assert result.exit_code == 0
