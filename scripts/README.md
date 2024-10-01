# Scripts

## Raster scripts
refer to each script `.sh` file for documentation


## Vector scripts
You need nix installed, alternatively you can install `gdal` and `tippecanoe` in your system.

```
$ nix-shell
$ pip install -e .
$ genarate_pmtiles path/to/file.gpkg  
```

This script will split each layer into a separate gpkg file, then convert each to GeoJSON and use `tippecanoe` to generate a PMTiles with all the layers together.
