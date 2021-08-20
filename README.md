# Volcano Cooking

> Let's make some volcanoes erupt!

## Install

```console
$ git clone https://github.com/engeir/volcano-cooking.git
$ cd volcano-cooking
$ poetry install
$ poetry run volcano-cooking
```

```sh
git clone https://github.com/engeir/volcano-cooking.git
cd volcano-cooking
poetry install
poetry run volcano-cooking
```

## Data

To be able to compare the newly created synthetic file with one that is already used by
CESM2, check out the [data_source_files](https://svn.code.sf.net/p/codescripts/code/trunk/ncl/emission)
directory.

Coordinate files are located [here](https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/coords/).
For example `fv_1.9x2.5_L30.nc` which can be used with two degrees resolution in the
atmosphere model.
