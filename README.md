

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


## Notes
Client is generated from the OpenAPI Spec served at `/api/v1/docs` using [Python OpenAPI generator](https://github.com/openapi-generators/openapi-python-client).
The generator produces a client that uses `Bearer` prefix, while DRF Auth token uses `Token` as a prefix.
