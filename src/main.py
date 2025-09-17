import json
import logging
import pathlib
import re
from typing import Any

import click
from openpyxl import load_workbook

from config import template_env


def str_to_snake_case(text: str) -> str:
    """
    Convert to snake_case.
    - Header One -> header_one
    - HeaderTwo -> header_two
    - headerTwo -> header_two
    - HEADER -> header
    - EPSG Code -> epsg_code
    - someURLValue -> some_url_value
    """
    text = text.strip()
    #  uppercase (>2 letters) converted to lowercase
    text = re.sub(r"\b[A-Z]{2,}\b", lambda m: m.group(0).lower(), text)
    # to snake_case
    text = re.sub(r"(?<!^)(?<![A-Z])(?=[A-Z])", "_", text).replace(" ", "_").lower()
    return text


def load_workbook_sheet(
    wb,
    sheet_name: str,
    skip_first_row: bool = True,
) -> tuple[Any, list[str] | None]:
    sheet = wb[sheet_name]
    rows = sheet.iter_rows()

    # first row is header
    if skip_first_row:
        next(rows)
        header = [cell.value.strip() for cell in next(rows) if cell.value]
        return rows, header

    # first row is data, header is None
    return rows, None


@click.command()
@click.option("--schema", default="schema.xlsx", type=click.Path())
@click.option(
    "--wd",
    default=".",
    type=click.Path(dir_okay=True, exists=True, readable=True, path_type=pathlib.Path),
)
def start(schema: str, wd: pathlib.Path) -> None:
    schema_path = wd / schema

    wb = load_workbook(str(schema_path))

    # Load layer group metadata (projectMetadata)
    rows, header = load_workbook_sheet(wb, "projectMetadata", True)
    project_metadata = {}
    for row in rows:
        row = [
            cell.value.strip() if isinstance(cell.value, str) else cell.value
            for cell in row
        ]
        if not any(row):
            continue
        project_metadata = dict(zip(header, row, strict=True))

        break

    logging.debug("found_project %s" % project_metadata)

    # Load project contacts
    project_metadata["contacts"] = []
    rows, header = load_workbook_sheet(wb, "projectContacts", True)
    for row in rows:
        row = [
            cell.value.strip() if isinstance(cell.value, str) else cell.value
            for cell in row
        ]
        if not any(row):
            continue
        project_metadata["contacts"].append(dict(zip(header, row, strict=True)))

    logging.info("project_metadata %s" % project_metadata)

    # Load layer metadata (datasetMetadata) into nested dict
    # lyr_metadata = {h1: {h2: value}}
    # h1 = first row, filled with previous value if empty
    # h2 = second row, should not contain empty values
    rows, header = load_workbook_sheet(wb, "datasetMetadata", False)
    h1, last_value = [], None
    h1 = [
        (last_value := str_to_snake_case(cell.value) if cell.value else last_value)
        for cell in next(rows)
    ]
    h2 = [cell.value.strip() for cell in next(rows) if cell.value]
    h2_snake_case = list(map(str_to_snake_case, h2))

    map_json = {
        "id": "localEA",
        "title": "Kartportal for Finskala Naturregnskap",
        "subtitle": "Local Ecosystem Accounts",
        "description": "",
        "icon": "https://maps.nina.no/assets/logosmall-BFfoJdyr.png",
        "baseMap": "positron",
        "layerOrder": [],
        "viewState": {
            "longitude": 17.8,
            "latitude": 65.6,
            "zoom": 4,
        },
        "expandedItems": [],
        "items": {
            "root": {
                "name": "Layers",
                "type": "folder",
                "children": [
                    project_metadata["projectID"],
                ],
            },
            project_metadata["projectID"]: {
                "name": project_metadata["projectTitle"],
                "type": "folder",
                "description": template_env.get_template(
                    "project_description.md",
                )
                .render(
                    project=project_metadata,
                )
                .strip(),
                "children": [],
            },
        },
        "config": {
            "titiler_api_url": "/titiler",
            "theme": "nina",
            "language": "no",
            "footer": {
                "items": [
                    "![](https://maps.nina.no/assets/logowhite-6HSLYLYZ.png)",
                    "Norsk institutt for naturforskning - [www.nina.no](https://www.nina.no)",
                ],
                "justify": "justify-between",
                "align": "items-baseline",
            },
        },
    }

    lyr_metadata = {h1[0]: {}}
    for row in rows:
        row = [
            cell.value.strip() if isinstance(cell.value, str) else cell.value
            for cell in row
        ]
        if not any(row):
            continue
        dataset_metadata = dict(zip(h2, row, strict=True))
        dataset_metadata = {
            k: (v if v is not None else "") for k, v in dataset_metadata.items()
        }
        for h1_key, h2_key, value in zip(h1, h2_snake_case, row, strict=False):
            if h1_key not in lyr_metadata:
                lyr_metadata[h1_key] = {}
            lyr_metadata[h1_key][h2_key] = value if value is not None else ""

        if dataset_metadata["categoryEcosystemAccounting"] not in map_json["items"]:
            map_json["items"][dataset_metadata["categoryEcosystemAccounting"]] = {
                "type": "folder",
                "name": dataset_metadata["kategoriNaturregnskap"],
                "children": [],
            }

            map_json["items"][project_metadata["projectID"]]["children"].append(
                dataset_metadata["categoryEcosystemAccounting"],
            )

        category = map_json["items"][dataset_metadata["categoryEcosystemAccounting"]]

        item = {
            "name": dataset_metadata["datasetAlias"],
            "type": "layer",
            "description": template_env.get_template("layer_description.md")
            .render(
                lyr_metadata=lyr_metadata,
                project=project_metadata,
            )
            .strip(),
            "layer": {
                "type": "raster",
            },
        }

        map_json["items"][dataset_metadata["datasetName"]] = item

        category["children"].append(
            dataset_metadata["datasetName"],
        )

    print(json.dumps(map_json))


if __name__ == "__main__":
    start()
