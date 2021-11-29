# Volcano Cooking

[![codecov](https://codecov.io/gh/engeir/volcano-cooking/branch/main/graph/badge.svg?token=8I5VE7LYA4)](https://codecov.io/gh/engeir/volcano-cooking)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> Let's make some volcanoes erupt!

## TODO

-   Add forcing generator: single volcano at third year for easier testing.

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
case) or inside the current directory (second case) when something is saved with a file
named `synthetic_volcanoes_<date>.nc`.

## Data

### Create forcing file for CESM2

To be able to create forcing files used by the CESM2 from the newly created synthetic
file, check out the [data_source_files] directory. This holds creation files that uses the
forcing file this project creates to make a new, full forcing file that CESM2 accepts. For
example, `createVolcEruptV3.1piControl.ncl`. This need a `common.ncl` file, found
[here](common-nlc), in addition to other standard `ncl` libraries. Make sure to edit
`createVolcEruptV3.1piControl.ncl` to read the created file and that the first and last
year cover those used in the created file.

Coordinate files are located [here](coord-file). For example `fv_1.9x2.5_L30.nc` which can
be used with two degrees resolution in the atmosphere model.

Assuming a directory tree as below and with the above mentioned changes and downloads of
files, the forcing file CESM2 need can be generated by running

```sh
sh _script/create_cesm_frc.sh
```


<details><summary><i><b>Directory tree</b></i></summary><br><ul>

```
.
├── data
│   ├── originals
│   │   ├── createVolcEruptV3.1piControl.ncl
│   │   ├── createVolcEruptV3.1piControl.ncl.original
│   │   ├── fv_0.9x1.25_L30.nc
│   │   ├── fv_1.9x2.5_L30.nc
│   │   ├── volcan-eesm_global_2015_so2-emissions-database_v1.0.nc
│   └── output
│       ├── synthetic_volcanoes_20211126_1128.nc
│       └── synthetic_volcanoes_20211126_1128.npz
├── LICENSE
├── poetry.lock
├── pyproject.toml
├── README.md
├── _script
│   └── create_cesm_frc.sh
├── setup.cfg
├── src
│   └── ...
└── tests
    └── ...
```

</ul></details>

<details><summary><i><b>Diff between edited ncl script and original</b></i></summary><br><ul>

```diff
# diff data/originals/createVolcEruptV3.1piControl.ncl data/originals/createVolcEruptV3.1piControl.ncl.original
1c1
< load "/home/een023/programs/miniconda3/ncl/lib/common.ncl"
---
> load "$CODE_PATH/ncl/lib/common.ncl"
20,21c20,21
<   res="2deg"
<   print("Horizontal resolution not set; defaulting to 2deg (1.9x2.5). For 0.95x1.25: setenv resolution 1deg")
---
>   res="1deg"
>   print("Horizontal resolution not set; defaulting to 1deg (0.95x1.25). For 1.9x2.5: setenv resolution 2deg")
25c25
<   templateFilename = getenv("COORDS2DEG")
---
>   templateFilename = "/glade/work/mmills/inputdata/grids/coords_1.9x2.5_L88_c150828.nc"
28c28
<     templateFilename = getenv("COORDS1DEG")
---
>     templateFilename = "/glade/work/mmills/inputdata/grids/coords_0.95x1.25_L70_c150828.nc"
56,57c56,57
< filepath=getenv("SYNTH_FILE_DIR")+"/"
< outfilepath=getenv("DATA_OUT")+"/"
---
> filepath="/glade/work/mmills/data/VolcanEESM/"
> outfilepath="/glade/p/acom/acom-climate/cesm2/inputdata/atm/cam/chem/stratvolc/"
59,60c59,60
< infilename = getenv("SYNTH_BASE")
< infiletype = getenv("SYNTH_EXT")
---
> infilename   ="volcan-eesm_global_2015_so2-emissions-database_v3.1_c180414"
> infiletype = "nc"
62c62
< outfilename="VolcanEESMvEnger_piControl_SO2_"+firstYear+"-"+lastYear+"average"
---
> outfilename="VolcanEESMv3.10_piControl_SO2_"+firstYear+"-"+lastYear+"average"
```

</ul></details>

### Compare created file with a similar used in a default CESM2 experiment

A similar file to those that are created is needed to be able to use some of the scripts
in the `helper_scripts` directory. By default it assumes the file is named
`volcan-eesm_global_2015_so2-emissions-database_v1.0.nc` and that it is placed inside the
`data/originals` directory. You can find this file [here](volc-frc).

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

[data_source_files]: https://svn.code.sf.net/p/codescripts/code/trunk/ncl/emission
[common-ncl]: http://svn.code.sf.net/p/codescripts/code/trunk/ncl/lib/common.ncl
[coord-file]: https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/coords/
[vold-frc]: http://catalogue.ceda.ac.uk/uuid/bfbd5ec825fa422f9a858b14ae7b2a0d
