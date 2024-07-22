import enum
import json
import logging
import pathlib
import re
from collections import defaultdict

import fiona
from httpx import Client, Response
from jinja2 import Environment


def upsert(
    client: Client,
    resource: str,
    slug: str,
    parent_resource: str = None,
    parent_slug: str = None,
    **kwargs,
) -> Response:
    url = f"{resource}/{slug}/"
    if parent_resource:
        url = f"{parent_resource}/{parent_slug}/" + url

    r = client.get(url)
    if r.status_code == 404:
        url = f"{resource}/"
        if parent_resource:
            url = f"{parent_resource}/{parent_slug}/" + url

        return client.post(
            url,
            **kwargs,
        )
    elif r.status_code == 200:
        return client.patch(
            url,
            **kwargs,
        )
    else:
        r.raise_for_status()


def check_map(client: Client, map_slug: str) -> None:
    # with client as client:
    res = client.get(f"maps/{map_slug}/")
    logging.debug(f"Retrieved Map: {res.json()}")


def create_project_folder(
    client: Client,
    map_slug: str,
    project: dict,
    template_env: Environment,
) -> str:
    slug = project["projectNumber"]
    template = template_env.get_template("project_description.html")
    res = upsert(
        client,
        "layer-groups",
        slug=slug,
        json={
            "name": project["projectTitle"],
            "map": map_slug,
            "order": 0,
            "parent": None,
            "slug": slug,
            "description": template.render(project=project),
        },
    )
    res.raise_for_status()
    logging.debug(f"Created Group: {res.json()}")
    return slug


class LayerType(enum.Enum):
    TIF = 1
    GPKG = 2
    WMS = 3


def get_layer_type(layer: dict) -> LayerType:
    if layer["fileType"] == "OGC-WMS":
        return LayerType.WMS
    if layer["dataType"] == "vector":
        return LayerType.GPKG
    elif layer["dataType"] == "raster" and layer["fileType"] == "GeoTIFF":
        return LayerType.TIF

    logging.debug(f"Layer type not supported: {layer}")
    raise Exception("Layer type not supported!")


EXTENSION_BY_LAYER_TYPE = defaultdict(
    lambda x: "",
    {
        LayerType.GPKG: lambda x: ".pmtiles",
        LayerType.TIF: lambda x: ".cog",
    },
)

SOURCE_BY_LAYER_TYPE = defaultdict(
    lambda x: "sources",
    {
        LayerType.GPKG: lambda x: "vector-sources",
        LayerType.TIF: lambda x: "raster-sources",
        LayerType.WMS: lambda x: "sources",
    },
)


