import enum
import logging
import pathlib
import re
from collections import defaultdict

from httpx import Client, Response


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
) -> str:
    slug = project["projectNumber"]
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
            # TODO: use jinja
            "description": f"""
                <p>{project['projectDescription']}</p>
            """,
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
    if layer["dataType"] == "vector":
        return LayerType.GPKG
    elif layer["dataType"] == "raster" and layer["fileType"] == "GeoTIFF":
        return LayerType.TIF
    elif layer["dataType"] == "raster" and layer["fileType"] == "OGC-WMS":
        return LayerType.WMS

    raise Exception("Layer type not supported!")


PROTOCOL_BY_LAYER_TYPE = defaultdict(
    lambda x: "",
    {
        LayerType.GPKG: lambda x: "pmtiles://",
        # LayerType.TIF: lambda x: f'TITILER_ADDRESS/', # TODO: handle titiler
    },
)


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
    },
)


def create_layer(
    client: Client,
    map_slug: str,
    layer: dict,
    project: str,
    slug: str,
    style: dict,
) -> None:
    category = layer["categoryEcosystemAccounting"].replace(" ", "_").replace(".", "")
    category_slug = f"{project}_{category}"

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

    result = re.search(r"(.*)\((.*)\)", layer["datasetAlias"])
    source_slug = f"{project}_{layer['fileName'].replace('.', '_')}"

    json_data = {
        "name": layer["fileName"],
        "slug": source_slug,
        "attribution": layer["datasetOwner"],
        "metadata": layer,
    }

    if layer_type == LayerType.GPKG:
        json_data["protocol"] = "pmtiles://"
    elif layer_type == LayerType.TIF:
        # TODO: handle titiler protocol generation
        json_data["protocol"] = ""
    # TODO: handle WMS

    res = upsert(
        client,
        source_type,
        source_slug,
        json=json_data,
    )
    res.raise_for_status()
    logging.debug(f"Created Source: {res.json()}")

    if layer["fileSkip"] == 0:
        filename = layer["fileName"]
        extension = EXTENSION_BY_LAYER_TYPE[layer_type](layer)

        res = client.post(
            f"{source_type}/{source_slug}/upload/",
            data={
                "field": "original_data",
            },
            files={
                # TODO: read actual file from fs
                "file": pathlib.Path(filename).open(mode="rb"),
            },
            timeout=60.0,
        )

        logging.debug(f"Uploaded Source original data: {res.text}")
        res.raise_for_status()

        res = client.post(
            f"{source_type}/{source_slug}/upload/",
            data={
                "field": "source",
            },
            files={
                # TODO: read actual file from fs
                "file": pathlib.Path(f"{filename}{extension}").open(mode="rb"),
            },
            timeout=60.0,
        )

        logging.debug(f"Uploaded Source display data: {res.text}")
        res.raise_for_status()

    json_data = {
        "map": map_slug,
        "name": result.group(1),
        "slug": slug,
        "group": category_slug,
        "source": source_slug,
        "lazy": True,
        "hidden": True,
        "downloadable": True,
        # TODO: jinja
        "description": f"""
            <p>{layer['datasetDescription']}</p>
            <p>Author: {layer['datasetManager']}</p>
            """,
    }

    if layer_type == LayerType.GPKG:
        json_data["source_layer"] = layer["datasetName"]
        json_data["style"] = style["vector_style"]

    res = upsert(
        client,
        "layers",
        slug,
        parent_resource="maps",
        parent_slug=map_slug,
        json=json_data,
    )
    logging.debug(res.text)
