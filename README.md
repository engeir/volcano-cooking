# Volcano Cooking

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

To be able to compare the newly created synthetic file with one that is already used by
CESM2, check out the
[data_source_files](https://svn.code.sf.net/p/codescripts/code/trunk/ncl/emission)
directory. This holds creation files that uses the forcing file this project creates to
make a new, full forcing file that CESM2 accepts. For example,
`createVolcEruptV3.1piControl.ncl`. This need a `common.ncl` file, found
[here](http://svn.code.sf.net/p/codescripts/code/trunk/ncl/lib/common.ncl).

A similar file to those that are created is needed to be able to use some of the scripts
in the `helper_scripts` directory. By default it assumes the file is named
`volcan-eesm_global_2015_so2-emissions-database_v1.0.nc` and that it is placed inside the
`data/originals` directory. You can find this file [here](http://catalogue.ceda.ac.uk/uuid/bfbd5ec825fa422f9a858b14ae7b2a0d).

Coordinate files are located [here](https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/coords/).
For example `fv_1.9x2.5_L30.nc` which can be used with two degrees resolution in the
atmosphere model.

## Todo

-   Fix FPP generation (find good values for gamma, etc.)
-   Create class or similar for generating data in different ways (random normal, FPP,
    etc.)

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
