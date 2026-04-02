"""
Best-effort fetch of public BMCC Mathematics & Computer Science department page text.

Uses stdlib only; respects short timeouts. Intended to *enrich* seed descriptions, not replace curated data.
If the request fails, seeding continues without this text.
"""

from __future__ import annotations

import re
import ssl
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

BMCC_MCS_URL = "https://www.bmcc.cuny.edu/academics/departments/mathematics-computer-science/"
USER_AGENT = "BMCCConnectCareersSeeder/1.0 (+https://github.com/)"
TIMEOUT_SEC = 12


def fetch_department_page_text() -> str | None:
    ctx = ssl.create_default_context()
    req = Request(BMCC_MCS_URL, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=TIMEOUT_SEC, context=ctx) as resp:
            if resp.status != 200:
                return None
            raw = resp.read().decode("utf-8", errors="replace")
    except (URLError, HTTPError, TimeoutError, OSError):
        return None
    # Strip scripts/styles roughly; keep it cheap
    raw = re.sub(r"(?is)<script.*?>.*?</script>", " ", raw)
    raw = re.sub(r"(?is)<style.*?>.*?</style>", " ", raw)
    text = re.sub(r"<[^>]+>", " ", raw)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:15000] if text else None


def excerpt_for_context(snippet: str | None, max_chars: int = 400) -> str | None:
    if not snippet:
        return None
    return snippet[:max_chars].rsplit(" ", 1)[0] + "…"
