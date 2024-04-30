import logging
import re

import backoff
from httpx import Client, HTTPError, Response


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
    res = client.post(
        "layer-groups/",
        json={
            "name": project["projectTitle"],
            "map": map_slug,
            "order": 0,
            "parent": None,
            "slug": slug,
        },
    )
    res.raise_for_status()
    logging.debug(f"Created Group: {res.json()}")
    return slug


def create_layer(
    client: Client,
    map_slug: str,
    layer: dict,
    project: str,
) -> None:
    category = layer["categoryEcosystemAccounting"].replace(" ", "_").replace(".", "")
    category_slug = f"{project}_{category}"

    @backoff.on_exception(
        backoff.expo,
        HTTPError,
        giveup=lambda e: 400 <= e.response.status_code < 500,
    )
    def post_layergroup() -> Response:
        res = client.get(f"layer-groups/{category_slug}/")
        if res.status_code < 400:
            return res

        res = client.post(
            "layer-groups/",
            json={
                "name": layer["kategoriNaturregnskap"],
                "order": 0,
                "parent": project,
                "slug": category_slug,
            },
        )
        res.raise_for_status()
        return res

    logging.debug("First, create the category")

    res = post_layergroup()
    logging.debug(f"Created Category: {res.json()}")

    source_type = f"{layer['dataType']}-sources"

    result = re.search(r"(.*)\((.*)\)", layer["datasetAlias"])
    source_slug = f"{project}_{layer['datasetName']}"
    res = upsert(
        client,
        source_type,
        source_slug,
        json={
            "name": result.group(1),
            "slug": source_slug,
            "attribution": layer["datasetOwner"],
            "metadata": layer,
        },
    )
    res.raise_for_status()
    logging.debug(f"Created Source: {res.json()}")

    res = upsert(
        client,
        "layers",
        source_slug,
        parent_resource="maps",
        parent_slug=map_slug,
        json={
            "map": map_slug,
            "name": result.group(1),
            "slug": source_slug,
            "group": category_slug,
            "source": source_slug,
            "lazy": True,
            "hidden": True,
            "downloadable": True,
        },
    )
    logging.debug(res.text)
