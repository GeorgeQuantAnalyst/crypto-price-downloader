# Crypto price downloader

Application for downloading current cryptocurrency prices from exchanges defined in Excel for further use in other applications.

* Supported exchanges:
  * Phemex
  * Kucoin

![Example](images/example.png)
## How to build
```bash
./build.sh
```

## How to deploy
```
./deploy.sh
```

## How to prepare
```bash
./prepare.sh
```

## How to run
```bash
./phemex_futures_price_download.sh
./kucoin_spot_price_download.sh
```

## Technologies
* Python 3
* Pandas
* CCXT
