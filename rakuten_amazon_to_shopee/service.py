from __future__ import annotations

import json
from pathlib import Path
import webbrowser

from .credentials import (
    prompt_int,
    prompt_rakuten_credentials,
    prompt_text,
    prompt_yes_no,
)
from .models import SourceProduct
from .preview_renderer import render_preview_html
from .source_router import detect_source
from .transform import source_to_listing_preview

# 用 url 獲得商品 json
# source_credentials 可不填，後面會用 getenv 去找
def fetch_source_product(url: str, source_credentials=None):
    source = detect_source(url)
    if source == "rakuten":
        from .rakuten_client import get_rakuten_item_by_url

        return get_rakuten_item_by_url(url, credentials=source_credentials)
    raise ValueError("Only Rakuten URLs support automatic fetching.")


def prompt_multiline(label: str) -> str:
    print(f"{label} (finish with an empty line)")
    lines: list[str] = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line.rstrip())
    return "\n".join(lines).strip()


def prompt_image_urls() -> list[str]:
    print("Image URLs (one per line, press Enter on an empty line to finish)")
    urls: list[str] = []
    while True:
        line = input().strip()
        if not line:
            break
        urls.append(line)
    return urls


def prompt_manual_product(reference_url: str = "") -> tuple[SourceProduct, int | None]:
    title = prompt_text("Product title")
    price_jpy = prompt_int("Source price JPY", required=False)
    price_twd_override = prompt_int(
        "Sale price TWD (leave blank for auto-calc)",
        required=False,
    )
    description = prompt_multiline("Product description")
    image_urls = prompt_image_urls()
    source_url = reference_url or prompt_text("Source URL", required=False) or ""

    if price_jpy is None and price_twd_override is None:
        raise ValueError(
            "Please provide either a source JPY price or a final TWD sale price."
        )

    return (
        SourceProduct(
            source="manual",
            source_id="manual-entry",
            source_url=source_url,
            title=title,
            price_jpy=price_jpy,
            image_urls=image_urls,
            description=description,
            stock=1,
            category_hint=None,
        ),
        price_twd_override,
    )


def build_preview_from_product(
    product: SourceProduct,
    price_twd_override: int | None = None,
) -> dict:
    preview = source_to_listing_preview(product, price_twd_override=price_twd_override)
    output = {
        "input_url": product.source_url,
        "source_product": product.to_dict(),
        "listing_preview": preview.to_dict(),
    }

    Path("preview_payload.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    Path("preview.html").write_text(
        render_preview_html(preview),
        encoding="utf-8",
    )
    return output


def build_preview_from_url(
    url: str,
    source_credentials=None,
    price_twd_override: int | None = None,
) -> dict:
    source_product = fetch_source_product(url, source_credentials=source_credentials)
    return build_preview_from_product(
        source_product,
        price_twd_override=price_twd_override,
    )


def main() -> None:
    url = input("Paste a Rakuten URL, or press Enter for manual mode: ").strip()
    source = detect_source(url)
    result: dict

    if source == "rakuten" and prompt_yes_no(
        "Use Rakuten API to auto-fetch product details",
        default=True,
    ):
        print("Enter Rakuten API credentials. Press Enter to reuse .env values when set.")
        credentials = prompt_rakuten_credentials()
        price_twd_override = prompt_int(
            "Sale price TWD (leave blank for auto-calc)",
            required=False,
        )
        try:
            result = build_preview_from_url(
                url=url,
                source_credentials=credentials,
                price_twd_override=price_twd_override,
            )
        except Exception as exc:
            print(f"Rakuten fetch failed: {exc}")
            print("Switching to manual input.")
            product, price_twd_override = prompt_manual_product(reference_url=url)
            result = build_preview_from_product(
                product,
                price_twd_override=price_twd_override,
            )
    else:
        if url and source != "rakuten":
            print("Non-Rakuten link detected. It will be kept as a reference URL.")
        product, price_twd_override = prompt_manual_product(reference_url=url)
        result = build_preview_from_product(
            product,
            price_twd_override=price_twd_override,
        )

    preview_path = Path("preview.html").resolve()
    webbrowser.open(preview_path.as_uri())

    print("Generated preview_payload.json and preview.html")
    print(f"Source: {result['source_product']['source']}")
    print(f"Title: {result['listing_preview']['title']}")
    print(f"Price (JPY): {result['listing_preview']['price_jpy']}")
    print(f"Sale price (TWD): {result['listing_preview']['price_twd']}")
    print(f"Preview page: {preview_path}")
