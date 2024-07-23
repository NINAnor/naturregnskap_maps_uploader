import logging
import pathlib

import click
import environ
from api import get_client
from jinja2 import Environment, FileSystemLoader, select_autoescape
from openpyxl import load_workbook
from upload import check_map, create_layer, create_project_folder
from yaml import safe_load

env = environ.Env()
BASE_DIR = pathlib.Path(__file__).parent.parent
environ.Env.read_env(str(BASE_DIR / ".env"))

DEBUG = env.bool("DEBUG", default=False)

logging.basicConfig(level=(logging.DEBUG if DEBUG else logging.INFO))


template_env = Environment(
    loader=FileSystemLoader(pathlib.Path(__file__).parent / "templates"),
    autoescape=select_autoescape(),
)


@click.command()
@click.argument("url")
@click.argument("map_slug")
@click.option("--schema", default="schema.xlsx", type=click.Path())
@click.option("--style", default="style.yml", type=click.Path())
@click.option(
    "--wd",
    default=".",
    type=click.Path(dir_okay=True, exists=True, readable=True, path_type=pathlib.Path),
)
def start(url: str, map_slug: str, schema: str, style: str, wd: pathlib.Path) -> None:
    style_path = wd / style
    schema_path = wd / schema

    style_index = {}
    titiler_config = {}
    with style_path.open("r") as style_file:
        conf = safe_load(style_file)
        style_index = conf["datasets"]
        titiler_config = conf["titiler"]

    wb = load_workbook(str(schema_path))
    project_sheet = wb["projectMetadata"]
    rows = project_sheet.iter_rows()
    # always skip first row
    next(rows)
    header = [cell.value.strip() for cell in next(rows) if cell.value]
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
    project_metadata["contacts"] = []

    contacts_sheet = wb["projectContacts"]
    rows = contacts_sheet.iter_rows()
    # always skip first row
    next(rows)
    header = [cell.value.strip() for cell in next(rows) if cell.value]
    for row in rows:
        row = [
            cell.value.strip() if isinstance(cell.value, str) else cell.value
            for cell in row
        ]
        if not any(row):
            continue

        project_metadata["contacts"].append(dict(zip(header, row, strict=True)))

    TOKEN = env("AUTH_TOKEN")
    logging.debug(f"using TOKEN: {TOKEN}")
    client = get_client(base_url=url, token=TOKEN)
    check_map(client, map_slug)
    project_slug = create_project_folder(
        client,
        map_slug,
        project_metadata,
        template_env,
    )

    # TODO: read and save also project owner and contributors

    dataset_sheet = wb["datasetMetadata"]
    rows = dataset_sheet.iter_rows()

    # header 1 = first row, filled with previous value if empty
    h1, last_value = [], None
    h1 = [
        (last_value := cell.value.strip() if cell.value else last_value)
        for cell in next(rows)
    ]
    # header 2 = second row, should not contain empty values
    h2 = [cell.value.strip() for cell in next(rows) if cell.value]

    display_metadata = {h1[0]: {}}
    logging.info(f"h1: {display_metadata}")

    for row in rows:
        row = [
            cell.value.strip() if isinstance(cell.value, str) else cell.value
            for cell in row
        ]
        if not any(row):
            continue
        # create display_metadata = {h1: {h2: value}}
        dataset_metadata = dict(zip(h2, row, strict=True))
        dataset_metadata = {
            k: (v if v is not None else "") for k, v in dataset_metadata.items()
        }
        # Created nested dict with h1 as key for h2 and value
        for h1_key, h2_key, value in zip(h1, h2, row):
            if h1_key not in display_metadata:
                display_metadata[h1_key] = {}
            if value is not None:
                display_metadata[h1_key][h2_key] = value
            else:
                display_metadata[h1_key][h2_key] = ""

        # rename keys, convert None values to empty string, start each word with lower key
        display_metadata = {k.replace(" ", "_"): v for k, v in display_metadata.items()}
        display_metadata = {
            k[0].lower() + k[1:]: v for k, v in display_metadata.items()
        }

        logging.debug(f"display_metadata: {display_metadata}")
        logging.debug(f'uploading {dataset_metadata["datasetAlias"]}')

        layer_slug = f"{project_slug}_{dataset_metadata['datasetName']}"

        if dataset_metadata["skip"] == 0:
            layer_style = (
                style_index[layer_slug]
                if layer_slug in style_index
                else style_index["DEFAULT"]
            )

            create_layer(
                client=client,
                map_slug=map_slug,
                layer=dataset_metadata,
                project=project_slug,
                slug=layer_slug,
                style=layer_style,
                wd=wd,
                titiler_config=titiler_config,
                template_env=template_env,
                lyr_metadata=display_metadata,
                project_metdata=project_metadata,
            )


if __name__ == "__main__":
    start()
