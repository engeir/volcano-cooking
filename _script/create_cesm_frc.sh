#!/bin/sh

export DATA_ORIG="data/originals"
export DATA_SYNTH="data/output"
export DATA_OUT="data/cesm"
mkdir -p $DATA_OUT
# export NCL_SCRIPT="createVolcEruptV3.1piControl.ncl"
export NCL_SCRIPT="createVolcEruptV3-2.ncl"
export COORDS1DEG="$DATA_ORIG/fv_0.9x1.25_L30.nc"
export COORDS2DEG="$DATA_ORIG/fv_1.9x2.5_L30.nc"
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

ncl "$DATA_ORIG/$NCL_SCRIPT"
exit 0
