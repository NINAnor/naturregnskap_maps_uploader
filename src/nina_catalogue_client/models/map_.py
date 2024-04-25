from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.visibility_enum import VisibilityEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="Map")


@_attrs_define
class Map:
    """
    Attributes:
        id (int):
        title (str):
        slug (Union[None, Unset, str]):
        subtitle (Union[None, Unset, str]):
        zoom (Union[None, Unset, int]):
        description (Union[Unset, str]):
        visibility (Union[Unset, VisibilityEnum]): * `public` - Public
            * `private` - Private
        config (Union[Unset, Any]):
        legend_config (Union[Unset, Any]):
        basemap_config (Union[Unset, Any]):
    """

    id: int
    title: str
    slug: Union[None, Unset, str] = UNSET
    subtitle: Union[None, Unset, str] = UNSET
    zoom: Union[None, Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    visibility: Union[Unset, VisibilityEnum] = UNSET
    config: Union[Unset, Any] = UNSET
    legend_config: Union[Unset, Any] = UNSET
    basemap_config: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        title = self.title

        slug: Union[None, Unset, str]
        if isinstance(self.slug, Unset):
            slug = UNSET
        else:
            slug = self.slug

        subtitle: Union[None, Unset, str]
        if isinstance(self.subtitle, Unset):
            subtitle = UNSET
        else:
            subtitle = self.subtitle

        zoom: Union[None, Unset, int]
        if isinstance(self.zoom, Unset):
            zoom = UNSET
        else:
            zoom = self.zoom

        description = self.description

        visibility: Union[Unset, str] = UNSET
        if not isinstance(self.visibility, Unset):
            visibility = self.visibility.value

        config = self.config

        legend_config = self.legend_config

        basemap_config = self.basemap_config

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "title": title,
            }
        )
        if slug is not UNSET:
            field_dict["slug"] = slug
        if subtitle is not UNSET:
            field_dict["subtitle"] = subtitle
        if zoom is not UNSET:
            field_dict["zoom"] = zoom
        if description is not UNSET:
            field_dict["description"] = description
        if visibility is not UNSET:
            field_dict["visibility"] = visibility
        if config is not UNSET:
            field_dict["config"] = config
        if legend_config is not UNSET:
            field_dict["legend_config"] = legend_config
        if basemap_config is not UNSET:
            field_dict["basemap_config"] = basemap_config

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        id = self.id if isinstance(self.id, Unset) else (None, str(self.id).encode(), "text/plain")

        title = self.title if isinstance(self.title, Unset) else (None, str(self.title).encode(), "text/plain")

        slug: Union[None, Unset, str]
        if isinstance(self.slug, Unset):
            slug = UNSET
        else:
            slug = self.slug

        subtitle: Union[None, Unset, str]
        if isinstance(self.subtitle, Unset):
            subtitle = UNSET
        else:
            subtitle = self.subtitle

        zoom: Union[None, Unset, int]
        if isinstance(self.zoom, Unset):
            zoom = UNSET
        else:
            zoom = self.zoom

        description = (
            self.description
            if isinstance(self.description, Unset)
            else (None, str(self.description).encode(), "text/plain")
        )

        visibility: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.visibility, Unset):
            visibility = (None, str(self.visibility.value).encode(), "text/plain")

        config = self.config if isinstance(self.config, Unset) else (None, str(self.config).encode(), "text/plain")

        legend_config = (
            self.legend_config
            if isinstance(self.legend_config, Unset)
            else (None, str(self.legend_config).encode(), "text/plain")
        )

        basemap_config = (
            self.basemap_config
            if isinstance(self.basemap_config, Unset)
            else (None, str(self.basemap_config).encode(), "text/plain")
        )

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {key: (None, str(value).encode(), "text/plain") for key, value in self.additional_properties.items()}
        )
        field_dict.update(
            {
                "id": id,
                "title": title,
            }
        )
        if slug is not UNSET:
            field_dict["slug"] = slug
        if subtitle is not UNSET:
            field_dict["subtitle"] = subtitle
        if zoom is not UNSET:
            field_dict["zoom"] = zoom
        if description is not UNSET:
            field_dict["description"] = description
        if visibility is not UNSET:
            field_dict["visibility"] = visibility
        if config is not UNSET:
            field_dict["config"] = config
        if legend_config is not UNSET:
            field_dict["legend_config"] = legend_config
        if basemap_config is not UNSET:
            field_dict["basemap_config"] = basemap_config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        title = d.pop("title")

        def _parse_slug(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        slug = _parse_slug(d.pop("slug", UNSET))

        def _parse_subtitle(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        subtitle = _parse_subtitle(d.pop("subtitle", UNSET))

        def _parse_zoom(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        zoom = _parse_zoom(d.pop("zoom", UNSET))

        description = d.pop("description", UNSET)

        _visibility = d.pop("visibility", UNSET)
        visibility: Union[Unset, VisibilityEnum]
        if isinstance(_visibility, Unset):
            visibility = UNSET
        else:
            visibility = VisibilityEnum(_visibility)

        config = d.pop("config", UNSET)

        legend_config = d.pop("legend_config", UNSET)

        basemap_config = d.pop("basemap_config", UNSET)

        map_ = cls(
            id=id,
            title=title,
            slug=slug,
            subtitle=subtitle,
            zoom=zoom,
            description=description,
            visibility=visibility,
            config=config,
            legend_config=legend_config,
            basemap_config=basemap_config,
        )

        map_.additional_properties = d
        return map_

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