def create_layer(
    client: Client,
    map_slug: str,
    layer: dict,
    project: str,
    slug: str,
    style: dict,
    wd: pathlib.Path,
    titiler_config: dict,
    template_env: Environment,
    lyr_metadata: dict,
    project_metdata: dict,
) -> None:
    
    category = layer["categoryEcosystemAccounting"].replace(" ", "_").replace(".", "")
    category_slug = f"{project}_{category}"

    # Metadata dictionaries
    data_description = lyr_metadata["data_description"]
    citation = lyr_metadata["citation"]
    temporal_scope = lyr_metadata["temporal_scope"]
    geographic_scope = lyr_metadata["geographic_scope"]
    taxonomic_scope = lyr_metadata["taxonomic_scope"]
    methodology = lyr_metadata["methodology"]

    template = template_env.get_template("layer_description.html")
    layer_type = get_layer_type(layer)

    logging.debug("First, create the category")
    res = upsert(
        client,
        "layer-groups",
        category_slug,
        json={
            "name": layer["kategoriNaturregnskap"],
            "order": 0,
            "parent": project,
            "slug": category_slug,
        },
    )

    logging.debug(f"Created Category: {res.json()}")

    source_type = SOURCE_BY_LAYER_TYPE[layer_type](layer)

    source_slug = ""
    source_name = ""

    if layer_type == LayerType.GPKG:
        source_slug = f"{project}_{layer['datasetName'].replace('.', '_')}"
        source_name = layer["datasetName"]
    else:
        source_slug = f"{project}_{layer['datasetName'].replace('.', '_')}"
        source_name = layer["datasetName"]

    json_data = {
        "name": source_name,
        "slug": source_slug,
        "attribution": layer["datasetOwner"],
        "metadata": layer,
    }

    if layer_type == LayerType.GPKG:
        json_data["protocol"] = "pmtiles://"
    elif layer_type == LayerType.TIF:
        style["raster_style"]

        params = []
        for key, value in style["raster_style"].items():
            if isinstance(value, list):
                for e in value:
                    params.append(f"{key}={e}")
            elif isinstance(value, dict):
                params.append(f"{key}={json.dumps(value)}")
            else:
                params.append(f"{key}={value}")

        json_data["protocol"] = (
            f"{titiler_config['url']}/cog/tilejson.json?{'&'.join(params)}&url="
        )
    elif layer_type == LayerType.WMS:
        json_data["extra"] = {
            "type": "raster",
            "tileSize": 256,
            "tiles": [
                layer["fileName"]
                + "&bbox={bbox-epsg-3857}&format=image/png&service=WMS&version=1.1.1&request=GetMap&srs=EPSG:3857&transparent=true&width=256&height=256",
            ],
        }

    res = upsert(
        client,
        source_type,
        source_slug,
        json=json_data,
    )
    res.raise_for_status()
    logging.debug(f"Created Source: {res.json()}")

    if layer["fileSkip"] == 0 and layer_type != LayerType.WMS:
        filename = layer["fileName"]
        extension = EXTENSION_BY_LAYER_TYPE[layer_type](layer)

        source_file = wd / filename

        if layer_type == LayerType.GPKG:
            with fiona.open(source_file, layer=layer["datasetName"], mode="r") as src:
                profile = src.profile
                profile["driver"] = "GPKG"

                layer_source_file = wd / f"{layer['datasetName']}.gpkg"
                if not layer_source_file.exists():
                    logging.info(
                        f"{str(layer_source_file)} not found, it will be extracted with fiona",
                    )
                    # NOTE: the datasets does not work with P://, it will produce a transaction error
                    with fiona.open(
                        layer_source_file,
                        mode="w",
                        layer=layer["datasetName"],
                        **profile,
                    ) as dst:
                        dst.writerecords(src)

            source_file = layer_source_file

        if source_file.exists():
            res = client.post(
                f"{source_type}/{source_slug}/upload/",
                data={
                    "field": "original_data",
                },
                files={
                    "file": source_file.open(mode="rb"),
                },
                timeout=60.0,
            )

            logging.debug(f"Uploaded Source original data: {res.text}")
            res.raise_for_status()
        else:
            logging.warn(f"Source original file not found: {str(source_file)}")

        file = wd / f"{filename}{extension}"
        if (wd / filename).exists():
            res = client.post(
                f"{source_type}/{source_slug}/upload/",
                data={
                    "field": "source",
                },
                files={
                    "file": file.open(mode="rb"),
                },
                timeout=60.0,
            )

            logging.debug(f"Uploaded Source display data: {res.text}")
            res.raise_for_status()
        else:
            logging.warn(f"Source display file not found: {str(file)}")

    json_data = {
        "map": map_slug,
        "name": layer["datasetAlias"],
        "slug": slug,
        "group": category_slug,
        "source": source_slug,
        "lazy": True,
        "hidden": True,
        "downloadable": layer_type != LayerType.WMS,
        "legend": style["legend"] if "legend" in style else {},
        "description": template.render(
            data_description = data_description,
            citation = citation,
            temporal_scope = temporal_scope,
            geographic_scope = geographic_scope,
            taxonomic_scope = taxonomic_scope,
            methodology = methodology,
            project=project_metdata,
            ),
    }

    if layer_type == LayerType.GPKG:
        json_data["source_layer"] = layer["datasetName"]
        json_data["style"] = style["vector_style"]

    if layer_type == LayerType.WMS:
        json_data["style"] = {
            "type": "raster",
            "paint": {},
        }

    res = upsert(
        client,
        "layers",
        slug,
        parent_resource="maps",
        parent_slug=map_slug,
        json=json_data,
    )
    logging.debug(res.text)