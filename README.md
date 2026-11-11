# Earl Carlson — portfolio

A static, single-page portfolio in the "lab report" print direction. No build step, no dependencies.

## Structure

- `index.html` — the whole site: homepage plus four case studies, shown by URL hash
  (`#docker`, `#digitalocean`, `#facebook`, `#nokia-rebel`). Styles and scripts are inline.
- `assets/` — portrait and case-study images (JPEG).
- `brief.html` — the design brief and changelog.

Fonts load from Google Fonts (Archivo, Courier Prime).

## Run locally

Open `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Before making it public

- Facebook case: research participants' faces are shown. Confirm consent.
- Docker case: names a colleague (Sean Brady) and internal personas.
- DigitalOcean case: hero image is still a stand-in.
- Contact details and links are not filled in yet.
