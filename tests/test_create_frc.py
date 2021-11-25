"""Test cases for module create_frc."""

import inspect

import volcano_cooking.modules.create.create_frc as m


def test_frc_class_method() -> None:
    for n, c in inspect.getmembers(m, inspect.isclass):
        if c.__module__ == "volcano_cooking.modules.create.create_frc":
            if n != "FrcGenerator":
                c()
                assert issubclass(c, m.FrcGenerator)


def test_output() -> None:
    size = 500
    f = m.StdFrc(fs=1, total_pulses=size)
    out1, out2 = f.get_frc()
    assert out1.shape == out2.shape
    assert out2.shape == (size,)
    f = m.Frc(fs=1, size=size)
    out1, out2 = f.get_fpp()
    out3, out4 = f.get_frc()
    assert out1.shape == out2.shape
    assert out2.shape == (size,)
    assert out3.shape == out4.shape
    assert len(out1) > len(out3)


if __name__ == "__main__":
    test_frc_class_method()
    test_output()
