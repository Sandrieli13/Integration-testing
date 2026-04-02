"""Parse BMCC CUNY Pathways elective list pages (accordion dt/dd HTML)."""

import re
from html import unescape
from urllib.error import URLError
from urllib.request import Request, urlopen

ACCORDION_PAIR = re.compile(
    r"<dt>.*?<div[^>]*>(.*?)</div></dt><dd[^>]*>(.*?)</dd>",
    re.DOTALL | re.IGNORECASE,
)
CODE_RE = re.compile(r'coursenum"><a[^>]*>([^<]+)</a>', re.I)
CRS_RE = re.compile(r'(\d+)\s*<span class="small-label">\s*CRS', re.I)
# e.g. ANT 100, CRT 100.6, TRS 233
CODE_VALIDATE = re.compile(r"^[A-Z]{2,5}\s+\d{3}(?:\.\d+)?[A-Z]?$")


def strip_tags(html_fragment: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html_fragment)
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def fetch_page(url: str, *, timeout: int = 60) -> str:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (integration-testing)"})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


# BMCC department course listings (e.g. CIS) use <dt>/<dd> blocks, not Pathways accordions.
DT_DD_PAIR = re.compile(
    r"<dt[^>]*>(.*?)</dt>\s*<dd[^>]*>(.*?)</dd>",
    re.DOTALL | re.IGNORECASE,
)
DT_DD_HEADER = re.compile(
    r"(\d+)\s*CRS.*?(CIS|CSC|GIS)\s+(\d+)\s+(.+)",
    re.DOTALL | re.IGNORECASE,
)


def parse_department_course_listing(html: str) -> dict[str, tuple[int, str, str]]:
    """
    Parse a BMCC department course-listing page.
    Returns mapping 'CIS 317' -> (credit, course_name, description).
    """
    by_code: dict[str, tuple[int, str, str]] = {}
    for header_html, body_html in DT_DD_PAIR.findall(html):
        header = strip_tags(header_html)
        m = DT_DD_HEADER.search(header)
        if not m:
            continue
        credit = int(m.group(1))
        dept = m.group(2).upper()
        num = m.group(3)
        title = strip_tags(m.group(4))
        code_key = f"{dept} {num}"
        course_name = f"{code_key} — {title}"[:255]
        description = strip_tags(body_html)
        by_code[code_key] = (credit, course_name, description)
    return by_code


def parse_courses_from_html(html: str) -> list[tuple[int, str, str]]:
    """Return list of (credit, course_name, description)."""
    rows: list[tuple[int, str, str]] = []
    for header, body in ACCORDION_PAIR.findall(html):
        cm = CODE_RE.search(header)
        if not cm:
            continue
        code = strip_tags(cm.group(1))
        if not CODE_VALIDATE.match(code):
            continue
        crs = CRS_RE.search(header)
        credit = int(crs.group(1)) if crs else 3
        tail = header[cm.end() :]
        tm = re.search(r"<a[^>]*>([^<]+)</a>", tail)
        title = strip_tags(tm.group(1)) if tm else ""
        course_name = f"{code} — {title}"[:255]
        description = strip_tags(body)
        rows.append((credit, course_name, description))
    return rows


def fetch_and_parse(url: str) -> list[tuple[int, str, str]]:
    try:
        raw = fetch_page(url)
    except URLError as e:
        raise RuntimeError(f"Failed to fetch {url}: {e}") from e
    return parse_courses_from_html(raw)
