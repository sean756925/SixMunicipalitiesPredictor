"""Privacy-safe persistent page-view counter backed by Supabase."""
from __future__ import annotations

import json
from typing import Callable
from urllib.request import Request, urlopen


def record_supabase_view(
    supabase_url: str,
    anon_key: str,
    *,
    timeout: float = 5,
    opener: Callable = urlopen,
) -> tuple[int, int]:
    """Atomically record one view and return (all-time, today) counts.

    The Supabase RPC stores only a local calendar date and an aggregate count.
    It does not receive or store visitor identifiers from this application.
    """
    base_url = supabase_url.strip().rstrip("/")
    key = anon_key.strip()
    if not base_url.startswith("https://") or not key:
        raise ValueError("A valid HTTPS Supabase URL and anon key are required")

    request = Request(
        f"{base_url}/rest/v1/rpc/record_page_view",
        data=b"{}",
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    with opener(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))

    row = payload[0] if isinstance(payload, list) and payload else payload
    if not isinstance(row, dict):
        raise ValueError("Supabase returned an unexpected page-view response")

    total = int(row["total_views"])
    today = int(row["today_views"])
    if total < 0 or today < 0 or today > total:
        raise ValueError("Supabase returned invalid page-view counts")
    return total, today
