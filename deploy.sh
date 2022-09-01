#!/bin/bash

# Constants
VERSION=$1
PACKAGE_NAME="phemex-futures-price-downloader-$VERSION.tar.gz"
APP_PACKAGE_FOLDER="dist"
APP_FOLDER="$HOME/App/phemex-price-downloader"

echo "Start deploy app: $PACKAGE_NAME to $APP_FOLDER"
rm -rf "$APP_FOLDER/phemex-futures-price-downloader-$VERSION"
mkdir -p $APP_FOLDER
cp "$APP_PACKAGE_FOLDER/$PACKAGE_NAME" "$APP_FOLDER"
cd "$APP_FOLDER" || exit 1
tar -xvzf "$PACKAGE_NAME"
echo "Finished deploy app"