def verify_price_format(price: str):
    assert price.startswith("$"), f"Цена не в формате $, получено: {price}"


def price_to_float(price: str) -> float:
    return float(price.split("$")[1])


def extract_price(text: str) -> str:
    return "$" + text.strip().split("$")[1]


def log_step(logger, results, msg):
    logger.info(msg)
    results["steps"].append(msg)
