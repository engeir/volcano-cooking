"""Test cases for the create_data module."""

import inspect
import json

import numpy as np
import pytest
import volcano_cooking.modules.create.create_data as cr
from click.testing import CliRunner


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


def test_generate_from_file(runner: CliRunner) -> None:
    """Test the json file input."""
    d1 = {"dates": ["1850-01-17"], "emissions": ["400", "400"]}
    d2 = {"emissions": ["400", "400"]}
    d3 = {
        "dates": ["1850-01-17", "1860-01-01"],
        "emissions": ["400", "400"],
        "lat": ["0.0", "20.0"],
        "lon": ["120.0", "0.0"],
        "minimum injection height": ["25", "27"],
        "maximum injection height": ["26", "26"],
    }
    with runner.isolated_filesystem():
        with open("new_file.json", "w") as f:
            json.dump(d1, f, indent=2)
        module_ = "volcano_cooking.modules.create.create_data"
        for n, c in inspect.getmembers(cr, inspect.isclass):
            if c.__module__ == module_ and n in ["GenerateFromFile"]:
                c_ = c(20, 20, "new_file.json")
                assert issubclass(c, cr.Generate)
                with pytest.raises(KeyError):
                    c_.generate()
    with runner.isolated_filesystem():
        with open("new_file.json", "w") as f:
            json.dump(d2, f, indent=2)
        module_ = "volcano_cooking.modules.create.create_data"
        for n, c in inspect.getmembers(cr, inspect.isclass):
            if c.__module__ == module_ and n in ["GenerateFromFile"]:
                c_ = c(20, 20, "new_file.json")
                assert issubclass(c, cr.Generate)
                with pytest.raises(KeyError):
                    c_.generate()
    with runner.isolated_filesystem():
        with open("new_file.json", "w") as f:
            json.dump(d3, f, indent=2)
        module_ = "volcano_cooking.modules.create.create_data"
        for n, c in inspect.getmembers(cr, inspect.isclass):
            if c.__module__ == module_ and n in ["GenerateFromFile"]:
                c_ = c(20, 20, "new_file.json")
                assert issubclass(c, cr.Generate)
                c_.generate()
                ds = cr.Data(*c_.get_arrays())
                assert np.array_equal(ds.lats, np.array(d3["lat"], dtype=np.float32))
                assert np.array_equal(ds.lons, np.array(d3["lon"], dtype=np.float32))
                assert np.array_equal(ds.miihs, np.array([25, 26], dtype=np.float32))
                assert np.array_equal(ds.mxihs, np.array([26, 27], dtype=np.float32))
                assert np.array_equal(
                    ds.tes, np.array(d3["emissions"], dtype=np.float32)
                )
                assert np.array_equal(ds.yoes, np.array([1850, 1860], dtype=np.int16))
                assert np.array_equal(ds.moes, np.array([1, 1], dtype=np.float32))
                assert np.array_equal(ds.does, np.array([17, 1], dtype=np.float32))
