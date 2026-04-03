"""
Best-effort fetch + parse of public BMCC Student Activities / clubs pages.

Uses only the Python standard library. Intended for occasional refresh via
management command — not for high-frequency scraping.
"""

from __future__ import annotations

import html as html_lib
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_CLUBS_URL = "https://www.bmcc.cuny.edu/student-affairs/student-activities/clubs/"
HOW_TO_JOIN_URL = "https://www.bmcc.cuny.edu/student-affairs/student-activities/clubs/how-to-join-a-club/"

USER_AGENT = (
    "BMCCConnect/1.0 (+student clubs directory; contact site operator; respects public pages)"
)


@dataclass
class BmccScrapeResult:
    intro_text: str = ""
    highlights: list[str] = field(default_factory=list)
    resource_links: list[dict[str, str]] = field(default_factory=list)
    osa_email: str = ""
    osa_phone: str = ""
    osa_hours: str = ""
    extra_notice: str = ""
    source_urls: list[str] = field(default_factory=list)
    raw_plain_text: str = ""
    error: str | None = None


_VOID = frozenset(
    {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }
)


class _EntryContentExtractor(HTMLParser):
    """Collect visible text and outbound links inside WordPress .entry-content."""

    def __init__(self) -> None:
        super().__init__()
        self._depth = 0
        self._in_skip = False
        self._suppress = 0  # skip BMCC left nav column inside .entry-content
        self._chunks: list[str] = []
        self._links: list[tuple[str, str]] = []
        self._link_href: str | None = None
        self._link_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = {k: v or "" for k, v in attrs}
        classes = (ad.get("class") or "").split()

        if self._suppress > 0:
            if tag not in _VOID:
                self._suppress += 1
            return

        if tag in ("script", "style", "noscript"):
            self._in_skip = True
            return

        if tag == "div" and "leftbar" in classes:
            self._suppress = 1
            return

        if tag == "div" and "entry-content" in classes and self._depth == 0:
            self._depth = 1
            return

        if self._depth > 0:
            if tag not in _VOID:
                self._depth += 1

        href = ad.get("href") or ""
        if (
            tag == "a"
            and self._depth > 0
            and (href.startswith("http") or href.startswith("mailto:"))
        ):
            self._link_href = href
            self._link_parts = []

        if tag == "br" and self._depth > 0 and not self._in_skip:
            self._chunks.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if self._suppress > 0:
            if tag not in _VOID:
                self._suppress -= 1
            return

        if tag in ("script", "style", "noscript"):
            self._in_skip = False
            return

        if self._depth > 0:
            if tag == "a" and self._link_href:
                label = " ".join(self._link_parts).strip()
                if label and len(label) < 500:
                    lab = html_lib.unescape(label)
                    self._links.append((self._link_href, lab))
                    self._chunks.append(lab)
                self._link_href = None
                self._link_parts = []

            if tag not in _VOID:
                self._depth -= 1

    def handle_data(self, data: str) -> None:
        if self._suppress > 0:
            return

        if self._depth > 0 and not self._in_skip:
            if self._link_href:
                self._link_parts.append(data)
            else:
                text = data.strip()
                if text:
                    self._chunks.append(html_lib.unescape(text))

    def plain_text(self) -> str:
        raw = " ".join(self._chunks)
        raw = re.sub(r"\s+", " ", raw)
        return raw.strip()

    def unique_links(self) -> list[tuple[str, str]]:
        seen: set[tuple[str, str]] = set()
        out: list[tuple[str, str]] = []
        for href, label in self._links:
            key = (href, label)
            if key not in seen:
                seen.add(key)
                out.append((href, label))
        return out


def _fetch_html(url: str) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=30) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def _extract_osa_from_text(text: str) -> tuple[str, str, str]:
    email = ""
    phone = ""
    hours = ""
    m = re.search(
        r"[Ee]mail:\s*([a-zA-Z0-9._%+-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})",
        text,
    )
    if m:
        email = m.group(1).strip()
    m = re.search(r"\(212\)\s*[\d\-]{7,12}", text)
    if m:
        phone = m.group(0).strip()
    m = re.search(
        r"Office Hours:\s*([^.]+\.)",
        text,
        re.I,
    )
    if m:
        hours = m.group(1).strip()
    if not hours:
        m = re.search(
            r"(Monday\s*-\s*Friday[^.]{5,120})",
            text,
            re.I,
        )
        if m:
            hours = m.group(1).strip()
    return email, phone, hours


