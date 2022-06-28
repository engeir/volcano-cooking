"""Test cases for the create_data module."""
import inspect
import json

import pytest
from click.testing import CliRunner

import volcano_cooking.modules.create.create_data as cr


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces.

    Returns
    -------
    CliRunner
        Runner for creating isolated file  system.
    """
    return CliRunner()


def test_generate_classes(runner: CliRunner) -> None:
    """Test to see if classes are being generated."""
    data = {"dates": ["1850-01-17", "1860-01-01"], "emissions": ["400", "400"]}
    with runner.isolated_filesystem():
        with open("new_file.json", "w") as f:
            json.dump(data, f, indent=2)
        module_ = "volcano_cooking.modules.create.create_data"
        for n, c in inspect.getmembers(cr, inspect.isclass):
            if c.__module__ == module_ and n not in ["Data", "Generate"]:
                c_ = c(20, 20, "new_file.json")
                assert issubclass(c, cr.Generate)
                c_.generate()
                cr.Data(*c_.get_arrays())
