"""Test cases for the create_data module."""
import inspect

import volcano_cooking.modules.create.create_data as cr


def test_generate_classes() -> None:
    for n, c in inspect.getmembers(cr, inspect.isclass):
        if c.__module__ == "volcano_cooking.modules.create.create_data":
            if n != "Data" and n != "Generate":
                c_ = c(20, 20)
                assert issubclass(c, cr.Generate)
                c_.generate()
                cr.Data(*c_.get_arrays())
