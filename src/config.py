from pathlib import Path


DATA_DIR = Path("data/raw")
TICKERS = [
    # Technology (3)
    "AAPL",   # Apple
    "MSFT",   # Microsoft
    "NVDA",   # NVIDIA

    # Financial (2)
    "JPM",    # JPMorgan Chase
    "BAC",    # Bank of America

    # Healthcare (2)
    "JNJ",    # Johnson & Johnson
    "PFE",    # Pfizer

    # Consumer (1)
    "AMZN"    # Amazon
]

BENCHMARK = "^GSPC" # S&P 500

START_DATE = "2020-01-01"
END_DATE = "2025-01-01"