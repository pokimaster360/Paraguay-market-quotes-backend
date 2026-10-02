import re
import requests

from src.models.currency import Currency
from src.models.exchange_type import ExchangeType


def parse_price(value: str) -> int:
    """'5780.00' → 5780, '' → 0"""
    if not value:
        return 0
    clean = re.sub(r"[^\d.]", "", value)
    if not clean or clean == ".":
        return 0
    return int(float(clean))


def get_cotization(
    url="https://www.bancognb.com.py/public/currency_quotations",
):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0 Safari/537.36",
        "Referer": "https://www.bancognb.com.py/",
        "Accept": "application/json, text/plain, */*",
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()

        currencies = {}

        for item in data.get("exchangeRates", []):
            name = item["currencyCode"]  # "USD" / "EUR"

            cash_buy   = parse_price(item.get("cashBuyPrice", ""))
            cash_sell  = parse_price(item.get("cashSellPrice", ""))
            hb_buy     = parse_price(item.get("electronicBuyPrice", ""))
            hb_sell    = parse_price(item.get("electronicSellPrice", ""))

            # --- Efectivo ---
            currencies[name] = Currency(
                house="GNB",
                name=name,
                buy=str(cash_buy),
                sell=str(cash_sell),
                buy_trend=None,
                sell_trend=None,
                exchange_type=ExchangeType.CASH,
            )

            # --- Home Banking / APP ---
            currencies[f"{name}-app"] = Currency(
                house="GNB",
                name=name,
                buy=str(hb_buy),
                sell=str(hb_sell),
                buy_trend=None,
                sell_trend=None,
                exchange_type=ExchangeType.APP,
            )
        # print(currencies)
        return currencies

    except requests.RequestException as e:
        print(f"Error de request: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Error parseando JSON: {e}")
        return None


def test_get_cotization():
    result = get_cotization()
    if result:
        for name, data in result.items():
            print(f"{name}: Compra={data.buy} Venta={data.sell} ({data.exchange_type})")
    else:
        print("No se pudieron obtener las cotizaciones")


if __name__ == "__main__":
    test_get_cotization()