from pathlib import Path
import json
from datetime import datetime

_BASE_OUTPUT = Path(__file__).resolve().parent.parent / "output"


def save_screenshot(page, name: str):
    path = _BASE_OUTPUT / "screenshots"
    path.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=path / name, full_page=True)


def save_report(test_name: str, results: dict):
    path = _BASE_OUTPUT / "reports"
    path.mkdir(parents=True, exist_ok=True)

    report = {
        "test_name": test_name,
        "timestamp": datetime.now().isoformat(),
        "results": results,
    }

    with open(path / f"{test_name}.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
