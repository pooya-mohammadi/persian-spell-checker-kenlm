#!/usr/bin/env bash
# set -xe

#!/bin/bash

usage="$(basename "$0") [-h] [-o <int>] [-l {'fa'|'en'|'fr'|'it'|...}] [-d {'probing'|'trie'}] [-t <string> ] [-w <int>]  -- Create n-gram Language Model on Persian Wikipedia articles using KenLM.
where:
    -h  show this help text
    -o  set the order of the model, i.e. the n in n-gram (default: 4)
    -l  ISO 639-1 code of the language to train on (default: fa)
    -d  data structure to use (use 'trie' or 'probing'). See https://kheafield.com/code/kenlm/structures/ for details. (default: trie)
    -t  target directory to write to
    -w  number of vocabs in vocabulary to keep (default: 80,000)

EXAMPLE USAGE: create a 4-gram model for the Persian language using the 80K most frequent vocabs from the Wikipedia articles: bash train_kenlm.sh -l fa -o 4 -w 80000
"

# Defaults
order=4
language='fa'
data_structure=trie
top_words=80000
target_dir='.'
remove_artifacts=false
recreate_vocab=false
tmp_dir='.'


while getopts ":h:o:l:d:t:w:r:v:" option; do
    case "${option}" in
    h) echo "$usage"
       exit
       ;;
    o) order=$OPTARG
       ;;
    l) language=$OPTARG
       ;;
    d) data_structure=$OPTARG
       ;;
    w) top_words=$OPTARG
       ;;
    t) target_dir=$OPTARG
       ;;
    :) printf "missing argument for -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
   \?) printf "illegal option: -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
    esac
done


corpus_name="wiki_${language}_kenlm_vocabs.txt"
corpus_file="${language}wiki-latest-pages-articles_clean.txt" # uncompressed corpus
corpus_bin=${corpus_file}.bz2
#lm_counts="${tmp_dir}/${corpus_name}.counts" # corpus vocabulary with counts (all words)
lm_vocab="${tmp_dir}/${corpus_name}" # corpus vocabulary used for training (most frequent words)
lm_arpa="${tmp_dir}/${language}_wiki.arpa" # ARPA file
lm_binary="${language}_wiki.binary" # ARPA file

echo "[INFO] Parameters: corpus_name: ${corpus_name}, lm_vocab: ${lm_vocab}, corpus_file: ${corpus_file}, corpus_bin: ${corpus_bin}"

echo "[INFO] Compressing ${corpus_file}. File size before:"
du -h ${corpus_file}


if ! [ -e $lm_arpa ]; then
    echo "[INFO] Training $order-gram KenLM model with data from $corpus_file and saving ARPA file to $lm_arpa"
    echo "[INFO] This can take several hours, depending on the order of the model"
    cat ${corpus_file} | kenlm/build/bin/lmplz -o ${order} -T ./tmp  --limit_vocab_file ${lm_vocab} > ${lm_arpa}
    echo "[INFO] Successfully created ${lm_arpa} language model!"
else
  echo "[INFO] ${lm_arpa} already exists! skipping..."
fi

if ! [ -e $lm_binary ]; then
    echo "[INFO] Building binary file from $lm_arpa and saving to $lm_binary"
    echo "[INFO] This should usually not take too much time even for high-order models"
    kenlm/build/bin/build_binary ${data_structure} ${lm_arpa} ${lm_binary}
    echo "[INFO] Successfully created ${lm_binary} binary language model!"
else
  echo "[INFO] ${lm_binary} already exists! skipping..."
fi