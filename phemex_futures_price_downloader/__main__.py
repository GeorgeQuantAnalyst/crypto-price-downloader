import logging.config
import sys

import ccxt
import pandas as pd

from phemex_futures_price_downloader import __version__

__logo__ = """
---------------------------------------------------------------------
phemex-futures-price-downloader {}
---------------------------------------------------------------------
""".format(__version__.__version__)

LOGGER_CONFIG_FILE_PATH = "logger.conf"

# Init
logging.config.fileConfig(fname=LOGGER_CONFIG_FILE_PATH, disable_existing_loggers=False)

if __name__ == '__main__':
    try:
        logging.info(__logo__)
        logging.info("Load dataset assets.csv")
        assets = pd.read_csv("data/assets.csv")
        exchange = ccxt.phemex()

        logging.info("Replace suffix and prefix in tickers")
        assets["Ticker"] = assets["Ticker"].str.replace("PERP", "")
        assets["Ticker"] = assets["Ticker"].str.replace("100", "u100")

        logging.info("Fetch last price for tickers")
        assets["LastPrice"] = assets["Ticker"].apply(lambda x: exchange.fetch_ticker(x)["last"])

        logging.info("Save result to csv")
        assets.to_csv("data/assets_with_price.csv", index=False)
    except:
        logging.exception("Error in application:")
        sys.exit(1)
