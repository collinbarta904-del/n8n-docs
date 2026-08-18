# fonts

All web fonts are **self-hosted** — the page loads no font CDN.

- `fonts.css` — `@font-face` rules for **Inter** (UI) and **Handjet** (retro
  dot-matrix display), with the `.woff2` files under `webfonts/`. Generated from
  Google Fonts and rewritten to local paths.
- `GeistPixel-Circle.woff2` — optional local fallback in the display stack
  (`"Handjet", "Geist Pixel Circle", monospace`). The page renders correctly
  without it.

Font Awesome brand icons are likewise self-hosted under `../vendor/fontawesome/`.

> Note: the original spec called for `BubbledotICG-FinePos` from the OnlineWebFonts
> CDN. That host is blocked by egress policy in the build environment, so the
> headline uses **Handjet** — a genuine LED/dot-matrix face that is freely
> self-hostable. To switch back, drop the real `BubbledotICG-FinePos.woff2` here,
> add an `@font-face` for it in `fonts.css`, and put it first in `--font-display`.
