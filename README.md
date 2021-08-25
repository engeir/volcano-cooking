# Volcano Cooking

> Let's make some volcanoes erupt!

## Install

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

## Todo

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
