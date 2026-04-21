import logging
from pathlib import Path

_LOGS_DIR = Path(__file__).resolve().parent.parent / "output" / "logs"


def get_logger(name: str) -> logging.Logger:
    _LOGS_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(_LOGS_DIR / f"{name}.log", encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(handler)

    return logger
