import logging
import pathlib

import click
import environ
from nina_catalogue_client import AuthenticatedClient
from upload import check_map

env = environ.Env()
BASE_DIR = pathlib.Path(__file__).parent.parent
environ.Env.read_env(str(BASE_DIR / ".env"))

DEBUG = env.bool("DEBUG", default=False)

logging.basicConfig(level=(logging.DEBUG if DEBUG else logging.INFO))


@click.command()
@click.argument("url")
@click.argument("map_slug")
def start(url: str, map_slug: str) -> None:
    TOKEN = env("AUTH_TOKEN")
    logging.debug(f"using TOKEN: {TOKEN}")
    client = AuthenticatedClient(base_url=url, token=TOKEN, verify_ssl=False)
    check_map(client, map_slug)


if __name__ == "__main__":
    start()
