from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class HttpError(RuntimeError):
    pass


def request_json(url: str, *, headers: dict[str, str] | None = None,
                 data: dict[str, str] | None = None, timeout: int = 30) -> dict:
    payload = urlencode(data).encode() if data else None
    request = Request(url, data=payload, headers=headers or {})
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read())
    except HTTPError as exc:
        # OAuth errors are actionable (for example, invalid_grant) but request bodies never contain secrets.
        detail = exc.read().decode("utf-8", errors="replace").strip()
        raise HttpError(f"Request failed for {url}: HTTP {exc.code} {detail or exc.reason}") from exc
    except (URLError, json.JSONDecodeError) as exc:
        raise HttpError(f"Request failed for {url}: {exc}") from exc
