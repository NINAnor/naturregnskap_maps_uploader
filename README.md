

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -e .

touch .env
```

- Create a Map in the catalogue (via admin)
- Create a token for your user in the catalogue (via admin)

in the `.env` file add:
```
AUTH_TOKEN=my_token
DEBUG=True
```

## How to use
Customize the `style.json` file accordingly, you can use the option `--style` if your file has a different name
You'll need a `schema.xlsx` file that describes the project, you can use the option `--schema` if your file has a different name

Run the following command

```
naturregnskap_maps_uploader_start {http://localhost:8000} {my_map_slug}
```

replace the url with the right address and the map slug with yours



## Preparing the data
requirements: GDAL

**NOTE**: `GDAL_NUM_THREADS=ALL_CPUS` will use all the CPUs available, you can limit it specifing the actual number of CPUs to use `GDAL_NUM_THREADS=5`

### COG

```bash
gdal_translate $DATASET $DATASET.cog -co NUM_THREADS=ALL_CPUS -co TILING_SCHEME=GoogleMapsCompatible -of COG
```

COG files must append the `.cog` extension to the original file name, **this is not a standard, but the script expects this convention**.


### PMTiles
```bash
export GDAL_NUM_THREADS=ALL_CPUS
ogr2ogr -of PMTiles $DATASET.pmtiles $DATASET -dsco MAXZOOM=$MAXZOOM -dsco MINZOOM=$MINZOOM
```

PMTiles files must append the `.pmtiles` extension to the original file name, **this is not a standard, but the script expects this convention**.
