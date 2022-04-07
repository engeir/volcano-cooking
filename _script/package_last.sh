#!/bin/sh

## Local
GREEN='\033[0;32m'
BOLD=$(tput bold)
NORM=$(tput sgr0)

DATA_SYNTH="data/output"
DATA_OUT="data/cesm"
DATA_LOG="data/cesm/logs"

SYNTH_FILE=$(find "$DATA_SYNTH" -name "*.nc" -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -f2- -d" ")
SYNTH_BASE="${SYNTH_FILE%.*}"
SYNTH_NC="$SYNTH_BASE.nc"
SYNTH_NPZ="$SYNTH_BASE.npz"
CESM_FILE=$(find "$DATA_OUT" -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -f2- -d" ")
LOG_FILE=$(find "$DATA_LOG" -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -f2- -d" ")

if [ -z "$SYNTH_NC" ]; then
    echo "Cannot find synthetic nc file."
    exit 1
fi
if [ -z "$SYNTH_NPZ" ]; then
    echo "Cannot find synthetic npz file."
    exit 1
fi
if [ -z "$CESM_FILE" ]; then
    echo "Cannot find CESM file."
    exit 1
fi
if [ -z "$LOG_FILE" ]; then
    echo "Cannot find log file."
    exit 1
fi

mkdir -p source-files
mv "$SYNTH_NC" source-files
mv "$SYNTH_NPZ" source-files
mv "$CESM_FILE" source-files
mv "$LOG_FILE" source-files

echo "$GREEN${BOLD}Successfully placed all latest source files in the 'source-files' directory.$NORM"
