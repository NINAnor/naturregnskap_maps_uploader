from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.patched_vector_source import PatchedVectorSource
from ...models.vector_source import VectorSource
from ...types import Response


def _get_kwargs(
    slug: str,
    *,
    body: Union[
        PatchedVectorSource,
        PatchedVectorSource,
        PatchedVectorSource,
    ],
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/api/v1/vector-sources/{slug}/",
    }

    if isinstance(body, PatchedVectorSource):
        _json_body = body.to_dict()

        _kwargs["json"] = _json_body
        headers["Content-Type"] = "application/json"
    if isinstance(body, PatchedVectorSource):
        _data_body = body.to_dict()

        _kwargs["data"] = _data_body
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, PatchedVectorSource):
        _files_body = body.to_multipart()

        _kwargs["files"] = _files_body
        headers["Content-Type"] = "multipart/form-data"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[VectorSource]:
    if response.status_code == HTTPStatus.OK:
        response_200 = VectorSource.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[VectorSource]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    slug: str,
    *,
    client: AuthenticatedClient,
    body: Union[
        PatchedVectorSource,
        PatchedVectorSource,
        PatchedVectorSource,
    ],
) -> Response[VectorSource]:
    """
    Args:
        slug (str):
        body (PatchedVectorSource):
        body (PatchedVectorSource):
        body (PatchedVectorSource):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VectorSource]
    """

    kwargs = _get_kwargs(
        slug=slug,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    slug: str,
    *,
    client: AuthenticatedClient,
    body: Union[
        PatchedVectorSource,
        PatchedVectorSource,
        PatchedVectorSource,
    ],
) -> Optional[VectorSource]:
    """
    Args:
        slug (str):
        body (PatchedVectorSource):
        body (PatchedVectorSource):
        body (PatchedVectorSource):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VectorSource
    """

    return sync_detailed(
        slug=slug,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    slug: str,
    *,
    client: AuthenticatedClient,
    body: Union[
        PatchedVectorSource,
        PatchedVectorSource,
        PatchedVectorSource,
    ],
) -> Response[VectorSource]:
    """
    Args:
        slug (str):
        body (PatchedVectorSource):
        body (PatchedVectorSource):
        body (PatchedVectorSource):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VectorSource]
    """

    kwargs = _get_kwargs(
        slug=slug,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    slug: str,
    *,
    client: AuthenticatedClient,
    body: Union[
        PatchedVectorSource,
        PatchedVectorSource,
        PatchedVectorSource,
    ],
) -> Optional[VectorSource]:
    """
    Args:
        slug (str):
        body (PatchedVectorSource):
        body (PatchedVectorSource):
        body (PatchedVectorSource):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VectorSource
    """

    return (
        await asyncio_detailed(
            slug=slug,
            client=client,
            body=body,
        )
    ).parsed
