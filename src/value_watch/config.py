from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_dotenv(path: Path = ROOT / ".env") -> None:
    """Load simple KEY=VALUE entries without replacing exported environment values."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


@dataclass(frozen=True)
class Settings:
    client_id: str
    client_secret: str
    callback_url: str
    data_dir: Path = ROOT / "data"

    @classmethod
    def from_env(cls, require_credentials: bool = True) -> "Settings":
        load_dotenv()
        values = {
            "client_id": os.environ.get("SCHWAB_API_CLIENT_ID", ""),
            "client_secret": os.environ.get("SCHWAB_API_CLIENT_SECRET", ""),
            "callback_url": os.environ.get("SCHWAB_API_CALLBACK_URL", ""),
        }
        if require_credentials and not all(values.values()):
            env_names = {"client_id": "SCHWAB_API_CLIENT_ID", "client_secret": "SCHWAB_API_CLIENT_SECRET",
                         "callback_url": "SCHWAB_API_CALLBACK_URL"}
            missing = ", ".join(env_names[key] for key, value in values.items() if not value)
            raise ValueError(f"Missing {missing}. Copy .env.example to .env and fill it in.")
        return cls(**values)
