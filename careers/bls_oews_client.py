"""
Fetch U.S. BLS Occupational Employment and Wage Statistics (OEWS) for tech career charts.

Uses the official BLS Public Data API v2 (JSON POST), not HTML scraping:
https://www.bls.gov/developers/api_signature_v2.htm

Register for a free API key: https://data.bls.gov/registrationEngine/
Set BLS_API_KEY in the environment (see mysite/settings.py).

Series ID format (25 chars): OE + U + area_type + area(7) + industry(6) + occupation(6) + datatype(2)
See: https://github.com/govex/bls-oews-api-tutorial
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# National, all industries; datatype 01 = employment, 08 = hourly median wage
# SOC codes are 6 digits without hyphen (2018 SOC).
TECH_OCCUPATIONS: tuple[tuple[str, str], ...] = (
    ("Software Developers", "151252"),
    ("Computer Systems Analysts", "151211"),
    ("Information Security Analysts", "151212"),
    ("Web & Digital Interface Designers", "151255"),
    ("Database Administrators", "151243"),
    ("Computer Network Architects", "151241"),
    ("Data Scientists (subset SOC)", "152051"),
)


def _series_prefix(metro_area_code: str | None) -> str:
    """OEUN… national cross-industry, or OEUM + 7-digit CBSA + 000000 industry."""
    code = (metro_area_code or "").strip()
    if len(code) == 7 and code.isdigit():
        return f"OEUM{code}000000"
    return "OEUN000000000000"


def _build_series_ids(prefix: str) -> tuple[list[str], list[str]]:
    """Returns (employment_series_ids, wage_series_ids) aligned with TECH_OCCUPATIONS."""
    emp: list[str] = []
    wage: list[str] = []
    for _label, occ6 in TECH_OCCUPATIONS:
        emp.append(f"{prefix}{occ6}01")
        wage.append(f"{prefix}{occ6}08")
    return emp, wage


def _cache_path(base_dir: Path) -> Path:
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "bls_tech_market_cache.json"


def _cache_valid(path: Path, max_age_seconds: float) -> bool:
    if not path.is_file():
        return False
    age = time.time() - path.stat().st_mtime
    return age >= 0 and age < max_age_seconds


def _load_cache(path: Path) -> dict[str, Any] | None:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError, TypeError):
        return None


def _save_cache(path: Path, payload: dict[str, Any]) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
    except OSError:
        pass


def _post_bls(series_ids: list[str], api_key: str, timeout: int = 45) -> dict[str, Any]:
    body = {
        "seriesid": series_ids,
        "registrationkey": api_key,
        "startyear": "2018",
        "endyear": str(time.gmtime().tm_year + 1),
    }
    data = json.dumps(body).encode("utf-8")
    req = Request(
        BLS_API_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "BMCC-Connect/1.0 (OEWS charts; contact: college IT)",
        },
        method="POST",
    )
    with urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    return json.loads(raw)


def _latest_value(series_block: dict[str, Any]) -> tuple[str | None, float | None]:
    """Most recent OEWS annual point from a BLS series object."""
    rows = series_block.get("data") or []
    if not rows:
        return None, None
    # BLS usually returns newest first; still pick max year
    best_year: str | None = None
    best_val: float | None = None
    for row in rows:
        y = str(row.get("year", ""))
        v_raw = row.get("value")
        if v_raw is None:
            continue
        try:
            v = float(str(v_raw).replace(",", ""))
        except ValueError:
            continue
        if best_year is None or y > best_year:
            best_year = y
            best_val = v
    return best_year, best_val


def fetch_tech_oews_live(
    api_key: str,
    *,
    metro_area_code: str | None = None,
) -> tuple[list[dict], list[dict], str, str] | None:
    """
    Returns (openings_points, salary_points, oews_year, geo_note) in CanvasJS shape,
    or None if the API fails or returns incomplete data.
    """
    prefix = _series_prefix(metro_area_code)
    emp_ids, wage_ids = _build_series_ids(prefix)
    all_ids = emp_ids + wage_ids

    try:
        parsed = _post_bls(all_ids, api_key)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, OSError):
        return None

    if parsed.get("status") != "REQUEST_SUCCEEDED":
        return None

    results = (parsed.get("Results") or {}).get("series") or []
    by_id = {s.get("seriesID"): s for s in results if s.get("seriesID")}

    openings: list[dict] = []
    salary: list[dict] = []
    years: list[str] = []

    for label, occ6 in TECH_OCCUPATIONS:
        sid_e = f"{prefix}{occ6}01"
        sid_w = f"{prefix}{occ6}08"
        ye, ve = _latest_value(by_id.get(sid_e) or {})
        yw, vw = _latest_value(by_id.get(sid_w) or {})
        if ve is None or vw is None:
            return None
        openings.append({"label": label, "y": int(round(ve))})
        salary.append({"y": round(vw, 2), "label": label})
        if ye:
            years.append(ye)
        if yw:
            years.append(yw)

    oews_year = max(years) if years else str(time.gmtime().tm_year)
    if len(metro_area_code or "") == 7:
        geo = f"Metropolitan area CBSA {metro_area_code} (BLS OEWS)"
    else:
        geo = "United States, national (BLS OEWS)"

    return openings, salary, oews_year, geo


def load_or_fetch_tech_oews(
    api_key: str,
    base_dir: Path,
    *,
    cache_hours: int = 24,
    metro_area_code: str | None = None,
    force_refresh: bool = False,
) -> tuple[list[dict], list[dict], str, str] | None:
    path = _cache_path(base_dir)
    ttl = max(1, int(cache_hours)) * 3600

    if not force_refresh and _cache_valid(path, ttl):
        cached = _load_cache(path)
        if cached and cached.get("version") == 1:
            try:
                return (
                    cached["openings"],
                    cached["salary"],
                    str(cached["oews_year"]),
                    str(cached["geo_note"]),
                )
            except (KeyError, TypeError):
                pass

    result = fetch_tech_oews_live(api_key, metro_area_code=metro_area_code)
    if result is None:
        stale = _load_cache(path)
        if stale and stale.get("version") == 1:
            try:
                return (
                    stale["openings"],
                    stale["salary"],
                    str(stale["oews_year"]),
                    str(stale["geo_note"]) + " (stale cache; live fetch failed)",
                )
            except (KeyError, TypeError):
                pass
        return None

    openings, salary, oews_year, geo_note = result
    _save_cache(
        path,
        {
            "version": 1,
            "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "openings": openings,
            "salary": salary,
            "oews_year": oews_year,
            "geo_note": geo_note,
            "metro_area_code": metro_area_code or "",
        },
    )
    return result
