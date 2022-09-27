import logging.config
import sys

from crypto_price_downloader import __version__
from crypto_price_downloader.crypto_price_downloader import CryptoPriceDownloader
from crypto_price_downloader.utils import load_config

__logo__ = """
---------------------------------------------------------------------
crypto-price-downloader {}
---------------------------------------------------------------------
""".format(__version__.__version__)

CONFIG_FILE_PATH = "config.yaml"
LOGGER_CONFIG_FILE_PATH = "logger.conf"

# Init
logging.config.fileConfig(fname=LOGGER_CONFIG_FILE_PATH, disable_existing_loggers=False)
logging.info(__logo__)
config = load_config(CONFIG_FILE_PATH)

if __name__ == '__main__':
    crypto_price_downloader = CryptoPriceDownloader(config["RateExceedDelaySeconds"])
    exchange = sys.argv[1]

    if exchange == "PhemexFutures":
        crypto_price_downloader.download_phemex_futures_price()

    if exchange == "KucoinSpot":
        crypto_price_downloader.download_kucoin_spot_price()

    if exchange == "BinanceSpot":
        crypto_price_downloader.download_binance_spot_price()
