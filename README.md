# Earl Carlson — portfolio

A static, single-page portfolio in the "lab report" print direction. No build step, no dependencies.

## Structure

- `index.html` — the whole site: homepage plus four case studies, shown by URL hash
  (`#docker`, `#digitalocean`, `#facebook`, `#nokia-rebel`). Styles and scripts are inline.
- `assets/` — portrait and case-study images (JPEG).
- `resume.html` — the resume in the site's style. Prints to a plain, single-column page.
- `resume.pdf` — that page printed to PDF (2 pages, real text, no images) for ATS uploads.
- `brief.html` — the design brief and changelog.
- `tools/build_preview.py` — builds the single-file claude.ai preview pages (see below).

Fonts load from Google Fonts (Archivo, Courier Prime).

## Run locally

Serve the folder (the portrait's ink effect uses WebGL, which can't read images from `file://`, so opening `index.html` directly shows a still portrait):

```sh
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Before making it public

- Facebook case: research participants' faces are shown. Confirm consent.
- Docker case: names a colleague (Sean Brady) and internal personas.
- DigitalOcean case: hero image is still a stand-in.

## Regenerating the resume PDF

Open `resume.html` in Chrome, Print, Destination "Save as PDF", Margins "Default", and turn Headers and footers off.
The print styles handle the rest (white page, no effects, flags hidden).

## Updating the claude.ai previews

`index.html` and `resume.html` are the source. Edit them directly, then:

```sh
python3 tools/build_preview.py      # writes preview/site.html and preview/resume.html (gitignored)
```

That inlines the images, strips the page wrapper and points the site/resume links at the preview URLs.
Publish `preview/site.html` to https://claude.ai/artifact/X2g3E3G8hun9Q9xPR8913J and
`preview/resume.html` to https://claude.ai/artifact/WrSSytJAjf86BDZnV5FzjN.
