#!/bin/sh

# Set variables

export DATA_ORIG="data/originals"
export DATA_SYNTH="data/output"
export DATA_OUT="data/cesm"
mkdir -p $DATA_OUT
# export NCL_SCRIPT="createVolcEruptV3.1piControl.ncl"
export NCL_SCRIPT="createVolcEruptV3.ncl"
export COORDS1DEG="$DATA_ORIG/fv_0.9x1.25_L30.nc"
# export COORDS2DEG="$DATA_ORIG/fv_1.9x2.5_L30.nc"
export COORDS2DEG="$DATA_ORIG/fv_1.9x2.5_L26.nc"
# export COORDS2DEG="$DATA_ORIG/fv_1.9x2.5.nc"
# export COORDS2DEG="$DATA_ORIG/fv_1.9x2.5_nc3000_Nsw084_Nrs016_Co120_Fi001_ZR_GRNL_031819.nc"
SYNTH_FILE=$(find "$DATA_SYNTH" -name "*.nc" -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -f2- -d" ")
export SYNTH_FILE
SYNTH_FILE_DIR=$(dirname "$SYNTH_FILE")
export SYNTH_FILE_DIR
SYNTH_FILE_BASE=$(basename "$SYNTH_FILE")
SYNTH_EXT="${SYNTH_FILE_BASE##*.}"
SYNTH_BASE="${SYNTH_FILE_BASE%.*}"
export SYNTH_BASE
export SYNTH_EXT
export res="2deg"

# Check availability

if [ -z "$SYNTH_FILE" ]; then
    echo "Cannot find synthetic volcano forcing file. Generate with 'volcano-cooking'."
    exit 1
fi
if ! [ -e "$DATA_ORIG/$NCL_SCRIPT" ]; then
    echo "Cannot find file '$NCL_SCRIPT'."
    exit 1
fi
if ! [ -e "$COORDS1DEG" ]; then
    echo "Cannot find 1deg coordinate file."
    exit 1
fi
if ! [ -e "$COORDS2DEG" ]; then
    echo "Cannot find 2deg coordinate file."
    exit 1
fi
if ! type "ncl" > /dev/null; then
    echo "Cannot find ncl executable"
    exit 1
fi

# Write a log file

current_day="$(date +%Y%m%d)"
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
res=$res

Running NCL script...
" > "$DATA_OUT"/logs/"$current_day".log

ncl "$DATA_ORIG/$NCL_SCRIPT" 2>&1 | tee -a "$DATA_OUT"/logs/"$current_day".log
# The file need to be in NetCDF3 format. Could specify this in the ncl script, but the
# nccopy command seems to support more formats, so perhaps it is better to use that(?).
new_file="$(cat "$DATA_OUT"/logs/"$current_day".log | tail -n1 | awk '{print $5}')"
mv $new_file $new_file.old
nccopy -k cdf5 $new_file.old $new_file
rm $new_file.old
exit 0
