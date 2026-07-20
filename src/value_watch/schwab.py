from __future__ import annotations

import base64
import json
import webbrowser
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlencode, urlparse

from .config import Settings
from .http import request_json

AUTH_URL = "https://api.schwabapi.com/v1/oauth/authorize"
TOKEN_URL = "https://api.schwabapi.com/v1/oauth/token"
QUOTES_URL = "https://api.schwabapi.com/marketdata/v1/quotes"


class SchwabClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.token_path = settings.data_dir / "schwab-token.json"

    def _headers(self) -> dict[str, str]:
        raw = f"{self.settings.client_id}:{self.settings.client_secret}".encode()
        return {"Authorization": "Basic " + base64.b64encode(raw).decode(),
                "Content-Type": "application/x-www-form-urlencoded"}

    def login(self) -> None:
        """Perform interactive OAuth. Copy the final redirected URL if the local page fails to load."""
        query = urlencode({"response_type": "code", "client_id": self.settings.client_id,
                           "redirect_uri": self.settings.callback_url})
        url = f"{AUTH_URL}?{query}"
        print("Opening Schwab sign-in. After approval, copy the entire URL from the browser address bar.")
        print(url)
        webbrowser.open(url)
        redirected = input("Paste redirected URL: ").strip()
        # parse_qs decodes once. unquote covers browsers that preserve a double-encoded code.
        code = unquote(parse_qs(urlparse(redirected).query).get("code", [""])[0])
        if not code:
            raise ValueError("No authorization code found in the redirected URL.")
        token = request_json(TOKEN_URL, headers=self._headers(), data={
            "grant_type": "authorization_code", "code": code,
            "redirect_uri": self.settings.callback_url,
        })
        self._save_token(token)

    def _save_token(self, token: dict) -> None:
        self.token_path.parent.mkdir(parents=True, exist_ok=True)
        token["obtained_at"] = datetime.now(timezone.utc).isoformat()
        self.token_path.write_text(json.dumps(token, indent=2) + "\n")
        self.token_path.chmod(0o600)

    def _access_token(self) -> str:
        if not self.token_path.exists():
            raise ValueError("No Schwab token. Run `value-watch login` first.")
        token = json.loads(self.token_path.read_text())
        # A refresh token lasts longer than the short-lived access token. Refresh before each report.
        refreshed = request_json(TOKEN_URL, headers=self._headers(), data={
            "grant_type": "refresh_token", "refresh_token": token["refresh_token"],
        })
        if "refresh_token" not in refreshed:
            refreshed["refresh_token"] = token["refresh_token"]
        self._save_token(refreshed)
        return refreshed["access_token"]

    def quotes(self, symbols: list[str]) -> dict[str, dict]:
        auth = {"Authorization": f"Bearer {self._access_token()}"}
        query = urlencode({"symbols": ",".join(symbols), "fields": "quote,fundamental"})
        return request_json(f"{QUOTES_URL}?{query}", headers=auth)
