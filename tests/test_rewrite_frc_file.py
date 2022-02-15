"""Test cases for the compare_datasets module."""

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
        with pytest.raises(FileNotFoundError):
            synthetic_volcanoes.create_volcanoes(version=2, option=1)
