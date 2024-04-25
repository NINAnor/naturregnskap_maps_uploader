from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedLayer")


@_attrs_define
class PatchedLayer:
    """
    Attributes:
        name (Union[None, Unset, str]):
        slug (Union[None, Unset, str]):
        map_ (Union[None, Unset, str]):
        source (Union[None, Unset, str]):
        style (Union[Unset, Any]):
        group (Union[None, Unset, int]):
        group_order (Union[Unset, int]):
        downloadable (Union[Unset, bool]):
        description (Union[None, Unset, str]):
        link (Union[None, Unset, str]):
        legend (Union[Unset, Any]):
        is_basemap (Union[Unset, bool]):
        is_lazy (Union[Unset, bool]):
        hidden (Union[Unset, bool]):
    """

    name: Union[None, Unset, str] = UNSET
    slug: Union[None, Unset, str] = UNSET
    map_: Union[None, Unset, str] = UNSET
    source: Union[None, Unset, str] = UNSET
    style: Union[Unset, Any] = UNSET
    group: Union[None, Unset, int] = UNSET
    group_order: Union[Unset, int] = UNSET
    downloadable: Union[Unset, bool] = UNSET
    description: Union[None, Unset, str] = UNSET
    link: Union[None, Unset, str] = UNSET
    legend: Union[Unset, Any] = UNSET
    is_basemap: Union[Unset, bool] = UNSET
    is_lazy: Union[Unset, bool] = UNSET
    hidden: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        slug: Union[None, Unset, str]
        if isinstance(self.slug, Unset):
            slug = UNSET
        else:
            slug = self.slug

        map_: Union[None, Unset, str]
        if isinstance(self.map_, Unset):
            map_ = UNSET
        else:
            map_ = self.map_

        source: Union[None, Unset, str]
        if isinstance(self.source, Unset):
            source = UNSET
        else:
            source = self.source

        style = self.style

        group: Union[None, Unset, int]
        if isinstance(self.group, Unset):
            group = UNSET
        else:
            group = self.group

        group_order = self.group_order

        downloadable = self.downloadable

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        link: Union[None, Unset, str]
        if isinstance(self.link, Unset):
            link = UNSET
        else:
            link = self.link

        legend = self.legend

        is_basemap = self.is_basemap

        is_lazy = self.is_lazy

        hidden = self.hidden

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if slug is not UNSET:
            field_dict["slug"] = slug
        if map_ is not UNSET:
            field_dict["map"] = map_
        if source is not UNSET:
            field_dict["source"] = source
        if style is not UNSET:
            field_dict["style"] = style
        if group is not UNSET:
            field_dict["group"] = group
        if group_order is not UNSET:
            field_dict["group_order"] = group_order
        if downloadable is not UNSET:
            field_dict["downloadable"] = downloadable
        if description is not UNSET:
            field_dict["description"] = description
        if link is not UNSET:
            field_dict["link"] = link
        if legend is not UNSET:
            field_dict["legend"] = legend
        if is_basemap is not UNSET:
            field_dict["is_basemap"] = is_basemap
        if is_lazy is not UNSET:
            field_dict["is_lazy"] = is_lazy
        if hidden is not UNSET:
            field_dict["hidden"] = hidden

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        slug: Union[None, Unset, str]
        if isinstance(self.slug, Unset):
            slug = UNSET
        else:
            slug = self.slug

        map_: Union[None, Unset, str]
        if isinstance(self.map_, Unset):
            map_ = UNSET
        else:
            map_ = self.map_

        source: Union[None, Unset, str]
        if isinstance(self.source, Unset):
            source = UNSET
        else:
            source = self.source

        style = self.style if isinstance(self.style, Unset) else (None, str(self.style).encode(), "text/plain")

        group: Union[None, Unset, int]
        if isinstance(self.group, Unset):
            group = UNSET
        else:
            group = self.group

        group_order = (
            self.group_order
            if isinstance(self.group_order, Unset)
            else (None, str(self.group_order).encode(), "text/plain")
        )

        downloadable = (
            self.downloadable
            if isinstance(self.downloadable, Unset)
            else (None, str(self.downloadable).encode(), "text/plain")
        )

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        link: Union[None, Unset, str]
        if isinstance(self.link, Unset):
            link = UNSET
        else:
            link = self.link

        legend = self.legend if isinstance(self.legend, Unset) else (None, str(self.legend).encode(), "text/plain")

        is_basemap = (
            self.is_basemap
            if isinstance(self.is_basemap, Unset)
            else (None, str(self.is_basemap).encode(), "text/plain")
        )

        is_lazy = self.is_lazy if isinstance(self.is_lazy, Unset) else (None, str(self.is_lazy).encode(), "text/plain")

        hidden = self.hidden if isinstance(self.hidden, Unset) else (None, str(self.hidden).encode(), "text/plain")

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {key: (None, str(value).encode(), "text/plain") for key, value in self.additional_properties.items()}
        )
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if slug is not UNSET:
            field_dict["slug"] = slug
        if map_ is not UNSET:
            field_dict["map"] = map_
        if source is not UNSET:
            field_dict["source"] = source
        if style is not UNSET:
            field_dict["style"] = style
        if group is not UNSET:
            field_dict["group"] = group
        if group_order is not UNSET:
            field_dict["group_order"] = group_order
        if downloadable is not UNSET:
            field_dict["downloadable"] = downloadable
        if description is not UNSET:
            field_dict["description"] = description
        if link is not UNSET:
            field_dict["link"] = link
        if legend is not UNSET:
            field_dict["legend"] = legend
        if is_basemap is not UNSET:
            field_dict["is_basemap"] = is_basemap
        if is_lazy is not UNSET:
            field_dict["is_lazy"] = is_lazy
        if hidden is not UNSET:
            field_dict["hidden"] = hidden

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_slug(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        slug = _parse_slug(d.pop("slug", UNSET))

        def _parse_map_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        map_ = _parse_map_(d.pop("map", UNSET))

        def _parse_source(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        source = _parse_source(d.pop("source", UNSET))

        style = d.pop("style", UNSET)

        def _parse_group(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        group = _parse_group(d.pop("group", UNSET))

        group_order = d.pop("group_order", UNSET)

        downloadable = d.pop("downloadable", UNSET)

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_link(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        link = _parse_link(d.pop("link", UNSET))

        legend = d.pop("legend", UNSET)

        is_basemap = d.pop("is_basemap", UNSET)

        is_lazy = d.pop("is_lazy", UNSET)

        hidden = d.pop("hidden", UNSET)

        patched_layer = cls(
            name=name,
            slug=slug,
            map_=map_,
            source=source,
            style=style,
            group=group,
            group_order=group_order,
            downloadable=downloadable,
            description=description,
            link=link,
            legend=legend,
            is_basemap=is_basemap,
            is_lazy=is_lazy,
            hidden=hidden,
        )

        patched_layer.additional_properties = d
        return patched_layer

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
