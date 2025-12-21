import yfinance as yf
import re

TRADING_DAYS_PER_WEEK = 5


def parse_weeks(horizon: str) -> int:
    """
    Extract number of weeks from user input.
    Defaults to 1 week if parsing fails.
    """
    if not horizon:
        return 1

    h = horizon.lower().strip()

    # Numeric only: "1", "2", "4"
    if re.fullmatch(r"\d+", h):
        return int(h)

    # Text: "2 weeks", "3 week", "4 weeks"
    match = re.search(r"(\d+)", h)
    if match:
        return int(match.group(1))

    return 1


def get_price_series(symbol: str, horizon: str):
    try:
        weeks = parse_weeks(horizon)
        days_needed = weeks * TRADING_DAYS_PER_WEEK

        # Fetch a SAFE period (Yahoo-supported)
        ticker = yf.Ticker(symbol.upper() + ".NS")
        hist = ticker.history(period="3mo", interval="1d")

        if hist.empty:
            return []

        # Take last N trading days
        hist = hist.tail(days_needed)

        return [
            {
                "time": idx.strftime("%Y-%m-%d"),
                "close": round(float(row["Close"]), 2)
            }
            for idx, row in hist.iterrows()
        ]

    except Exception as e:
        print("Price fetch error:", e)
        return []
