#!/bin/sh

# Set variables

## Local
RED='\033[0;31m'
GREEN='\033[0;32m'
BOLD=$(tput bold)
NORM=$(tput sgr0)
COORDS_REMOTE="https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/coords/"

## Global
DATA_ORIG="data/originals"
export DATA_SYNTH="data/output"
export DATA_OUT="data/cesm"
mkdir -p "$DATA_OUT"
THIS_DIR="$1"
NCL_DIR="$1"
export NCL_SCRIPT="createVolcEruptV3.ncl"
COORDS1DEG_FILE="fv_0.9x1.25_L30.nc"
COORDS2DEG_FILE="fv_1.9x2.5_L30.nc"
export COORDS1DEG="$DATA_ORIG/$COORDS1DEG_FILE"
export COORDS2DEG="$DATA_ORIG/$COORDS2DEG_FILE"
SYNTH_FILE=$(find "$DATA_SYNTH" -name "*.nc" -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -f2- -d" ")
export SYNTH_FILE
SYNTH_FILE_DIR=$(dirname "$SYNTH_FILE")
export SYNTH_FILE_DIR
SYNTH_FILE_BASE=$(basename "$SYNTH_FILE")
SYNTH_EXT="${SYNTH_FILE_BASE##*.}"
SYNTH_BASE="${SYNTH_FILE_BASE%.*}"
export SYNTH_BASE
export SYNTH_EXT
export RES="2deg"

# Check if an .env file exists and load from it.
if [ -f .env ]; then
    # NOTE: This needs word splitting, don't quote it.
    export $(grep -v '^#' .env | xargs -d '\n')
fi

# Check availability

if [ -z "$SYNTH_FILE" ]; then
    echo "Cannot find synthetic volcano forcing file. Generate with 'volcano-cooking'."
    exit 1
fi
if ! [ -e "$NCL_DIR/$NCL_SCRIPT" ]; then
    echo "Cannot find file '$NCL_SCRIPT'."
    exit 1
fi
if ! [ -e "$COORDS1DEG" ] && [ "$RES" = "1deg" ]; then
    echo "Cannot find 1deg coordinate file."
    python -c "from volcano_cooking.__main__ import get_forcing_file;get_forcing_file('$COORDS1DEG_FILE', url='$COORDS_REMOTE$COORDS1DEG_FILE', not_forcing=True)"
    [ -e "$COORDS1DEG" ] || exit 1
fi
if ! [ -e "$COORDS2DEG" ] && [ "$RES" = "2deg" ]; then
    echo "Cannot find 2deg coordinate file."
    python -c "from volcano_cooking.__main__ import get_forcing_file;get_forcing_file('$COORDS2DEG_FILE', url='$COORDS_REMOTE$COORDS2DEG_FILE', not_forcing=True)"
    [ -e "$COORDS2DEG" ] || exit 1
fi
if ! type "ncl" >/dev/null; then
    echo "Cannot find ncl executable"
    exit 1
fi

# Write a log file

current_day="$(date +%Y%m%d-%H%M%S)"
mkdir -p "$DATA_OUT"/logs
echo "Creating file with variables:

DATA_ORIG=$DATA_ORIG
DATA_SYNTH=$DATA_SYNTH
DATA_OUT=$DATA_OUT
NCL_SCRIPT=$NCL_SCRIPT
COORDS1DEG=$COORDS1DEG
COORDS2DEG=$COORDS2DEG
SYNTH_FILE=$SYNTH_FILE
SYNTH_FILE_DIR=$SYNTH_FILE_DIR
SYNTH_BASE=$SYNTH_BASE
SYNTH_EXT=$SYNTH_EXT
RES=$RES

Running NCL script...
" >"$DATA_OUT"/logs/"$current_day".log

ncl "$NCL_DIR/$NCL_SCRIPT" 2>&1 | tee -a "$DATA_OUT"/logs/"$current_day".log
echo "$GREEN${BOLD}Log file created at ""$DATA_OUT/logs/""$current_day.log$NORM"
# The file need to be in NetCDF3 format. Could specify this in the ncl script, but the
# nccopy command seems to support more formats, so perhaps it is better to use that(?).
new_file="$(tail <"$DATA_OUT"/logs/"$current_day".log -n1 | awk '{print $5}')"
[ -z "$new_file" ] && echo "$RED${BOLD}No file was created. ${NORM}See the log file for details." && exit 1
if ! echo "$new_file" | grep -q ".*.nc$"; then
    echo "This ($new_file) is not a netCDF file."
    exit 1
fi

# Add attributes to the coordinate `altitude_int`, which we do via the python script
# `easy_fix.py`.
echo "Fixing the attributes of the altitude_int coordinate..."
XRMSG="\n$BOLD${RED}Cannot import xarray.$NORM Activate the environment where you installed the project
and re-run, or run manually with a python interpreter containing xarray as:

    $ echo $new_file | python src/volcano_cooking/modules/create/easy_fix.py

Please also make sure that the final step of making it cdf5 compatible is done:

    $ rm $new_file
    $ nccopy -k cdf5 ${new_file%???}_2.0.nc $new_file
    $ rm ${new_file%???}_2.0.nc
    $ exit 0"
if ! python -c "import xarray" >/dev/null 2>&1; then
    echo "$XRMSG"
    exit 1
fi
echo "$new_file" | python "$THIS_DIR"/modules/create/easy_fix.py

# Make it a `cdf5` compatible file.
rm "$new_file"
nccopy -k cdf5 "${new_file%???}"_2.0.nc "$new_file"
rm "${new_file%???}"_2.0.nc
exit 0
