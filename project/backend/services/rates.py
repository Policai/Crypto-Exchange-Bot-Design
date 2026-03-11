import httpx

COINGECKO_IDS = {
    "BTC": "bitcoin",
    "LTC": "litecoin",
    "TRX": "tron",
    "TON": "the-open-network",
    "USDT": "tether",
}


async def get_rate(from_currency: str, to_currency: str, margin_percent: float = 2.0) -> float:
    if from_currency == to_currency:
        return 1.0
    if "RUB" in (from_currency, to_currency):
        vs = "rub"
    else:
        vs = "usd"

    ids = ",".join({COINGECKO_IDS.get(from_currency, "tether"), COINGECKO_IDS.get(to_currency, "tether")})
    async with httpx.AsyncClient(timeout=10) as client:
        data = (
            await client.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies={vs}"
            )
        ).json()

    from_price = data.get(COINGECKO_IDS.get(from_currency, "tether"), {}).get(vs, 1)
    to_price = data.get(COINGECKO_IDS.get(to_currency, "tether"), {}).get(vs, 1)
    base_rate = from_price / to_price
    return base_rate * (1 + margin_percent / 100)
