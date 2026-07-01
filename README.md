# Rakuten Listing Copy Panel

This project turns product information into a local copy-ready preview page.

Current behavior:

- Fetch a single Rakuten product by URL
- Fall back to manual entry for non-Rakuten links or direct paste mode
- Transform the source product into a copy-ready listing preview
- Write `preview_payload.json`
- Write `preview.html` with clickable copy buttons
- Open the preview page in your browser

## Quick start

1. Create a virtual environment and install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

2. Optional: copy `.env.example` to `.env` and fill in your Rakuten credentials.

3. Run the CLI:

   ```powershell
   python main.py
   ```

4. Paste a Rakuten product URL, or press Enter to use manual mode.

The CLI can auto-fetch Rakuten details with the Rakuten API.
If you do not have Rakuten API access, or if you want to use an Amazon or other
reference link, the app will switch to manual input mode and still generate the
copy panel.

The preview page includes one-click copy buttons for:

- title
- sale price
- description
- primary image URL
- all image URLs
- all fields combined

## Notes

- Amazon and Shopee API integration were intentionally removed from this
  version.
- Review content rights before reusing source images or descriptions on any
  marketplace.
