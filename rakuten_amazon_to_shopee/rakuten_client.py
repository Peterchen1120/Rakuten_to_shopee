from __future__ import annotations

import os

try:
    import requests
except ImportError:  # pragma: no cover - handled at runtime
    requests = None

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - handled at runtime
    def load_dotenv() -> bool:
        return False

from .models import SourceProduct
from .credentials import RakutenCredentials
from .source_router import extract_rakuten_item_code

load_dotenv()

RAKUTEN_ENDPOINT = (
    "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20260401"
)


def clean_rakuten_image_url(url: str) -> str:
    return url.replace("?_ex=128x128", "").replace("?_ex=64x64", "").strip()


def get_rakuten_item_by_url(
    url: str,
    credentials: RakutenCredentials | None = None,
) -> SourceProduct:
    if requests is None:
        raise RuntimeError("requests is required to call the Rakuten API.")

    config = credentials or RakutenCredentials.from_env()
    app_id = config.app_id or os.getenv("RAKUTEN_APP_ID")
    access_key = config.access_key or os.getenv("RAKUTEN_ACCESS_KEY")

    if not app_id or not access_key:
        raise RuntimeError("RAKUTEN_APP_ID and RAKUTEN_ACCESS_KEY must be set.")

    item_code = extract_rakuten_item_code(url)
    params = {
        "applicationId": app_id,
        "accessKey": access_key,
        "format": "json",
        "formatVersion": 2,
        "itemCode": item_code,
        "hits": 1,
        "elements": ",".join(
            [
                "itemName",
                "itemCode",
                "itemUrl",
                "itemPrice",
                "itemCaption",
                "mediumImageUrls",
                "availability",
                "genreId",
                "shopName",
            ]
        ),
    }

    response = requests.get(RAKUTEN_ENDPOINT, params=params, timeout=20)
    response.raise_for_status()

    payload = response.json()
    items = payload.get("items") or payload.get("Items") or []
    if not items:
        raise RuntimeError(f"Rakuten API did not return itemCode={item_code}.")

    # 樂天的商品格式不一
    # 1. [{"itemName": "xxx","price": xxx}]，
    # 2. [{"Item": {"itemName": "xxx", "price": xxx}}]
    item = items[0].get("Item", items[0]) if isinstance(items[0], dict) else items[0]

    # 圖片格式也是不一
    # 1. {imageUrl:"xxx"}
    # 2. "xxx" (直接是 url)
    # 一樣用 isinstance 去抓
    image_urls: list[str] = []
    for image in item.get("mediumImageUrls", []):
        raw_url = image.get("imageUrl") if isinstance(image, dict) else str(image)
        if raw_url:
            image_urls.append(clean_rakuten_image_url(raw_url))

    price = item.get("itemPrice")
    availability = item.get("availability")

    return SourceProduct(
        source = "rakuten",
        source_id = str(item.get("itemCode", item_code)),
        source_url = item.get("itemUrl", url),
        title= str(item.get("itemName", "")).strip(),
        price_jpy = int(price) if price is not None else None,
        image_urls = image_urls[:9],
        description = str(item.get("itemCaption", "")).strip(),
        stock = 1 if availability == 1 else 0,
        category_hint = str(item.get("genreId", "")) or None,
    )
