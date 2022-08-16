# Volcano Cooking

[![PyPI version](https://img.shields.io/pypi/v/volcano-cooking)](https://pypi.org/project/volcano-cooking/)
[![codecov](https://codecov.io/gh/engeir/volcano-cooking/branch/main/graph/badge.svg?token=8I5VE7LYA4)](https://codecov.io/gh/engeir/volcano-cooking)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> Let's make some volcanoes erupt!

[![asciicast](https://asciinema.org/a/6eOsLnlOikscbXYLJqclxytD3.svg)](https://asciinema.org/a/6eOsLnlOikscbXYLJqclxytD3)

__NOTE:__
The created dates *must* start before the model start. Running CESM2 from year 1850 with
the first eruption in 1850 will make it crash. Setting the first eruption to 1849,
however, will make it run. The same goes for the end, the model must stop prior to the
last event, otherwise it will crash. This project will make sure one event is placed
ahead of the `init` year, but the end will vary depending on number of events created
and their frequency.

## Install

The package is published on [PyPI] and installable via `pip`:

```bash
pip install volcano-cooking
```

To contribute to the project, clone and install the full development version (uses
[poetry] for dependencies):

```bash
git clone https://github.com/engeir/volcano-cooking.git
cd volcano-cooking
poetry install
pre-commit install
```

Before committing new changes to a branch you can run command

```bash
nox
```

to run the full test suite. You will need [Poetry], [nox] and [nox-poetry] installed for
this.

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

When running the command `volcano-cooking --run-ncl`, a few environment variables will
be used, which can be controlled by setting them in a `.env` file. See
[`.env.example`](./.env.example) to see some default values. With this you can for
example easily change the grid resolution to be `1deg` rather than `2deg` (default).

If you want to change this to an even grater extent, you may be able to set this in the
`.env` file, otherwise fork the repo and make your own version!

> For more complete examples, have a look at the `examples` directory. Cloning this
> repository and running `volcano-cooking --file json.json` from *inside* the `examples`
> directory will result in some output files generated to a new `data` directory inside
> `examples`. If you further rename `.env.example` → `.env` you may also run
> `volcano-cooking --run-ncl` and `volcano-cooking --package-last` (this assumes you
> follow option 0, see below).

### Option 0 (default, using NCL-script)

#### TL;DR

```console
$ volcano-cooking -f 1 -s 100
Generating with 'GenerateFPP'...
$ volcano-cooking --run-ncl
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
$ volcano-cooking --package-last
Successfully placed all latest source files in the 'source-files' directory.
$ ls source-files
20220502-140022.log                     VolcanEESMv3.11Enger_SO2_850-2016_Mscale_Zreduc_2deg_c20220502-140023.nc
synthetic_volcanoes_20220502_135956.nc  synthetic_volcanoes_20220502_135956.npz
```

#### Dependencies

This option needs

- `volcano-cooking` installed
- A coordinate file (~ 10 kB)
- [`ncl`](https://www.ncl.ucar.edu/Download/) executable

#### Create source file for forcing

Run command `volcano-cooking` with the options you want. See `volcano-cooking --help`.

#### Create forcing file for CESM2

> Running the [_script/create_cesm_frc.sh](_script/create_cesm_frc.sh) script depends on
> having `ncl` installed. See installation instructions
> [here](https://www.ncl.ucar.edu/Download/).

After having run the `volcano-cooking` command, the forcing file for CESM2 can be
generated by running

```bash
volcano-cooking --run-ncl
```

If the needed coordinate files are missing, you will be asked if you want to download
them. If you want to use different files, or change the default resolution (default is 2
degrees), edit [.env](./.env.example) accordingly. In this case, you also need to
manually download whatever coordinate file you want to use. See section [Setting up
manually](#setting-up-manually).

#### Wrap up

The last created files, source files, logs and final output, can be nicely collected and
placed in a directory named `source-files` with command:

```sh
volcano-cooking --package-last
```

<details><summary><h4>Setting up manually</h4></summary><br>

To be able to create forcing files used by CESM2 from the newly created synthetic file,
we need a script from the [emissions][data_source_files] directory. These are scripts
that use the forcing file this project generates to make a new, full forcing file that
CESM2 accepts (examples of such files can be found [here][volc-frc-complete]). For
example, `createVolcEruptV3.ncl` can be found in the [emissions][data_source_files]
directory. This need a `common.ncl` file, found [here][common-ncl], in addition to other
standard `ncl` libraries. Make sure to edit `createVolcEruptV3.ncl` to read the created
file and that the first and last year cover those used in the created file. A working
version of `createVolcEruptV3.ncl` that uses input files generated by `volcano-cooking`
can be found in [data/originals](data/originals). To see what was changed from the
original, run `diff data/originals/createVolcEruptV3.ncl.original
src/volcano_cooking/createVolcEruptV3.ncl`.

Coordinate files are needed when running `createVolcEruptV3.ncl` or similar scripts, and
are located [here][coord-file]. For example `fv_1.9x2.5_L30.nc` which can be used with
two degrees resolution in the atmosphere model. The following commands will download
1 and 2 degree resolution coordinate files, respectively, to the `data/originals`
directory:

```bash
wget --no-check-certificate https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/coords/fv_0.9x1.25_L30.nc --directory-prefix data/originals
wget --no-check-certificate https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/coords/fv_1.9x2.5_L30.nc --directory-prefix data/originals
```

</details>

### Option 1 (directly change forcing file)

#### TL;DR

```console
$ volcano-cooking -f 1 -s 100 -o
Generating with 'GenerateFPP'...
```

#### Dependencies

This option needs

- `volcano-cooking` installed
- A coordinate file (~ 10 kB)
- Original CESM2 forcing file (~ 2.2 GB)

#### Run library

Now the only thing we need to do is running `volcano-cooking` with the flag `-o`, and
choose the type of forcing we want (see `volcano-cooking --lst`):

```bash
volcano-cooking -f 1 -s 100 -o
```

<details><summary><h4>Get forcing and coordinate files manually</h4></summary><br>

> Manually downloading the files and placing them in the correct directory is *not*
> needed. Running the command as shown above will ask you if you want to download the
> files, and place them where they need to be.

This option relies on having a working forcing file and coordinate file at hand. We will
use the forcing file that CESM2 places in the `stratvolc` directory of the `cam` model.
Download from [this link][stratvolc-forcing] and place it in the `data/originals`
directory, or run command:

```bash
wget --no-check-certificate https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/chem/stratvolc/VolcanEESMv3.11_SO2_850-2016_Mscale_Zreduc_2deg_c191125.nc --directory-prefix data/originals
```

It's 2.2 GB file, so it will take some time.

We will also need a coordinate file, specifically `fv_1.9x2.5_L30.nc` which is found
[here][coord-file]. This file is small and quick to download. From the command line:

```bash
wget --no-check-certificate https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/coords/fv_0.9x1.25_L30.nc --directory-prefix data/originals
wget --no-check-certificate https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/coords/fv_1.9x2.5_L30.nc --directory-prefix data/originals
```

</details>

## Extra

### Compare created file with a similar used in a default CESM2 experiment

A similar file to those that are created is needed to be able to use some scripts in the
`helper_scripts` directory. By default, it assumes the file is named
`volcan-eesm_global_2015_so2-emissions-database_v1.0.nc` and that it is placed inside
the `data/originals` directory. You can find this file [here][volc-frc].

[data_source_files]: https://svn.code.sf.net/p/codescripts/code/trunk/ncl/emission
[common-ncl]: http://svn.code.sf.net/p/codescripts/code/trunk/ncl/lib/common.ncl
[coord-file]: https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/coords/
[coords-repo]: https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/share/scripgrids/
[volc-frc]: http://catalogue.ceda.ac.uk/uuid/bfbd5ec825fa422f9a858b14ae7b2a0d
[volc-frc-complete]: https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/chem/stratvolc/
[stratvolc-forcing]: https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/chem/stratvolc/VolcanEESMv3.11_SO2_850-2016_Mscale_Zreduc_2deg_c191125.nc
[pypi]: https://pypi.org/
[nox]: https://nox.thea.codes/en/stable/
[nox-poetry]: https://nox-poetry.readthedocs.io/
[poetry]: https://python-poetry.org
