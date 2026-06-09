from src.data_loader import download_stock_data, download_benchmark_data


def main():
    download_stock_data()
    download_benchmark_data()


if __name__ == "__main__":
    main()