"""Main file to run the program."""

import click

import volcano_cooking.synthetic_volcanoes as sv


@click.command()
@click.option(
    "frc",
    "-f",
    type=int,
    default=0,
    show_default=True,
    help="Choose what forcing generator to use. See volcano-cooking --lst for a list of all available generators.",
)
@click.option(
    "init_year",
    "-init",
    type=int,
    default=1850,
    show_default=True,
    help="Set the first year.",
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
def main(frc: int, init_year: int, size: int, lst: bool) -> None:
    if lst:
        for cl in sv.__GENERATORS__:
            print(f"{cl}: {sv.__GENERATORS__[cl].__name__}")
    else:
        sv.create_volcanoes(size=size, init_year=init_year, version=frc)


if __name__ == "__main__":
    main(0, False)
