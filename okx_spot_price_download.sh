#!/bin/bash
set -e

source venv/bin/activate
python3 -m crypto_price_downloader Okx
libreoffice data/okx_spot.csv