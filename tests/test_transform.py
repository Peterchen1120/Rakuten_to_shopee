import unittest

from rakuten_amazon_to_shopee.models import SourceProduct
from rakuten_amazon_to_shopee.transform import (
    clean_text,
    price_jpy_to_twd,
    source_to_listing_preview,
)


class TransformTests(unittest.TestCase):
    def test_clean_text_strips_html_and_banned_words(self) -> None:
        self.assertEqual(
            clean_text("<b>Amazon</b> Camera   Strap", 120),
            "Camera Strap",
        )

    def test_price_jpy_to_twd_rounds_up_to_tens(self) -> None:
        self.assertEqual(price_jpy_to_twd(1000), 700)

    def test_source_to_listing_preview_maps_fields(self) -> None:
        product = SourceProduct(
            source="rakuten",
            source_id="shop:item",
            source_url="https://item.rakuten.co.jp/shop/item/",
            title="Rakuten Sample Bag",
            price_jpy=1200,
            image_urls=["https://example.com/1.jpg"],
            description="A lightweight bag.",
            stock=2,
            category_hint="100",
        )

        preview = source_to_listing_preview(product)

        self.assertEqual(preview.title, "Sample Bag")
        self.assertEqual(preview.price_twd, 760)
        self.assertEqual(preview.image_urls, ["https://example.com/1.jpg"])


if __name__ == "__main__":
    unittest.main()
