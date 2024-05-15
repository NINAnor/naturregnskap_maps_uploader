import logging
import pathlib

import click
import environ
from api import get_client
from openpyxl import load_workbook
from upload import check_map, create_layer, create_project_folder
from yaml import safe_load

env = environ.Env()
BASE_DIR = pathlib.Path(__file__).parent.parent
environ.Env.read_env(str(BASE_DIR / ".env"))

DEBUG = env.bool("DEBUG", default=False)

logging.basicConfig(level=(logging.DEBUG if DEBUG else logging.INFO))


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
    with style_path.open("r") as style_file:
        style_index = safe_load(style_file)["datasets"]

    wb = load_workbook(str(schema_path))
    project_sheet = wb["projectMetadata"]
    rows = project_sheet.iter_rows()
    # always skip first row
    next(rows)
    header = [cell.value.strip() for cell in next(rows) if cell.value]
    for row in rows:
        row = [cell.value for cell in row]
        if not any(row):
            continue
        project_metadata = dict(zip(header, row, strict=True))

        break

    logging.debug("found_project %s" % project_metadata)

    TOKEN = env("AUTH_TOKEN")
    logging.debug(f"using TOKEN: {TOKEN}")
    client = get_client(base_url=url, token=TOKEN)
    check_map(client, map_slug)
    project_slug = create_project_folder(client, map_slug, project_metadata)

    dataset_sheet = wb["datasetMetadata"]
    rows = dataset_sheet.iter_rows()
    # always skip first row
    next(rows)
    header = [cell.value.strip() for cell in next(rows) if cell.value]
    for row in rows:
        row = [cell.value for cell in row]
        if not any(row):
            continue
        dataset_metadata = dict(zip(header, row, strict=True))

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
            )


if __name__ == "__main__":
    start()
