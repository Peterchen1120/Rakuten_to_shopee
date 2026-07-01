from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class SourceProduct:
    source: str
    source_id: str
    source_url: str
    title: str
    price_jpy: int | None
    image_urls: list[str] = field(default_factory=list)
    description: str = ""
    stock: int | None = 1
    category_hint: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ListingPreview:
    title: str
    description: str
    price_twd: int
    price_jpy: int | None
    image_urls: list[str]
    source: str
    source_id: str
    source_url: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
