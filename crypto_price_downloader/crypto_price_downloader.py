import datetime
import logging
import time

import ccxt
import pandas as pd
from ccxt import RateLimitExceeded


class CryptoPriceDownloader:
    PHEMEX_FUTURES_CSV = "data/phemex_futures.csv"
    KUCOIN_SPOT_CSV = "data/kucoin_spot.csv"

    DATE_TIME_FORMATTER = "%d.%m.%Y %X"

    def __init__(self, rate_exceed_delay_seconds):
        self.rate_exceed_delay_seconds = rate_exceed_delay_seconds
        self.phemex_client = ccxt.phemex()
        self.kucoin_client = ccxt.kucoin()

    def download_phemex_futures_price(self):
        assets = pd.read_csv(self.PHEMEX_FUTURES_CSV)

        logging.info("Start downloading price for Phemex futures")
        count_assets = assets.shape[0]
        result = pd.DataFrame()
        for index, asset in assets.iterrows():
            try:
                logging.info("Download - {} ({}/{})".format(asset["Ticker"], index + 1, count_assets))
                ticker = asset["Ticker"].replace("PERP", "").replace("100", "u100")
                asset["LastPrice"] = self.phemex_client.fetch_ticker(ticker)["last"]
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
                asset["LastPrice"] = self.kucoin_client.fetch_ticker(ticker)["last"]
                asset["UpdateDate"] = datetime.datetime.now().strftime(self.DATE_TIME_FORMATTER)
                result = pd.concat([result, pd.DataFrame([asset])])
            except:
                logging.exception("Problem with download price for: {}".format(asset["Ticker"]))
                result = pd.concat([result, pd.DataFrame([asset])])

        result.to_csv(self.KUCOIN_SPOT_CSV, index=False)
        logging.info("Finished downloading price for Kucoin spot")

    def __download_last_price_from_phemex_futures(self, ticker):
        while True:
            try:
                return self.phemex_client.fetch_ticker(ticker)["last"]
            except RateLimitExceeded:
                logging.warning(
                    "RateLimitExceeded: Too Many Requests on exchange api, app will be sleep {} seconds before recall api."
                    .format(self.rate_exceed_delay_seconds))
                time.sleep(self.rate_exceed_delay_seconds)

    def __download_last_price_from_kucoin(self, ticker):
        while True:
            try:
                return self.kucoin_client.fetch_ticker(ticker)["last"]
            except RateLimitExceeded:
                logging.warning(
                    "RateLimitExceeded: Too Many Requests on exchange api, app will be sleep {} seconds before recall api."
                    .format(self.rate_exceed_delay_seconds))
                time.sleep(self.rate_exceed_delay_seconds)
