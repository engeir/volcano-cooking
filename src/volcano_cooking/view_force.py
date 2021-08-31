"""CLI for the view_synthetic_forcing function.

This implements a wrapper for a function to be able to use it as a standalone program. It
takes a filename as a mandatory input parameter.
"""

import click

import volcano_cooking.helper_scripts.view_generated_forcing as v


@click.command()
@click.argument("filename")
def main(filename):
    """View a plot of `filename`.

    Parameters
    ----------
    filename: str
        Name of the file you want plotted
    """
    v.view_forcing(".nc", in_file=filename)
