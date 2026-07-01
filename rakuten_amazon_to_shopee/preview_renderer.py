from __future__ import annotations

import json
from html import escape

from .models import ListingPreview


def _safe_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/")


def render_preview_html(preview: ListingPreview) -> str:
    primary_image = preview.image_urls[0] if preview.image_urls else ""
    copy_payload = {
        "title": preview.title,
        "price": str(preview.price_twd),
        "description": preview.description,
        "primaryImage": primary_image,
        "allImages": "\n".join(preview.image_urls),
        "allFields": "\n".join(
            [
                f"Title: {preview.title}",
                f"Sale price: {preview.price_twd}",
                f"Source price (JPY): {preview.price_jpy if preview.price_jpy is not None else 'N/A'}",
                f"Description:\n{preview.description}",
                f"Primary image: {primary_image or 'N/A'}",
                f"Source URL: {preview.source_url or 'N/A'}",
            ]
        ),
    }

    gallery_items = "\n".join(
        [
            (
                '<a class="thumb" href="{url}" target="_blank" rel="noreferrer">'
                '<img src="{url}" alt="Product image {index}"></a>'
            ).format(url=escape(url, quote=True), index=index + 1)
            for index, url in enumerate(preview.image_urls)
        ]
    )

    image_block = (
        (
            '<a class="hero-image" href="{url}" target="_blank" rel="noreferrer">'
            '<img src="{url}" alt="Primary product image"></a>'
        ).format(url=escape(primary_image, quote=True))
        if primary_image
        else '<div class="hero-empty">No image provided</div>'
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Listing Copy Panel</title>
  <style>
    :root {{
      --bg: #f7efe6;
      --panel: rgba(255, 251, 246, 0.92);
      --ink: #2b1f1a;
      --muted: #7a6157;
      --accent: #cc5c3d;
      --accent-strong: #a43d21;
      --line: rgba(79, 43, 31, 0.12);
      --shadow: 0 24px 60px rgba(93, 47, 29, 0.14);
    }}
    * {{
      box-sizing: border-box;
    }}
    body {{
      margin: 0;
      font-family: "Segoe UI Variable", "Noto Sans", "Microsoft JhengHei", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(214, 120, 88, 0.18), transparent 28%),
        linear-gradient(160deg, #f8f2eb 0%, #f2e2d6 45%, #f7efe6 100%);
      min-height: 100vh;
    }}
    .shell {{
      width: min(1100px, calc(100% - 32px));
      margin: 32px auto;
      display: grid;
      grid-template-columns: 1.05fr 1fr;
      gap: 24px;
    }}
    .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 28px;
      box-shadow: var(--shadow);
      backdrop-filter: blur(10px);
    }}
    .visual {{
      padding: 20px;
    }}
    .hero-image, .hero-empty {{
      display: grid;
      place-items: center;
      width: 100%;
      min-height: 430px;
      background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(244,228,216,0.9));
      border-radius: 22px;
      overflow: hidden;
      border: 1px solid rgba(79, 43, 31, 0.08);
    }}
    .hero-image img {{
      width: 100%;
      height: 100%;
      max-height: 540px;
      object-fit: contain;
      display: block;
    }}
    .hero-empty {{
      color: var(--muted);
      font-size: 18px;
      letter-spacing: 0.04em;
    }}
    .thumb-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
      gap: 12px;
      margin-top: 16px;
    }}
    .thumb {{
      aspect-ratio: 1;
      border-radius: 18px;
      overflow: hidden;
      border: 1px solid rgba(79, 43, 31, 0.08);
      background: white;
    }}
    .thumb img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .info {{
      padding: 22px;
      display: grid;
      gap: 16px;
      align-content: start;
    }}
    .heading {{
      display: flex;
      align-items: start;
      justify-content: space-between;
      gap: 16px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--line);
    }}
    .eyebrow {{
      margin: 0 0 6px;
      color: var(--muted);
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
    }}
    h1 {{
      margin: 0;
      font-size: clamp(28px, 4vw, 44px);
      line-height: 1.08;
    }}
    .tag {{
      padding: 9px 14px;
      border-radius: 999px;
      background: rgba(204, 92, 61, 0.12);
      color: var(--accent-strong);
      font-size: 13px;
      white-space: nowrap;
    }}
    .meta-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
    }}
    .card {{
      border: 1px solid var(--line);
      border-radius: 22px;
      padding: 18px;
      background: rgba(255, 255, 255, 0.58);
    }}
    .card h2 {{
      margin: 0 0 12px;
      font-size: 14px;
      color: var(--muted);
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }}
    .price {{
      font-size: 34px;
      font-weight: 700;
      color: var(--accent-strong);
    }}
    .sub {{
      margin-top: 8px;
      color: var(--muted);
      font-size: 14px;
    }}
    .copy-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 14px;
    }}
    button {{
      border: none;
      border-radius: 999px;
      padding: 11px 16px;
      background: linear-gradient(135deg, var(--accent), #e28362);
      color: white;
      font: inherit;
      cursor: pointer;
      transition: transform 120ms ease, box-shadow 120ms ease, background 120ms ease;
      box-shadow: 0 10px 22px rgba(164, 61, 33, 0.24);
    }}
    button:hover {{
      transform: translateY(-1px);
      background: linear-gradient(135deg, #c74e2d, #dc7250);
    }}
    button.secondary {{
      background: white;
      color: var(--ink);
      border: 1px solid rgba(79, 43, 31, 0.12);
      box-shadow: none;
    }}
    .field-value {{
      white-space: pre-wrap;
      word-break: break-word;
      line-height: 1.6;
      font-size: 16px;
    }}
    .description {{
      min-height: 220px;
    }}
    .source-link {{
      color: var(--accent-strong);
      word-break: break-all;
    }}
    .toast {{
      position: fixed;
      right: 20px;
      bottom: 20px;
      padding: 12px 16px;
      border-radius: 14px;
      background: rgba(43, 31, 26, 0.92);
      color: white;
      opacity: 0;
      transform: translateY(10px);
      transition: opacity 180ms ease, transform 180ms ease;
      pointer-events: none;
    }}
    .toast.show {{
      opacity: 1;
      transform: translateY(0);
    }}
    @media (max-width: 900px) {{
      .shell {{
        grid-template-columns: 1fr;
      }}
      .meta-grid {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <section class="panel visual">
      {image_block}
      <div class="thumb-grid">{gallery_items}</div>
    </section>
    <section class="panel info">
      <div class="heading">
        <div>
          <p class="eyebrow">Copy Ready Listing</p>
          <h1>{escape(preview.title)}</h1>
        </div>
        <div class="tag">{escape(preview.source.upper())}</div>
      </div>

      <div class="meta-grid">
        <article class="card">
          <h2>Sale Price</h2>
          <div class="price">NT$ {preview.price_twd}</div>
          <div class="sub">Source price JPY: {preview.price_jpy if preview.price_jpy is not None else "N/A"}</div>
          <div class="copy-row">
            <button type="button" data-copy-key="price">Copy Price</button>
          </div>
        </article>
        <article class="card">
          <h2>Primary Image</h2>
          <div class="field-value">{escape(primary_image or "N/A")}</div>
          <div class="copy-row">
            <button type="button" data-copy-key="primaryImage">Copy Image URL</button>
            <button type="button" class="secondary" data-copy-key="allImages">Copy All Image URLs</button>
          </div>
        </article>
      </div>

      <article class="card">
        <h2>Title</h2>
        <div class="field-value">{escape(preview.title)}</div>
        <div class="copy-row">
          <button type="button" data-copy-key="title">Copy Title</button>
        </div>
      </article>

      <article class="card">
        <h2>Description</h2>
        <div class="field-value description">{escape(preview.description)}</div>
        <div class="copy-row">
          <button type="button" data-copy-key="description">Copy Description</button>
          <button type="button" class="secondary" data-copy-key="allFields">Copy All Fields</button>
        </div>
      </article>

      <article class="card">
        <h2>Source URL</h2>
        <a class="source-link" href="{escape(preview.source_url or '#', quote=True)}" target="_blank" rel="noreferrer">{escape(preview.source_url or "N/A")}</a>
      </article>
    </section>
  </main>

  <div class="toast" id="toast">Copied</div>

  <script>
    const copyPayload = {_safe_json(copy_payload)};
    const toast = document.getElementById("toast");

    function showToast(message) {{
      toast.textContent = message;
      toast.classList.add("show");
      window.clearTimeout(showToast.timerId);
      showToast.timerId = window.setTimeout(() => {{
        toast.classList.remove("show");
      }}, 1400);
    }}

    async function copyField(key) {{
      const value = copyPayload[key] || "";
      try {{
        await navigator.clipboard.writeText(value);
        showToast("Copied");
      }} catch (error) {{
        showToast("Copy failed");
      }}
    }}

    document.querySelectorAll("[data-copy-key]").forEach((button) => {{
      button.addEventListener("click", () => copyField(button.dataset.copyKey));
    }});
  </script>
</body>
</html>
"""
