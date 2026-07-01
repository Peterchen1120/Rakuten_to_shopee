import unittest

from rakuten_amazon_to_shopee.source_router import (
    detect_source,
    extract_rakuten_item_code,
)


class SourceRouterTests(unittest.TestCase):
    def test_detect_rakuten(self) -> None:
        self.assertEqual(
            detect_source("https://item.rakuten.co.jp/shop-name/item-id/"), "rakuten"
        )

    def test_detect_non_rakuten_as_manual(self) -> None:
        self.assertEqual(
            detect_source("https://www.amazon.co.jp/dp/B0ABCDEF12"), "manual"
        )

    def test_extract_rakuten_item_code(self) -> None:
        self.assertEqual(
            extract_rakuten_item_code(
                "https://item.rakuten.co.jp/shop-name/item-id/?variant=1"
            ),
            "shop-name:item-id",
        )

if __name__ == "__main__":
    unittest.main()
