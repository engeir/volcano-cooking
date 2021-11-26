"""CLI for the view_generated_forcing module.

This implements a wrapper for a function to be able to use it as a standalone program. It
takes a filename as a mandatory input parameter.
"""

import click

import volcano_cooking.helper_scripts.view_generated_forcing as v


@click.command()
@click.argument("filename", type=click.Path(exists=True), required=False)
@click.option(
    "--save/--no-save",
    "-s/-S",
    default=False,
    show_default=True,
    type=bool,
    help="Save the plot",
)
def main(filename: str, save: bool):
    """View a plot of `filename`.

    Parameters
    ----------
    filename: str
        Name of the file you want plotted
    save: bool
        Save the plot. Defaults to False
    """
    v.view_forcing(in_file=filename, save=save)
