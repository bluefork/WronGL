"""Logging configuration."""
from __future__ import annotations

import logging
import logging.handlers
import sys
from pathlib import Path

from .config import LOG_DIR

_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_DATE = "%Y-%m-%d %H:%M:%S"


def setup_logging(level: int = logging.INFO, log_dir: Path = LOG_DIR) -> None:
    root = logging.getLogger()
    root.setLevel(level)
    for h in list(root.handlers):
        root.removeHandler(h)

    fmt = logging.Formatter(_FORMAT, datefmt=_DATE)

    console = logging.StreamHandler(sys.stderr)
    console.setFormatter(fmt)
    console.setLevel(level)
    root.addHandler(console)

    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        fh = logging.handlers.RotatingFileHandler(
            log_dir / "wrongl.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8"
        )
        fh.setFormatter(fmt)
        fh.setLevel(logging.DEBUG)
        root.addHandler(fh)
    except OSError as exc:
        logging.getLogger(__name__).warning("File logging unavailable: %s", exc)

    for noisy in ("PIL", "urllib3", "wordfreq"):
        logging.getLogger(noisy).setLevel(logging.WARNING)