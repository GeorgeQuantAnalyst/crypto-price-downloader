#!/bin/bash
set -e

source venv/bin/activate
python3 -m crypto_price_downloader BybitFutures
libreoffice data/bybit_futures.csv