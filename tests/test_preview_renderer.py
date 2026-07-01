import unittest

from rakuten_amazon_to_shopee.models import ListingPreview
from rakuten_amazon_to_shopee.preview_renderer import render_preview_html


class PreviewRendererTests(unittest.TestCase):
    def test_render_preview_html_contains_copy_actions(self) -> None:
        preview = ListingPreview(
            title="Travel Pouch",
            description="Compact and lightweight.",
            price_twd=990,
            price_jpy=1990,
            image_urls=["https://example.com/image.jpg"],
            source="rakuten",
            source_id="shop:item",
            source_url="https://item.rakuten.co.jp/shop/item/",
        )

        html = render_preview_html(preview)

        self.assertIn("Copy Title", html)
        self.assertIn("Copy Price", html)
        self.assertIn("Copy Description", html)
        self.assertIn("Copy Image URL", html)
        self.assertIn("Travel Pouch", html)


if __name__ == "__main__":
    unittest.main()
