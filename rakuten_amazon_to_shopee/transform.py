from __future__ import annotations

import math
import re

from .models import ListingPreview, SourceProduct

BANNED_WORDS = [
    "Amazon",
    "amazon",
    "Rakuten",
    "rakuten",
    "Amazon.co.jp",
    "amazon.co.jp",
    "Rakuten Ichiba",
]


def clean_text(text: str, max_len: int) -> str:
    value = re.sub(r"<[^>]+>", "", text)
    value = re.sub(r"\s+", " ", value).strip()
    for word in BANNED_WORDS:
        value = value.replace(word, "")
    return value[:max_len].strip()


def price_jpy_to_twd(
    price_jpy: int,
    fx_rate: float = 0.22,
    international_shipping_twd: int = 220,
    handling_fee_twd: int = 80,
    platform_fee_rate: float = 0.08,
    margin_rate: float = 0.25,
) -> int:
    base_twd = price_jpy * fx_rate
    cost_twd = base_twd + international_shipping_twd + handling_fee_twd
    final_twd = cost_twd * (1 + platform_fee_rate + margin_rate)
    return int(math.ceil(final_twd / 10.0) * 10)


def source_to_listing_preview(
    product: SourceProduct,
    price_twd_override: int | None = None,
) -> ListingPreview:
    if price_twd_override is None and product.price_jpy is None:
        raise ValueError(
            f"Source product needs a JPY price or TWD override: {product.source_id}"
        )

    description = clean_text(product.description, 1800) or "請補上商品描述"
    price_twd = (
        price_twd_override
        if price_twd_override is not None
        else price_jpy_to_twd(product.price_jpy or 0)
    )

    return ListingPreview(
        title=clean_text(product.title, 120),
        description=description,
        price_twd=price_twd,
        price_jpy=product.price_jpy,
        image_urls=product.image_urls[:9],
        source=product.source,
        source_id=product.source_id,
        source_url=product.source_url,
    )
