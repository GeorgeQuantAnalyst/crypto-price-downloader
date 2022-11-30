import datetime
import logging
import time

import ccxt
import pandas as pd
import yfinance as yf
from ccxt import RateLimitExceeded, Exchange


class CryptoPriceDownloader:
    PHEMEX_FUTURES_CSV = "data/phemex_futures.csv"
    KUCOIN_SPOT_CSV = "data/kucoin_spot.csv"
    BINANCE_SPOT_CSV = "data/binance_spot.csv"
    OKX_SPOT_CSV = "data/okx_spot.csv"
    SIMPLEFX_CFD_CSV = "data/simplefx_cfd.csv"
    BYBIT_FUTURES_CSV = "data/bybit_futures.csv"

    DATE_TIME_FORMATTER = "%d.%m.%Y %X"

    def __init__(self, rate_exceed_delay_seconds):
        self.rate_exceed_delay_seconds = rate_exceed_delay_seconds
        self.phemex_client = ccxt.phemex()
        self.kucoin_client = ccxt.kucoin()
        self.binance_client = ccxt.binance()
        self.okx_client = ccxt.okx()
        self.bybit_client = ccxt.bybit()

    def download_phemex_futures_price(self) -> None:
        assets = pd.read_csv(self.PHEMEX_FUTURES_CSV)

        logging.info("Start downloading price for Phemex futures")
        count_assets = assets.shape[0]
        result = []
        for index, asset in assets.iterrows():
            try:
                logging.info("Download - {} ({}/{})".format(asset["ticker"], index + 1, count_assets))
                ticker = asset["ticker"]
                asset["last_price"] = self.__download_last_price(ticker, self.phemex_client)
                asset["update_date"] = datetime.datetime.now().strftime(self.DATE_TIME_FORMATTER)
                result.append(asset.to_dict())
            except:
                logging.exception("Problem with download price for: {}".format(asset["ticker"]))
                result.append(asset.to_dict())

        pd.DataFrame(result).to_csv(self.PHEMEX_FUTURES_CSV, index=False)
        logging.info("Finished downloading price for Phemex futures")

    def download_kucoin_spot_price(self) -> None:
        assets = pd.read_csv(self.KUCOIN_SPOT_CSV)

        logging.info("Start downloading price for Kucoin spot")
        count_assets = assets.shape[0]
        result = []
        for index, asset in assets.iterrows():
            try:
                logging.info("Download - {} ({}/{})".format(asset["Ticker"], index + 1, count_assets))
                ticker = asset["Ticker"].replace("USDT", "-USDT")
                asset["LastPrice"] = self.__download_last_price(ticker, self.kucoin_client)
                asset["UpdateDate"] = datetime.datetime.now().strftime(self.DATE_TIME_FORMATTER)
                result.append(asset.to_dict())
            except:
                logging.exception("Problem with download price for: {}".format(asset["Ticker"]))
                result.append(asset.to_dict())

        pd.DataFrame(result).to_csv(self.KUCOIN_SPOT_CSV, index=False)
        logging.info("Finished downloading price for Kucoin spot")

    def download_binance_spot_price(self) -> None:
        assets = pd.read_csv(self.BINANCE_SPOT_CSV)

        logging.info("Start downloading price for Binance spot")
        count_assets = assets.shape[0]
        result = []
        for index, asset in assets.iterrows():
            try:
                logging.info("Download - {} ({}/{})".format(asset["Ticker"], index + 1, count_assets))
                ticker = asset["Ticker"]
                asset["LastPrice"] = self.__download_last_price(ticker, self.binance_client)
                asset["UpdateDate"] = datetime.datetime.now().strftime(self.DATE_TIME_FORMATTER)
                result.append(asset.to_dict())
            except:
                logging.exception("Problem with download price for: {}".format(asset["Ticker"]))
                result.append(asset.to_dict())

        pd.DataFrame(result).to_csv(self.BINANCE_SPOT_CSV, index=False)
        logging.info("Finished downloading price for Binance spot")

    def download_okx_spot_price(self) -> None:
        assets = pd.read_csv(self.OKX_SPOT_CSV)

        logging.info("Start downloading price for Okx spot")
        count_assets = assets.shape[0]
        result = []

        for index, asset in assets.iterrows():
            try:
                logging.info("Download - {} ({}/{})".format(asset["Ticker"], index + 1, count_assets))
                ticker = asset["Ticker"].replace("USDT", "-USDT")
                asset["LastPrice"] = self.__download_last_price(ticker, self.okx_client)
                asset["UpdateDate"] = datetime.datetime.now().strftime(self.DATE_TIME_FORMATTER)
                result.append(asset.to_dict())
            except:
                logging.exception("Problem with download price for: {}".format(asset["Ticker"]))
                result.append(asset.to_dict())

        pd.DataFrame(result).to_csv(self.OKX_SPOT_CSV, index=False)
        logging.info("Finished downloading price for OKx spot")

    def download_simple_fx_cfd_price(self) -> None:
        assets = pd.read_csv(self.SIMPLEFX_CFD_CSV)

        logging.info("Start downloading price for SimpleFx cfd")
        count_assets = assets.shape[0]
        result = []

        for index, asset in assets.iterrows():
            try:
                logging.info("Download - {} ({}/{})".format(asset["Ticker"], index + 1, count_assets))
                ticker = asset["Ticker"]
                asset["LastPrice"] = round(yf.Ticker(ticker).history("1d")["Close"][0], 2)
                asset["UpdateDate"] = datetime.datetime.now().strftime(self.DATE_TIME_FORMATTER)
                result.append(asset.to_dict())
            except:
                logging.exception("Problem with download price for: {}".format(asset["Ticker"]))
                result.append(asset.to_dict())

        pd.DataFrame(result).to_csv(self.SIMPLEFX_CFD_CSV, index=False)
        logging.info("Finished downloading price for SimpleFx cfd")

    def download_bybit_futures_price(self) -> None:
        assets = pd.read_csv(self.BYBIT_FUTURES_CSV)

        logging.info("Start downloading price for Bybit futures")
        count_assets = assets.shape[0]
        result = []
        for index, asset in assets.iterrows():
            try:
                logging.info("Download - {} ({}/{})".format(asset["ticker"], index + 1, count_assets))
                ticker = asset["ticker"]
                asset["last_price"] = self.__download_last_price(ticker, self.bybit_client)
                asset["update_date"] = datetime.datetime.now().strftime(self.DATE_TIME_FORMATTER)
                result.append(asset.to_dict())
            except:
                logging.exception("Problem with download price for: {}".format(asset["ticker"]))
                result.append(asset.to_dict())

        pd.DataFrame(result).to_csv(self.BYBIT_FUTURES_CSV, index=False)
        logging.info("Finished downloading price for Bybit futures")

    def __download_last_price(self, ticker: str, exchange_client: Exchange) -> float:
        while True:
            try:
                return exchange_client.fetch_ticker(ticker)["last"]
            except RateLimitExceeded:
                logging.warning(
                    "RateLimitExceeded: Too Many Requests on exchange api, app will be sleep {} seconds before recall api."
                    .format(self.rate_exceed_delay_seconds))
                time.sleep(self.rate_exceed_delay_seconds)
