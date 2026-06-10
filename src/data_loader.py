import pandas as pd
import yfinance as yf

from src.config import (TICKERS, BENCHMARK, START_DATE, END_DATE, DATA_DIR)


def download_ticker_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    try:
        print(f"[INFO] Downloading data for {ticker}...")
        df = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            auto_adjust=True,
            progress=False
        )

        if df is None or df.empty:
            raise ValueError(
                f"No data returned for ticker: {ticker}"
            )

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.reset_index()
        df["Ticker"] = ticker
        df = df[["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"]]

        print(
            f"[SUCCESS] {ticker}: "
            f"{len(df):,} rows downloaded."
        )
        
        return df

    except Exception as ex:
        print(
            f"[ERROR] Failed to download "
            f"{ticker}: {ex}"
        )

        return pd.DataFrame()


def download_stock_data() -> None:
    print("\n" + "=" * 60)
    print("DOWNLOADING STOCK DATA")
    print("=" * 60)

    all_data = []
    failed_tickers = []

    for ticker in TICKERS:
        stock_df = download_ticker_data(
            ticker=ticker,
            start_date=START_DATE,
            end_date=END_DATE
        )

        if stock_df.empty:
            failed_tickers.append(ticker)
            continue

        stock_df["Ticker"] = ticker
        all_data.append(stock_df)

    if not all_data:
        raise RuntimeError("No stock data downloaded successfully.")

    stock_df = pd.concat(all_data, ignore_index=True)

    output_file = DATA_DIR / "stock_data.csv"

    stock_df.to_csv(output_file, index=False)

    print("\n" + "-" * 60)
    print("STOCK DOWNLOAD SUMMARY")
    print("-" * 60)
    print(f"Successful Tickers : {len(all_data)}")
    print(f"Failed Tickers     : {len(failed_tickers)}")

    if failed_tickers:
        print(
            f"Failed List: "
            f"{', '.join(failed_tickers)}"
        )

    print(f"\n[SUCCESS] Stock data saved to:")
    print(output_file.resolve())


def download_benchmark_data() -> None:
    print("\n" + "=" * 60)
    print("DOWNLOADING BENCHMARK DATA")
    print("=" * 60)

    try:
        benchmark_df = download_ticker_data(
            ticker=BENCHMARK,
            start_date=START_DATE,
            end_date=END_DATE
        )

        if benchmark_df.empty:
            raise RuntimeError(
                f"Benchmark download failed for {BENCHMARK}"
            )

        if isinstance(benchmark_df.columns, pd.MultiIndex):
            benchmark_df.columns = benchmark_df.columns.get_level_values(0)
        benchmark_df.drop(columns="Ticker", inplace=True)
        
        output_file = DATA_DIR / "benchmark_data.csv"
        benchmark_df.to_csv(output_file, index=False)

        print(f"\n[SUCCESS] Benchmark data saved to:")
        print(output_file.resolve())

    except Exception as ex:
        print(f"[ERROR] Benchmark download failed: {ex}")
        raise