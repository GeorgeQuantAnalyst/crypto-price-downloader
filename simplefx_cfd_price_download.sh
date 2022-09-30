#!/bin/bash

source venv/bin/activate
python3 -m crypto_price_downloader SimpleFx
libreoffice data/simplefx_cfd.csv