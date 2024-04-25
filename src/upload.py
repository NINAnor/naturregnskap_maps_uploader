import logging

from nina_catalogue_client import AuthenticatedClient
from nina_catalogue_client.api.maps import maps_retrieve
from nina_catalogue_client.models import Map


def check_map(client: AuthenticatedClient, map_slug: str) -> None:
    with client as client:
        map_instance: Map = maps_retrieve.sync(
            client=client,
            slug=map_slug,
        )
        logging.debug(f"Retrieved Map: {map_instance.to_dict()}")
