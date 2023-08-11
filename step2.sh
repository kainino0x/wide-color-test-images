#!/bin/false  # this should be run from inside a python script

OUTFILE=$1
INFILE=$2
ICCPROFILE=$3

# This comes from pypng and is installed to venv/bin.
if [ -n "$ICCPROFILE" ] ; then
    prichunkpng --iccprofile "$ICCPROFILE" "$INFILE" > "$OUTFILE"
else
    prichunkpng "$INFILE" > "$OUTFILE"
fi

# Optional. You can comment this out if optipng is not installed.
# (But note it will make your files MUCH smaller.)
optipng "$OUTFILE"

file "$OUTFILE"
