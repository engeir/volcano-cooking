# Volcano Cooking

[![codecov](https://codecov.io/gh/engeir/volcano-cooking/branch/main/graph/badge.svg?token=8I5VE7LYA4)](https://codecov.io/gh/engeir/volcano-cooking)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> Let's make some volcanoes erupt!

__NOTE:__ The created dates MUST start before the model start. Running CESM2 from year
1850 with the first eruption in 1850 will make it crash. Setting the first eruption to
1849, however, will make it run. The same goes for the end, the model must stop prior to
the last event, otherwise it will crash. This project will make sure one event is placed
ahead of the `init` year, but the end will vary depending on number of events created and
their frequency.

## TODO

- Combine paths with `os.join` instead of hard coded `/`
- Create a template file so need to download original is removed
- Recreate variables with their attributes instead of re-using old. When the new file
  contain more events than the original, we get an `IndexError` since we try to slice more
  indices than we have.

## Install

```sh
git clone https://github.com/engeir/volcano-cooking.git
cd volcano-cooking
poetry install
```

<details><summary><i><b>Installation notes</b></i></summary><br><ul>
The package <code>fppy</code> will not be installed properly since it is specified with
a path to a local copy. To install <code>fppy</code>, clone the <a
href="https://github.com/uit-cosmo/fppy">repo</a> and edit <code>pyproject.toml</code> by
changing the relative path to where you cloned <code>fppy</code>. Alternatively, you can
clone and install <code>fppy</code> into the virtual environment from the root of the
<code>fppy</code> repository with

```sh
pip install -e .
```

</ul></details>

## Usage

There are two packages coming with this project. The main package is the `volcano-cooking`
program, which will create a `.nc` and `.npz` file in the `data/output` directory. With
the `view_frc` program you can quickly view the content of the created files in a plot.

Run from within this repository/directory:

```sh
poetry run volcano-cooking
poetry run view-frc <file.nc>
```

or run as stand-alone programs:

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

### Option 1 (Directly change forcing file)

#### Get forcing file

This option relies on having a working forcing file at hand. We will use the forcing file
that CESM2 places in the `stratvolc` directory of the `cam` model. Download from [this
link][stratvolc-forcing] and place it in the `data/originals` directory, or run command:

```sh
wget --no-check-certificate https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/chem/stratvolc/VolcanEESMv3.11_SO2_850-2016_Mscale_Zreduc_2deg_c191125.nc
```

It's 2.2GB file so it will take some time.

#### Run library

Now the only thing we need to do is running `volcano-cooking` with the flag `-v1`, and
choose the type of forcing we want (see `volcano-cooking --lst`).

### Option 2 (using NCL-script)

#### Create forcing file for CESM2

To be able to create forcing files used by the CESM2 from the newly created synthetic
file, check out the [data_source_files] directory. This holds creation files that uses the
forcing file this project creates to make a new, full forcing file that CESM2 accepts
(examples of such files can be found [here][volc-frc-complete]). For example,
`createVolcEruptV3.1piControl.ncl`. This need a `common.ncl` file, found
[here][common-ncl], in addition to other standard `ncl` libraries. Make sure to edit
`createVolcEruptV3.1piControl.ncl` to read the created file and that the first and last
year cover those used in the created file.

Coordinate files are located [here][coord-file]. For example `fv_1.9x2.5_L30.nc` which can
be used with two degrees resolution in the atmosphere model.

Assuming a directory tree as below and with the above mentioned changes and downloads of
files, the forcing file CESM2 need can be generated by running

```sh
sh _script/create_cesm_frc.sh
```

Finally, the output file should be in `cdf5` format (check by running `ncdump -k
<file.nc>`). Converting to `cdf5` can be done with command

```sh
nccopy -k cdf5 <in-file.nc> <out-file.nc>
```

<details><summary><i><b>Directory tree</b></i></summary><br><ul>

```code
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
# diff data/originals/createVolcEruptV3.1piControl.ncl.original data/originals/createVolcEruptV3.1piControl.ncl
1c1
< load "$CODE_PATH/ncl/lib/common.ncl"
---
> load "/home/een023/programs/miniconda3/ncl/lib/common.ncl"
20,21c20,21
<   res="1deg"
<   print("Horizontal resolution not set; defaulting to 1deg (0.95x1.25). For 1.9x2.5: setenv resolution 2deg")
---
>   res="2deg"
>   print("Horizontal resolution not set; defaulting to 2deg (1.9x2.5). For 0.95x1.25: setenv resolution 1deg")
25c25
<   templateFilename = "/glade/work/mmills/inputdata/grids/coords_1.9x2.5_L88_c150828.nc"
---
>   templateFilename = getenv("COORDS2DEG")
28c28
<     templateFilename = "/glade/work/mmills/inputdata/grids/coords_0.95x1.25_L70_c150828.nc"
---
>     templateFilename = getenv("COORDS1DEG")
56,57c56,57
< filepath="/glade/work/mmills/data/VolcanEESM/"
< outfilepath="/glade/p/acom/acom-climate/cesm2/inputdata/atm/cam/chem/stratvolc/"
---
> filepath=getenv("SYNTH_FILE_DIR")+"/"
> outfilepath=getenv("DATA_OUT")+"/"
59,60c59,60
< infilename   ="volcan-eesm_global_2015_so2-emissions-database_v3.1_c180414"
< infiletype = "nc"
---
> infilename = getenv("SYNTH_BASE")
> infiletype = getenv("SYNTH_EXT")
62c62
< outfilename="VolcanEESMv3.10_piControl_SO2_"+firstYear+"-"+lastYear+"average"
---
> outfilename="VolcanEESMvEnger_piControl_SO2_"+firstYear+"-"+lastYear+"average"
```

</ul></details>

#### Compare created file with a similar used in a default CESM2 experiment

A similar file to those that are created is needed to be able to use some of the scripts
in the `helper_scripts` directory. By default it assumes the file is named
`volcan-eesm_global_2015_so2-emissions-database_v1.0.nc` and that it is placed inside the
`data/originals` directory. You can find this file [here][volc-frc].

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
[coords-repo]: https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/share/scripgrids/
[volc-frc]: http://catalogue.ceda.ac.uk/uuid/bfbd5ec825fa422f9a858b14ae7b2a0d
[volc-frc-complete]: https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/chem/stratvolc/
[stratvolc-forcing]: https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/chem/stratvolc/VolcanEESMv3.11_SO2_850-2016_Mscale_Zreduc_2deg_c191125.nc
