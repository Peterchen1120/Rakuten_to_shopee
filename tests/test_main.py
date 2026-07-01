import json
import os
import tempfile
import unittest

from rakuten_amazon_to_shopee.main import build_preview_from_product
from rakuten_amazon_to_shopee.models import SourceProduct


class MainFlowTests(unittest.TestCase):
    def test_build_preview_from_product_writes_preview_files(self) -> None:
        product = SourceProduct(
            source="rakuten",
            source_id="shop:item",
            source_url="https://item.rakuten.co.jp/shop/item/",
            title="Sample Pouch",
            price_jpy=1500,
            image_urls=["https://example.com/image.jpg"],
            description="Compact pouch",
            stock=1,
            category_hint="100",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            previous_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                result = build_preview_from_product(product)
            finally:
                os.chdir(previous_cwd)

            payload_path = os.path.join(tmpdir, "preview_payload.json")
            html_path = os.path.join(tmpdir, "preview.html")
            self.assertTrue(os.path.exists(payload_path))
            self.assertTrue(os.path.exists(html_path))

            with open(payload_path, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
            with open(html_path, "r", encoding="utf-8") as handle:
                html = handle.read()

            self.assertEqual(payload["source_product"]["source_id"], "shop:item")
            self.assertEqual(payload["listing_preview"]["title"], "Sample Pouch")
            self.assertEqual(result["listing_preview"]["price_twd"], 840)
            self.assertIn("Copy Title", html)
            self.assertIn("Copy Price", html)


if __name__ == "__main__":
    unittest.main()
