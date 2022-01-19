"""Main file to run the program."""

import os

import click

import volcano_cooking.synthetic_volcanoes as sv
from volcano_cooking import __version__


@click.command()
@click.version_option(version=__version__)
@click.option(
    "-o",
    "--option",
    count=True,
    show_default=True,
    help="Set the data creation option. "
    + "The default is option 0, -o gives option 1.",
)
@click.option(
    "frc",
    "-f",
    type=int,
    default=0,
    show_default=True,
    help="Choose what forcing generator to use. "
    + "See volcano-cooking --lst for a list of all available generators.",
)
@click.option(
    "init_year",
    "-init",
    type=int,
    default=1850,
    show_default=True,
    help="Set the first model year.",
)
@click.option(
    "size",
    "-s",
    type=int,
    default=3000,
    show_default=True,
    help="Set the number of volcanoes to generate.",
)
@click.option(
    "--lst/--no-lst",
    default=False,
    show_default=True,
    type=bool,
    help="Show a list of available forcing generators.",
)
def main(frc: int, init_year: int, size: int, lst: bool, option: int) -> None:
    if lst:
        for cl in sv.__GENERATORS__:
            print(f"{cl}: {sv.__GENERATORS__[cl].__name__}")
    else:
        if option == 1:
            file = os.path.join(
                "data",
                "originals",
                "VolcanEESMv3.11_SO2_850-2016_Mscale_Zreduc_2deg_c191125.nc",
            )
            if not os.path.exists(file):
                raise FileNotFoundError(f"You need the file '{file}' for this option.")
        sv.create_volcanoes(size=size, init_year=init_year, version=frc, option=option)


if __name__ == "__main__":
    main(0, False)
