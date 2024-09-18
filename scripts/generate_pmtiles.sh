#!/usr/bin/env nix-shell
#!nix-shell -p gdal
#!nix-shell -i bash

# generate_pmtiles
# Converts a GeoPackage file to PMTiles
# Output PMTiles file can be checked here: https://pmtiles.io/
# Arguments:
#   $1: Path to input GeoPackage file
#   $2: Path to output PMTiles file
#   $4: Maximum zoom level (e.g. 15, larger than 15 is not recommended)
#   $3: Minimum zoom level (e.g. 9, default: 0)
# Usage: generate_pmtiles /path/to/input.gpkg /path/to/output.pmtiles 15 12

input=$1
output=$2
maxzoom=${3:- 15}
minzoom=${4:-0}

ogr2ogr -skipfailures -f PMTiles "$output" "$input" -dsco MAXZOOM="$maxzoom" -dsco MINZOOM="$minzoom"
