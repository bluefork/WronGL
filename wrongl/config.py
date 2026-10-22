"""Configuration management for WronGL."""
from __future__ import annotations

import json
import logging
import os
import sys
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)

APP_NAME = "WronGL"
CONFIG_VERSION = 1


def _user_config_dir() -> Path:
    if sys.platform == "win32":
        base = os.environ.get("APPDATA") or (Path.home() / "AppData" / "Roaming")
    else:
        base = os.environ.get("XDG_CONFIG_HOME") or (Path.home() / ".config")
    return Path(base) / APP_NAME


def _user_data_dir() -> Path:
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA") or (Path.home() / "AppData" / "Local")
    else:
        base = os.environ.get("XDG_DATA_HOME") or (Path.home() / ".local" / "share")
    return Path(base) / APP_NAME


def _user_log_dir() -> Path:
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA") or (Path.home() / "AppData" / "Local")
        return Path(base) / APP_NAME / "logs"
    base = os.environ.get("XDG_STATE_HOME") or (Path.home() / ".local" / "state")
    return Path(base) / APP_NAME / "logs"


CONFIG_DIR = _user_config_dir()
CONFIG_PATH = CONFIG_DIR / "config.json"
DATA_DIR = _user_data_dir()
LOG_DIR = _user_log_dir()


@dataclass
class Config:
    version: int = CONFIG_VERSION
    hotkey: str = "<ctrl>+<shift>+l"
    layout_profile: str = "windows"
    convert_digits: bool = False
    convert_punctuation: bool = False  # reserved for Phase 3
    normalize_arabic: bool = True
    detection_mode: str = "smart"
    confidence_threshold: float = 0.55
    theme: str = "dark"
    window_geometry: str = "760x620"
    show_tray: bool = True
    minimize_to_tray: bool = True
    history_size: int = 20
    smart_clipboard: bool = True  # اضافه شده برای کلیپ‌بورد هوشمند

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Config":
        known = {f.name for f in fields(cls)}
        kwargs = {k: v for k, v in data.items() if k in known}
        return cls(**kwargs)


class ConfigManager:
    def __init__(self, path: Path = CONFIG_PATH) -> None:
        self.path = path
        self.config = Config()

    def load(self) -> Config:
        try:
            if self.path.exists():
                raw = json.loads(self.path.read_text(encoding="utf-8"))
                version = int(raw.get("version", 0))
                if version < CONFIG_VERSION:
                    log.info("Migrating config from v%s to v%s", version, CONFIG_VERSION)
                    raw["version"] = CONFIG_VERSION
                self.config = Config.from_dict(raw)
            else:
                log.info("No config at %s — creating defaults", self.path)
                self.save()
        except (OSError, ValueError, TypeError) as exc:
            log.warning("Failed to load config: %s — using defaults", exc)
            self.config = Config()
        return self.config

    def save(self) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(
                json.dumps(self.config.to_dict(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            log.debug("Config saved: %s", self.path)
        except OSError as exc:
            log.error("Failed to save config: %s", exc)


def resource_path(relative_path: str) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)