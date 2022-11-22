import logging.config
import sys

from crypto_price_downloader.constants import LOGGER_CONFIG_FILE_PATH, __logo__, CONFIG_FILE_PATH
from crypto_price_downloader.crypto_price_downloader import CryptoPriceDownloader
from crypto_price_downloader.utils import load_config

if __name__ == '__main__':
    logging.config.fileConfig(fname=LOGGER_CONFIG_FILE_PATH, disable_existing_loggers=False)
    logging.info(__logo__)
    config = load_config(CONFIG_FILE_PATH)

    crypto_price_downloader = CryptoPriceDownloader(config["base"]["rateExceedDelaySeconds"])
    exchange = sys.argv[1]

    match exchange:
        case "PhemexFutures":
            crypto_price_downloader.download_phemex_futures_price()
        case "KucoinSpot":
            crypto_price_downloader.download_kucoin_spot_price()
        case "BinanceSpot":
            crypto_price_downloader.download_binance_spot_price()
        case "Okx":
            crypto_price_downloader.download_okx_spot_price()
        case "SimpleFx":
            crypto_price_downloader.download_simple_fx_cfd_price()
        case "BybitFutures":
            crypto_price_downloader.download_bybit_futures_price()
        case _:
            raise Exception("Not supported exchange - [}".format(exchange))
