# Volcano Cooking

[![codecov](https://codecov.io/gh/engeir/volcano-cooking/branch/main/graph/badge.svg?token=8I5VE7LYA4)](https://codecov.io/gh/engeir/volcano-cooking)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> Let's make some volcanoes erupt!

## Install

```sh
git clone https://github.com/engeir/volcano-cooking.git
cd volcano-cooking
poetry install
```

## Usage

There are two packages coming with this project. The main package is the `volcano-cooking`
program, which will create a `.nc` and `.npz` file in the `data/output` directory. With
the `view_frc` program you can quickly view the content of the created files in a plot.

Run from within this repository/directory:
```sh
poetry run volcano-cooking
poetry run view-frc <file.nc>
```

or run as standalone programs:

```sh
volcano-cooking
view-frc <file.nc>
```

An optional flag can be sent to the `view-frc` program that will save the plot: `view-frc
-s <file.nc>`.

In either case a `data/output` directory will be created at the root of the project (first
case) or inside the current directory (second case) when something is saved.

## Data

### Create forcing file for CESM2

To be able to create forcing files used by the CESM2 from the newly created synthetic
file, check out the
[data_source_files](https://svn.code.sf.net/p/codescripts/code/trunk/ncl/emission)
directory. This holds creation files that uses the forcing file this project creates to
make a new, full forcing file that CESM2 accepts. For example,
`createVolcEruptV3.1piControl.ncl`. This need a `common.ncl` file, found
[here](http://svn.code.sf.net/p/codescripts/code/trunk/ncl/lib/common.ncl), in addition to
other standard `ncl` libraries. Make sure to edit `createVolcEruptV3.1piControl.ncl` to
read the created file and that the first and last year cover those used in the created
file.

Coordinate files are located
[here](https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/coords/). For
example `fv_1.9x2.5_L30.nc` which can be used with two degrees resolution in the
atmosphere model.

### Compare created file with a similar used in a default CESM2 experiment

A similar file to those that are created is needed to be able to use some of the scripts
in the `helper_scripts` directory. By default it assumes the file is named
`volcan-eesm_global_2015_so2-emissions-database_v1.0.nc` and that it is placed inside the
`data/originals` directory. You can find this file [here](http://catalogue.ceda.ac.uk/uuid/bfbd5ec825fa422f9a858b14ae7b2a0d).

## Todo

-   Fix FPP generation (find good values for gamma, etc.)
-   Move to use only `fppy` package, remove `uit_scripts` dependency.

### FPP

In the long run, this project should be able to produce volcanic forcing files where the
volcanic eruptions are generated from an FPP.

From the FPP we get arrival times and amplitudes. While it is obvious how the arrival
times should be input into the generation process, this is not the case with the
amplitudes.

The most natural variable to adjust according to the amplitudes is the total emission.

### Generator class

Since the volcanoes can conceivably be generated in different ways, it might be a good
idea to create a class which takes in all the variables that are needed and then checks
that all have correct properties.
