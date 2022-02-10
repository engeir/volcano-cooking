"""Main file to run the program."""

import os
from typing import List

import click

import volcano_cooking.configurations.shift_eruption_to_date as shift_eruption_to_date
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
    default=[1850, 1, 15],
    show_default=True,
    multiple=True,
    help="Set the first model year. If used with 'shift-eruption-to-date', "
    + "this becomes the year of the eruption and three instances can be used to specify "
    + "year, month, and day of the eruption. ",
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
@click.option(
    "--shift-eruption-to-date",
    "shift_eruption",
    is_flag=False,
    flag_value=True,
    default=False,
    show_default=True,
    type=str,
    help="Shift eruptions of provided file to 'init_year'. "
    + "If no file is provided, the last created file is used.",
)
def main(
    frc: int,
    init_year: List[int],
    size: int,
    lst: bool,
    option: int,
    shift_eruption: str,
) -> None:
    if lst:
        for cl in sv.__GENERATORS__:
            print(f"{cl}: {sv.__GENERATORS__[cl].__name__}")
        return
    _init_year = [1850, 1, 15]
    _init_year[: len(init_year)] = init_year
    if shift_eruption != "False":
        if shift_eruption == "True":
            shift_eruption_to_date.shift_eruption_to_date(tuple(_init_year), None)
        else:
            shift_eruption_to_date.shift_eruption_to_date(
                tuple(_init_year), shift_eruption
            )
    else:
        if option == 1:
            file = os.path.join(
                "data",
                "originals",
                "VolcanEESMv3.11_SO2_850-2016_Mscale_Zreduc_2deg_c191125.nc",
            )
            if not os.path.exists(file):
                raise FileNotFoundError(f"You need the file '{file}' for this option.")
        sv.create_volcanoes(
            size=size, init_year=_init_year[0], version=frc, option=option
        )
