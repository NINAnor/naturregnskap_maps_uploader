import time

from httpx import Client, Limits


# add some wait time not to overwhelm the rest API server
def wait(*args, **kwargs) -> None:
    time.sleep(0.5)


def get_client(base_url: str, token: str) -> Client:
    headers = {
        "Authorization": f"Token {token}",
    }
    limits = Limits(max_keepalive_connections=0, max_connections=1)
    client = Client(
        headers=headers,
        base_url=base_url + "/api/v1/",
        limits=limits,
        event_hooks={"request": [wait]},
    )
    return client