def _paragraphs_from_plain(text: str, max_paragraphs: int = 4) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text)
    out: list[str] = []
    buf = ""
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if len(buf) + len(p) < 420:
            buf = f"{buf} {p}".strip() if buf else p
        else:
            if buf:
                out.append(buf)
            buf = p
        if len(out) >= max_paragraphs:
            break
    if buf and len(out) < max_paragraphs:
        out.append(buf)
    return [x for x in out if len(x) > 40]


def scrape_bmcc_clubs_pages(
    main_url: str = DEFAULT_CLUBS_URL,
    join_url: str | None = HOW_TO_JOIN_URL,
) -> BmccScrapeResult:
    result = BmccScrapeResult()
    texts: list[str] = []
    all_links: list[tuple[str, str]] = []

    for url in [main_url] + ([join_url] if join_url else []):
        try:
            html = _fetch_html(url)
        except (HTTPError, URLError, TimeoutError, OSError) as e:
            result.error = f"{type(e).__name__}: {e}"
            continue

        parser = _EntryContentExtractor()
        try:
            parser.feed(html)
            parser.close()
        except Exception as e:  # noqa: BLE001 — best-effort parse
            result.error = f"Parse error ({url}): {e}"
            continue

        plain = parser.plain_text()
        if plain:
            texts.append(plain)
        all_links.extend(parser.unique_links())
        result.source_urls.append(url)

    if not texts and result.error:
        return result

    combined = "\n\n".join(texts)
    result.raw_plain_text = combined[:20000]
    paras = _paragraphs_from_plain(combined, max_paragraphs=5)
    if paras:
        result.intro_text = paras[0]
        result.highlights = paras[1:4]

    email, phone, hours = _extract_osa_from_text(combined)
    result.osa_email = email
    result.osa_phone = phone
    result.osa_hours = hours

    # Pull registration / fair / club hours sentences into a short notice
    notice_bits: list[str] = []
    for line in re.split(r"(?<=[.!?])\s+", combined):
        line = line.strip()
        if not line:
            continue
        low = line.lower()
        if any(
            k in low
            for k in (
                "registration",
                "club fair",
                "club hours",
                "wednesdays",
                "deadline",
                "semester",
                "zoom",
                "openlab",
            )
        ):
            if 20 < len(line) < 400:
                notice_bits.append(line)
    result.extra_notice = " ".join(notice_bits[:6])[:2000]

    # Useful outbound links (BMCC / CUNY / OpenLab / Zoom), deduped by URL
    seen_h: set[str] = set()
    for href, label in all_links:
        if href.startswith("mailto:"):
            continue
        if (
            "bmcc.cuny.edu" not in href
            and "openlab.bmcc" not in href
            and "zoom.us" not in href
        ):
            continue
        if href in seen_h:
            continue
        seen_h.add(href)
        result.resource_links.append({"label": label[:120], "url": href})
        if len(result.resource_links) >= 12:
            break

    if not result.intro_text and combined:
        result.intro_text = combined[:800] + ("…" if len(combined) > 800 else "")

    return result


def scrape_result_to_model_dict(result: BmccScrapeResult, source_url: str) -> dict[str, Any]:
    return {
        "intro_text": result.intro_text[:4000],
        "highlights": result.highlights[:20],
        "resource_links": result.resource_links[:30],
        "osa_email": result.osa_email[:254],
        "osa_phone": result.osa_phone[:80],
        "osa_hours": result.osa_hours[:500],
        "extra_notice": result.extra_notice[:4000],
        "raw_plain_text": result.raw_plain_text[:50000],
        "source_url": source_url[:500],
        "fetch_error": (result.error or "")[:2000],
    }
