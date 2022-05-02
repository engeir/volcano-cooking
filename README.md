# Volcano Cooking

[![codecov](https://codecov.io/gh/engeir/volcano-cooking/branch/main/graph/badge.svg?token=8I5VE7LYA4)](https://codecov.io/gh/engeir/volcano-cooking)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> Let's make some volcanoes erupt!

__NOTE:__
The created dates *must* start before the model start. Running CESM2 from year 1850 with
the first eruption in 1850 will make it crash. Setting the first eruption to 1849,
however, will make it run. The same goes for the end, the model must stop prior to the
last event, otherwise it will crash. This project will make sure one event is placed
ahead of the `init` year, but the end will vary depending on number of events created
and their frequency.

## Install

This repo is currently intended to be installed from source only. To install all
dependencies, clone the repo and install with [poetry](https://python-poetry.org):

```sh
git clone https://github.com/engeir/volcano-cooking.git
cd volcano-cooking
poetry install
# or, without development dependencies:
poetry install --no-dev
```

## Dependencies

Creating forcing files on the same format as
[`volcan-eesm_global_2015_so2-emissions-database_v1.0.nc`][volc-frc] depend on the
python project only. If you want to also create the forcing file that is input to CESM2,
done with the `-o` option for `volcano-cooking` (see
[section](#option-1-(directly-change-forcing-file))) or with the
[_script/create_cesm_frc.sh](_script/create_cesm_frc.sh) script, you also need `ncl`
installed. See installation instructions [here](https://www.ncl.ucar.edu/Download/).

## Usage

There are two CLI programs coming with this project. The main program is
`volcano-cooking`, which will create a `.nc` and `.npz` file in the `data/output`
directory. With the `view_frc` program you can quickly view the content of the created
files in a plot.

Run from within this repository/directory via poetry:

```sh
poetry run volcano-cooking
poetry run view-frc <file.nc>
```

or, if the virtual environment where the project is installed is activated:

```sh
volcano-cooking
view-frc <file.nc>
```

An optional flag can be sent to the `view-frc` program that will save the plot:
`view-frc -s <file.nc>`.

In either case a `data/output` directory will be created inside the current directory
when something is saved.

For more options to either `volcano-cooking` or `view-frc`, see

```sh
volcano-cooking --help
view-frc --help
```

## Data

### Option 0 (default, using NCL-script)

#### TL;DR

```console
$ volcano-cooking -f 1 -s 100
Generating with 'GenerateFPP'...
$ sh _script/create_cesm_frc.sh
 Copyright (C) 1995-2019 - All Rights Reserved
 University Corporation for Atmospheric Research
 NCAR Command Language Version 6.6.2
 The use of this software is governed by a License Agreement.
 See http://www.ncl.ucar.edu/ for more details.
(0)     in data/originals/createVolcEruptV3.ncl
...
  long_name :   SO2 elevated emissions from explosive volcanoes
  _FillValue :  9.96921e+36
(0)     saving stratvolc
(0)     File creation complete: data/cesm/VolcanEESMv3.11Enger_SO2_850-2016_Mscale_Zreduc_2deg_c20220502-140023.nc
Log file created at data/cesm/logs/20220502-140022.log
Fixing the attributes of the altitude_int coordinate...
$ sh _script/package_last.sh
Successfully placed all latest source files in the 'source-files' directory.
$ ls source-files
20220502-140022.log                     VolcanEESMv3.11Enger_SO2_850-2016_Mscale_Zreduc_2deg_c20220502-140023.nc
synthetic_volcanoes_20220502_135956.nc  synthetic_volcanoes_20220502_135956.npz
```

#### Setting up

To be able to create forcing files used by CESM2 from the newly created synthetic file,
we need a script from the [data_source_files] directory. These are scripts that use the
forcing file this project generates to make a new, full forcing file that CESM2 accepts
(examples of such files can be found [here][volc-frc-complete]). For example,
`createVolcEruptV3.ncl` can be found in [data_source_files]. This need a `common.ncl`
file, found [here][common-ncl], in addition to other standard `ncl` libraries. Make sure
to edit `createVolcEruptV3.ncl` to read the created file and that the first and last
year cover those used in the created file. A working version of `createVolcEruptV3.ncl`
that uses input files generated by `volcano-cooking` can be found in
[data/originals](data/originals). To see what was changed from the original, run `diff
createVolcEruptV3.ncl createVolcEruptV3.ncl.original`.

Coordinate files are needed when running `createVolcEruptV3.ncl` or similar scripts, and
are located [here][coord-file]. For example `fv_1.9x2.5_L30.nc` which can be used with
two degrees resolution in the atmosphere model. The following commands will download
1 and 2 degree resolution coordinate files, respectively, to the `data/originals`
directory:

```sh
wget --no-check-certificate https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/coords/fv_0.9x1.25_L30.nc --directory-prefix data/originals
wget --no-check-certificate https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/coords/fv_1.9x2.5_L30.nc --directory-prefix data/originals
```

#### Create source file for forcing

Run command `volcano-cooking` with the options you want. See `volcano-cooking --help`.

#### Create forcing file for CESM2

Assuming a directory tree as below and with the coordinate files downloaded, in addition
to having run the `volcano-cooking` command, the forcing file for CESM2 can be generated
by running

```sh
sh _script/create_cesm_frc.sh
```

#### Wrap up

The last created files, source files, logs and final output, can be nicely collected and
placed in a directory named `source-files` with command:

```sh
sh _script/package_last.sh
```

<details><summary><i><b>Directory tree</b></i></summary><br><ul>

```code
.
├── data
│   ├── originals
│   │   ├── createVolcEruptV3.ncl
│   │   ├── createVolcEruptV3.ncl.original
│   │   ├── fv_0.9x1.25_L30.nc
│   │   ├── fv_1.9x2.5_L30.nc
│   │   └── volcan-eesm_global_2015_so2-emissions-database_v1.0.nc
│   └── output
│       ├── synthetic_volcanoes_20211126_1128.nc
│       └── synthetic_volcanoes_20211126_1128.npz
├── LICENSE
├── poetry.lock
├── pyproject.toml
├── README.md
├── _script
│   ├── create_cesm_frc.sh
│   └── package_last.sh
├── setup.cfg
├── src
│   └── ...
└── tests
    └── ...
```

</ul></details>

### Option 1 (directly change forcing file)

#### TL;DR

```console
$ volcano-cooking -f 1 -s 100 -o
Generating with 'GenerateFPP'...
```

#### Get forcing and coordinate files

This option relies on having a working forcing file at hand. We will use the forcing
file that CESM2 places in the `stratvolc` directory of the `cam` model. Download from
[this link][stratvolc-forcing] and place it in the `data/originals` directory, or run
command:

```sh
wget --no-check-certificate https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/chem/stratvolc/VolcanEESMv3.11_SO2_850-2016_Mscale_Zreduc_2deg_c191125.nc --directory-prefix data/originals
```

It's 2.2 GB file, so it will take some time.

We will also need a coordinate file, specifically `fv_1.9x2.5.nc` which is found
[here][coord-file]. This file is small and quick to download. From the command line:

```sh
wget --no-check-certificate https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/coords/fv_0.9x1.25_L30.nc --directory-prefix data/originals
wget --no-check-certificate https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/coords/fv_1.9x2.5_L30.nc --directory-prefix data/originals
```

#### Run library

Now the only thing we need to do is running `volcano-cooking` with the flag `-o`, and
choose the type of forcing we want (see `volcano-cooking --lst`):

```sh
volcano-cooking -f 1 -s 100 -o
```

## Extra

### Compare created file with a similar used in a default CESM2 experiment

A similar file to those that are created is needed to be able to use some scripts in the
`helper_scripts` directory. By default, it assumes the file is named
`volcan-eesm_global_2015_so2-emissions-database_v1.0.nc` and that it is placed inside
the `data/originals` directory. You can find this file [here][volc-frc].

## TODO

- [ ] Simplify process of creating new forcing generator classes

[data_source_files]: https://svn.code.sf.net/p/codescripts/code/trunk/ncl/emission
[common-ncl]: http://svn.code.sf.net/p/codescripts/code/trunk/ncl/lib/common.ncl
[coord-file]: https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/coords/
[coords-repo]: https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/share/scripgrids/
[volc-frc]: http://catalogue.ceda.ac.uk/uuid/bfbd5ec825fa422f9a858b14ae7b2a0d
[volc-frc-complete]: https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/chem/stratvolc/
[stratvolc-forcing]: https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/chem/stratvolc/VolcanEESMv3.11_SO2_850-2016_Mscale_Zreduc_2deg_c191125.nc
