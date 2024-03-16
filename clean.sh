#!/bin/bash
# Go to the script folder
cd "$(dirname "$0")"

# Get the app environment variables
source .env

rm ./*.log
rm ./*.xml
rm -rf ./representation
rm -rf ./$LOG_DIR