#!/usr/bin/env python3
"""Build the single-file claude.ai preview pages from the site.

index.html and resume.html are the source of truth. This turns each one into a
self-contained page for the claude.ai Artifact links:

- strips the <!doctype>/<html>/<head>/<body> wrapper (the Artifact host adds its own),
- inlines every assets/*.jpg|png as a data: URI,
- points the site <-> resume links at the preview URLs,
- drops the "Download PDF" link (previews can't offer downloads).

Usage:
    python3 tools/build_preview.py [out_dir]     # default out_dir: ./preview (gitignored)

Then publish out_dir/site.html and out_dir/resume.html to the preview links below.
"""
import base64
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_URL = "https://claude.ai/artifact/X2g3E3G8hun9Q9xPR8913J"
RESUME_URL = "https://claude.ai/artifact/WrSSytJAjf86BDZnV5FzjN"

# Preview titles stay fixed so the claude.ai gallery entries keep their names.
TITLES = {"index.html": "Earl Carlson Lab Report", "resume.html": "Earl Carlson Resume"}
MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp", ".svg": "image/svg+xml"}


def unwrap(html):
    """Remove the document wrapper, keeping head contents (title, styles, fonts) and body."""
    html = re.sub(r"^\s*<!doctype html>\s*", "", html, flags=re.I)
    html = re.sub(r"<html[^>]*>\s*<head>\s*", "", html, count=1, flags=re.I)
    html = re.sub(r'<meta charset="[^"]*">\s*', "", html, count=1, flags=re.I)
    html = re.sub(r'<meta name="viewport"[^>]*>\s*', "", html, count=1, flags=re.I)
    html = re.sub(r"</head>\s*<body[^>]*>\s*", "", html, count=1, flags=re.I)
    html = re.sub(r"\s*</body>\s*</html>\s*$", "\n", html, flags=re.I)
    return html


def inline_assets(html):
    def repl(m):
        path = os.path.join(ROOT, m.group(1))
        ext = os.path.splitext(path)[1].lower()
        data = base64.b64encode(open(path, "rb").read()).decode()
        return "data:%s;base64,%s" % (MIME[ext], data)
    return re.sub(r"(?<![\w/.])(assets/[\w.\-]+\.(?:jpe?g|png|webp|svg))", repl, html)


def build(name, out_path):
    html = open(os.path.join(ROOT, name), encoding="utf-8").read()
    html = unwrap(html)
    html = re.sub(r"<title>.*?</title>", "<title>%s</title>" % TITLES[name], html, count=1)
    html = html.replace('href="resume.html"', 'href="%s"' % RESUME_URL)
    html = html.replace('href="index.html"', 'href="%s"' % SITE_URL)
    html = html.replace('<a href="resume.pdf">Download PDF</a>', "")
    html = inline_assets(html)
    assert "assets/" not in html, "an asset reference was left un-inlined in " + name
    assert "<html" not in html.lower() and "</body>" not in html.lower(), "document wrapper left in " + name
    open(out_path, "w", encoding="utf-8").write(html)
    return len(html)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "preview")
    os.makedirs(out, exist_ok=True)
    for src, dst in (("index.html", "site.html"), ("resume.html", "resume.html")):
        size = build(src, os.path.join(out, dst))
        print("%-12s -> %s (%d KB)" % (src, os.path.join(out, dst), size // 1024))
