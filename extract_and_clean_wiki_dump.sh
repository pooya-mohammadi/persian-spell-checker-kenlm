#!/bin/sh
set -e

WIKI_DUMP_FILE_IN=$1
if [ -z "$2" ]; then N_PROCESSORS=$2; else N_PROCESSORS=4; fi

WIKI_DUMP_FILE_OUT=${WIKI_DUMP_FILE_IN%%.*}.txt

# install wiki-extractor
echo "[INFO] Installing wikiextractor"
pip install wikiextractor

# clone the WikiExtractor repository
echo "[INFO] cloning wikiextractor!"
if [[ -d wikiextractor ]]; then
  echo "[INFO] WikiExtractor already exists! skipping ..."
else
  git clone https://github.com/attardi/wikiextractor.git
fi

# extract and clean the chosen Wikipedia dump
echo "[INFO] Extracting and cleaning $WIKI_DUMP_FILE_IN to $WIKI_DUMP_FILE_OUT..."
cd wikiextractor
python3 -m wikiextractor.WikiExtractor  ../$WIKI_DUMP_FILE_IN --processes $N_PROCESSORS -o -\
| sed "/^\s*\$/d" \
| grep -v "^<doc id=" \
| grep -v "</doc>\$" \
> ../$WIKI_DUMP_FILE_OUT

echo "[INFO] Successfully extracted and cleaned $WIKI_DUMP_FILE_IN to $WIKI_DUMP_FILE_OUT"
