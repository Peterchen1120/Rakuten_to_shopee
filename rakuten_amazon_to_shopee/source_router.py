from urllib.parse import urlparse


def detect_source(url: str) -> str:
    host = urlparse(url).netloc.lower()

    if "rakuten.co.jp" in host:
        return "rakuten"

    return "manual"


def extract_rakuten_item_code(url: str) -> str:
    parsed = urlparse(url)
    path_parts = [part for part in parsed.path.split("/") if part]

    if len(path_parts) < 2:
        raise ValueError(f"Could not parse Rakuten itemCode from URL: {url}")

    shop_code, item_id = path_parts[0], path_parts[1]
    return f"{shop_code}:{item_id}"
