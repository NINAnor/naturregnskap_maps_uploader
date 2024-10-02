import logging
import pathlib

import environ
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = environ.Env()
BASE_DIR = pathlib.Path(__file__).parent.parent
environ.Env.read_env(str(BASE_DIR / ".env"))

DEBUG = env.bool("DEBUG", default=False)
SKIP_SOURCE_FILES = env.bool("SKIP_SOURCE_FILES", default=False)

TITILER_URL = env("TITILER_URL")
TOKEN = env("AUTH_TOKEN")

logging.basicConfig(level=(logging.DEBUG if DEBUG else logging.INFO))


template_env = Environment(
    loader=FileSystemLoader(pathlib.Path(__file__).parent / "templates"),
    autoescape=select_autoescape(),
)
