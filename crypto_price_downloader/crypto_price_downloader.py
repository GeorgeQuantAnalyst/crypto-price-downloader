import datetime
import logging
import time

import ccxt
import pandas as pd
from ccxt import RateLimitExceeded


class CryptoPriceDownloader:
    PHEMEX_FUTURES_CSV = "data/phemex_futures.csv"
    KUCOIN_SPOT_CSV = "data/kucoin_spot.csv"
    BINANCE_SPOT_CSV = "data/binance_spot.csv"

    DATE_TIME_FORMATTER = "%d.%m.%Y %X"

    def __init__(self, rate_exceed_delay_seconds):
        self.rate_exceed_delay_seconds = rate_exceed_delay_seconds
        self.phemex_client = ccxt.phemex()
        self.kucoin_client = ccxt.kucoin()
        self.binance_client = ccxt.binance()

    def download_phemex_futures_price(self):
        assets = pd.read_csv(self.PHEMEX_FUTURES_CSV)

        logging.info("Start downloading price for Phemex futures")
        count_assets = assets.shape[0]
        result = pd.DataFrame()
        for index, asset in assets.iterrows():
            try:
                logging.info("Download - {} ({}/{})".format(asset["Ticker"], index + 1, count_assets))
                ticker = asset["Ticker"].replace("PERP", "").replace("100", "u100")
                asset["LastPrice"] = self.__download_last_price(ticker, self.phemex_client)
                asset["UpdateDate"] = datetime.datetime.now().strftime(self.DATE_TIME_FORMATTER)
                result = pd.concat([result, pd.DataFrame([asset])])
            except:
                logging.exception("Problem with download price for: {}".format(asset["Ticker"]))
                result = pd.concat([result, pd.DataFrame([asset])])

        result.to_csv(self.PHEMEX_FUTURES_CSV, index=False)
        logging.info("Finished downloading price for Phemex futures")

    def download_kucoin_spot_price(self):
        assets = pd.read_csv(self.KUCOIN_SPOT_CSV)

        logging.info("Start downloading price for Kucoin spot")
        count_assets = assets.shape[0]
        result = pd.DataFrame()
        for index, asset in assets.iterrows():
            try:
                logging.info("Download - {} ({}/{})".format(asset["Ticker"], index + 1, count_assets))
                ticker = asset["Ticker"].replace("USDT", "-USDT")
                asset["LastPrice"] = self.__download_last_price(ticker, self.kucoin_client)
                asset["UpdateDate"] = datetime.datetime.now().strftime(self.DATE_TIME_FORMATTER)
                result = pd.concat([result, pd.DataFrame([asset])])
            except:
                logging.exception("Problem with download price for: {}".format(asset["Ticker"]))
                result = pd.concat([result, pd.DataFrame([asset])])

        result.to_csv(self.KUCOIN_SPOT_CSV, index=False)
        logging.info("Finished downloading price for Kucoin spot")

    def download_binance_spot_price(self):
        assets = pd.read_csv(self.BINANCE_SPOT_CSV)

        logging.info("Start downloading price for Binance spot")
        count_assets = assets.shape[0]
        result = pd.DataFrame()
        for index, asset in assets.iterrows():
            try:
                logging.info("Download - {} ({}/{})".format(asset["Ticker"], index + 1, count_assets))
                ticker = asset["Ticker"]
                asset["LastPrice"] = self.__download_last_price(ticker, self.binance_client)
                asset["UpdateDate"] = datetime.datetime.now().strftime(self.DATE_TIME_FORMATTER)
                result = pd.concat([result, pd.DataFrame([asset])])
            except:
                logging.exception("Problem with download price for: {}".format(asset["Ticker"]))
                result = pd.concat([result, pd.DataFrame([asset])])

        result.to_csv(self.BINANCE_SPOT_CSV, index=False)
        logging.info("Finished downloading price for Binance spot")

    def __download_last_price(self, ticker, exchange_client):
        while True:
            try:
                return exchange_client.fetch_ticker(ticker)["last"]
            except RateLimitExceeded:
                logging.warning(
                    "RateLimitExceeded: Too Many Requests on exchange api, app will be sleep {} seconds before recall api."
                    .format(self.rate_exceed_delay_seconds))
                time.sleep(self.rate_exceed_delay_seconds)
