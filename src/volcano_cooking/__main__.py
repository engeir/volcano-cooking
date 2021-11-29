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
    "--lst/--no-lst",
    default=False,
    show_default=True,
    type=bool,
    help="Show a list of available forcing generators.",
)
def main(frc: int, lst: bool) -> None:
    if lst:
        for cl in sv.__GENERATORS__:
            print(f"{cl}: {sv.__GENERATORS__[cl].__name__}")
    else:
        sv.create_volcanoes(size=3000, version=frc)


if __name__ == "__main__":
    main(0, False)
