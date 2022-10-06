#!/bin/bash
set -e

source venv/bin/activate
python3 -m crypto_price_downloader BinanceSpot
libreoffice data/binance_spot.csv