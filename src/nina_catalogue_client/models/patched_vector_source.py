from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedVectorSource")


@_attrs_define
class PatchedVectorSource:
    """
    Attributes:
        name (Union[Unset, str]):
        slug (Union[None, Unset, str]):
        extra (Union[Unset, Any]):
        style (Union[Unset, Any]):
        url (Union[None, Unset, str]):
        attribution (Union[None, Unset, str]):
        protocol (Union[None, Unset, str]):
        source (Union[None, Unset, str]):
        original_data (Union[None, Unset, str]):
        default_layer (Union[None, Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    slug: Union[None, Unset, str] = UNSET
    extra: Union[Unset, Any] = UNSET
    style: Union[Unset, Any] = UNSET
    url: Union[None, Unset, str] = UNSET
    attribution: Union[None, Unset, str] = UNSET
    protocol: Union[None, Unset, str] = UNSET
    source: Union[None, Unset, str] = UNSET
    original_data: Union[None, Unset, str] = UNSET
    default_layer: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        slug: Union[None, Unset, str]
        if isinstance(self.slug, Unset):
            slug = UNSET
        else:
            slug = self.slug

        extra = self.extra

        style = self.style

        url: Union[None, Unset, str]
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        attribution: Union[None, Unset, str]
        if isinstance(self.attribution, Unset):
            attribution = UNSET
        else:
            attribution = self.attribution

        protocol: Union[None, Unset, str]
        if isinstance(self.protocol, Unset):
            protocol = UNSET
        else:
            protocol = self.protocol

        source: Union[None, Unset, str]
        if isinstance(self.source, Unset):
            source = UNSET
        else:
            source = self.source

        original_data: Union[None, Unset, str]
        if isinstance(self.original_data, Unset):
            original_data = UNSET
        else:
            original_data = self.original_data

        default_layer: Union[None, Unset, str]
        if isinstance(self.default_layer, Unset):
            default_layer = UNSET
        else:
            default_layer = self.default_layer

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if slug is not UNSET:
            field_dict["slug"] = slug
        if extra is not UNSET:
            field_dict["extra"] = extra
        if style is not UNSET:
            field_dict["style"] = style
        if url is not UNSET:
            field_dict["url"] = url
        if attribution is not UNSET:
            field_dict["attribution"] = attribution
        if protocol is not UNSET:
            field_dict["protocol"] = protocol
        if source is not UNSET:
            field_dict["source"] = source
        if original_data is not UNSET:
            field_dict["original_data"] = original_data
        if default_layer is not UNSET:
            field_dict["default_layer"] = default_layer

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        name = self.name if isinstance(self.name, Unset) else (None, str(self.name).encode(), "text/plain")

        slug: Union[None, Unset, str]
        if isinstance(self.slug, Unset):
            slug = UNSET
        else:
            slug = self.slug

        extra = self.extra if isinstance(self.extra, Unset) else (None, str(self.extra).encode(), "text/plain")

        style = self.style if isinstance(self.style, Unset) else (None, str(self.style).encode(), "text/plain")

        url: Union[None, Unset, str]
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        attribution: Union[None, Unset, str]
        if isinstance(self.attribution, Unset):
            attribution = UNSET
        else:
            attribution = self.attribution

        protocol: Union[None, Unset, str]
        if isinstance(self.protocol, Unset):
            protocol = UNSET
        else:
            protocol = self.protocol

        source: Union[None, Unset, str]
        if isinstance(self.source, Unset):
            source = UNSET
        else:
            source = self.source

        original_data: Union[None, Unset, str]
        if isinstance(self.original_data, Unset):
            original_data = UNSET
        else:
            original_data = self.original_data

        default_layer: Union[None, Unset, str]
        if isinstance(self.default_layer, Unset):
            default_layer = UNSET
        else:
            default_layer = self.default_layer

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {key: (None, str(value).encode(), "text/plain") for key, value in self.additional_properties.items()}
        )
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if slug is not UNSET:
            field_dict["slug"] = slug
        if extra is not UNSET:
            field_dict["extra"] = extra
        if style is not UNSET:
            field_dict["style"] = style
        if url is not UNSET:
            field_dict["url"] = url
        if attribution is not UNSET:
            field_dict["attribution"] = attribution
        if protocol is not UNSET:
            field_dict["protocol"] = protocol
        if source is not UNSET:
            field_dict["source"] = source
        if original_data is not UNSET:
            field_dict["original_data"] = original_data
        if default_layer is not UNSET:
            field_dict["default_layer"] = default_layer

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        def _parse_slug(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        slug = _parse_slug(d.pop("slug", UNSET))

        extra = d.pop("extra", UNSET)

        style = d.pop("style", UNSET)

        def _parse_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        url = _parse_url(d.pop("url", UNSET))

        def _parse_attribution(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        attribution = _parse_attribution(d.pop("attribution", UNSET))

        def _parse_protocol(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        protocol = _parse_protocol(d.pop("protocol", UNSET))

        def _parse_source(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        source = _parse_source(d.pop("source", UNSET))

        def _parse_original_data(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        original_data = _parse_original_data(d.pop("original_data", UNSET))

        def _parse_default_layer(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        default_layer = _parse_default_layer(d.pop("default_layer", UNSET))

        patched_vector_source = cls(
            name=name,
            slug=slug,
            extra=extra,
            style=style,
            url=url,
            attribution=attribution,
            protocol=protocol,
            source=source,
            original_data=original_data,
            default_layer=default_layer,
        )

        patched_vector_source.additional_properties = d
        return patched_vector_source

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
