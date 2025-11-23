#!/bin/sh

# Ensure proper spacing in conditions
if [ $# -lt 2 ]; then
    echo "Usage: entrypoint.sh <input-file> <output-file>"
    exit 1
fi

# Run parser
python /app/metadata_parser.py "$1" "$2"

# Run normalizer
python /app/normalize_dates.py
