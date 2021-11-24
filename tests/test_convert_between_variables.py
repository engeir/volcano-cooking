"""Test cases for the convert_between_variables module."""
import numpy as np
import pytest

from volcano_cooking.modules import convert


def test_vei_to_totalemission() -> None:
    a = np.arange(100)
    b = [1, 2, 3, 4]
    c = np.arange(10, dtype=np.int8)
    with pytest.raises(ValueError):
        convert.vei_to_totalemission(a)
        convert.vei_to_totalemission(b)
    out = convert.vei_to_totalemission(c)
    assert isinstance(out, np.ndarray)
    assert out.dtype == np.float32
    assert out.shape == c.shape


def test_totalemission_to_vei() -> None:
    a = np.arange(100)
    b = [1, 2, 3, 4]
    c = np.linspace(1, 10, 100)
    with pytest.raises(ZeroDivisionError):
        convert.totalemission_to_vei(a)
    with pytest.raises(TypeError):
        convert.totalemission_to_vei(b)
    out = convert.totalemission_to_vei(c)
    assert out.dtype == np.int8
    assert out.shape == c.shape


def test_vei_to_injectionheight() -> None:
    vei = np.random.randint(1, 7, 20)
    out1, out2 = convert.vei_to_injectionheights(vei)
    assert out1.shape == out2.shape
    assert out1.dtype == np.float32
    assert out2.dtype == np.float32
    for i, j in zip(out1, out2):
        assert i <= j
