#!/bin/bash
set -e

source venv/bin/activate
python3 -m crypto_price_downloader PhemexFutures
libreoffice data/phemex_futures.csv