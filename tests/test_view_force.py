"""Test cases for module view_force."""


from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from volcano_cooking import synthetic_volcanoes, view_force


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces.

    Returns
    -------
    CliRunner
        Runner for creating isolated file  system.
    """
    return CliRunner()


@patch("matplotlib.pyplot.figure")
def test_main_succeeds(mock_fig: MagicMock, runner: CliRunner) -> None:
    """It exits with a status code of zero.

    Parameters
    ----------
    mock_fig: MagicMock
        Suppress call to plt.show().
    runner: CliRunner
        Runner for creating isolated file systems.
    """
    r = len(synthetic_volcanoes.__GENERATORS__)
    for v in range(r):
        with runner.isolated_filesystem():
            synthetic_volcanoes.create_volcanoes(version=v)
            result = runner.invoke(view_force.main)
            mock_fig.assert_called()
            assert result.exit_code == 0
