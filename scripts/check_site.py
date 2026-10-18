#!/usr/bin/env python3
"""Check the actual deployable output; standard library only."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / "_site"
PUBLIC_EMAILS = {"contact@vineethkrishnat.com"}
EXPECTED = {"index.html", "research.html", "publications.html", "cv.html", "404.html"}
EXPECTED |= {"papers/" + p.with_suffix(".html").name for p in (ROOT.parent / "papers").glob("*.qmd")}


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.has_description = False
        self.has_title = False
        self.h1_count = 0
        self.figure_count = 0
        self.display_math_count = 0
        self.errors = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            if attrs["id"] in self.ids:
                self.errors.append("duplicate HTML id")
            self.ids.add(attrs["id"])
        if tag == "h1":
            self.h1_count += 1
        if tag == "figure":
            self.figure_count += 1
        if {"math", "display"}.issubset(attrs.get("class", "").split()):
            self.display_math_count += 1
        if tag == "title":
            self.has_title = True
        if tag == "meta" and attrs.get("name") == "description" and attrs.get("content"):
            self.has_description = True
        if tag == "img" and not attrs.get("alt"):
            self.errors.append("image missing alternative text")
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])


def main():
    errors = []
    if not ROOT.is_dir():
        sys.exit("Render the website with 'quarto render' before checking it.")
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*.html") if "site_libs" not in p.parts}
    if actual != EXPECTED:
        errors.append("unexpected or missing HTML pages; remove stale _site output and render again")
    pages = {}
    for name in sorted(EXPECTED & actual):
        path = ROOT / name
        source = path.read_text()
        page = Page(source)
        pages[path] = page
        errors.extend(f"{name}: {message}" for message in page.errors)
        if not page.has_title or not page.has_description:
            errors.append(f"{name}: missing page title or description")
        # The home title block is hidden in favor of the custom introduction.
        if page.h1_count != (2 if name == "index.html" else 1):
            errors.append(f"{name}: unexpected heading structure")
        if name.startswith("papers/"):
            if page.figure_count != 2 or page.display_math_count != 4:
                errors.append(f"{name}: expected two original figures and four source equations")
        # Generic checks avoid storing any removed personal details in this checker.
        emails = {email.casefold() for email in re.findall(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", source)}
        if emails - PUBLIC_EMAILS:
            errors.append(f"{name}: unapproved email address; review without publishing")
        patterns = {
            "phone number": r"(?<!\d)(?:\+1[ -]?)?\(?\d{3}\)?[ -]\d{3}[ -]\d{4}(?!\d)",
            "personal filesystem path": r"/Users/|/home/[^/]+/",
            "draft paper identifier": r"24xx\.xxxx",
            "residential contact heading": r"<h[1-6][^>]*>Contact Information|\bApt\s+\d",
        }
        for label, pattern in patterns.items():
            if re.search(pattern, source, re.I):
                errors.append(f"{name}: possible {label}; review without publishing")
    for path, page in pages.items():
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                if url.scheme == "http":
                    errors.append(f"{path.name}: insecure external link")
                continue
            decoded = unquote(url.path)
            target = (ROOT / decoded.lstrip("/")) if decoded.startswith("/") else path.parent / decoded
            if not decoded:
                target = path
            if target.is_dir():
                target = target / "index.html"
            target = target.resolve()
            if not target.is_relative_to(ROOT.resolve()) or not target.is_file():
                errors.append(f"{path.name}: broken local link {link}")
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f"{path.name}: missing fragment {link}")
    for required in ("CNAME", "robots.txt", "sitemap.xml", ".nojekyll", "assets/site.js", "assets/favicon.svg"):
        if not (ROOT / required).is_file():
            errors.append(f"missing deployment resource: {required}")
    if (ROOT / "CNAME").is_file() and (ROOT / "CNAME").read_text().strip() != "vineethkrishnat.com":
        errors.append("CNAME does not match the intended domain")
    portrait = ROOT / "assets/profile.jpeg"
    if portrait.is_file():
        image = portrait.read_bytes()
        if any(marker in image for marker in (b"Exif\x00\x00", b"http://ns.adobe.com/xap", b"Photoshop 3.0")):
            errors.append("portrait contains embedded EXIF/XMP/IPTC metadata; strip it before publishing")
    if errors:
        sys.exit("Website checks failed:\n- " + "\n- ".join(errors))
    print(f"Passed: {len(pages)} pages, local links and fragments, image descriptions, metadata, public-content checks, and deployment resources.")


if __name__ == "__main__":
    main()
