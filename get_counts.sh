#!/usr/bin/bash

usage="$(basename "$0") [-h] [-l {'fa'|'de'|'fr'|'it'|...}] [-r recreate_count] -- Create n-gram Language Model on ~2.2M Wikipedia articles using KenLM.
where:
    -h  show this help text
    -l input language fa
    -r recreate vocabulary
EXAMPLE USAGE: counting words in the input dataset for the Persian language. USAGE: get_count.sh -l fa -r true
"

# Defaults
language='fa'
target_dir='.'
recreate_count=false


while getopts ":h:l:r" option; do
    case "${option}" in
    h) echo "$usage"
       exit
       ;;
    l) language=$OPTARG
       ;;
    c) recreate_count=true
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

corpus_name="wiki_${language}"
corpus_file="${language}wiki-latest-pages-articles_clean.txt" # uncompressed corpus
lm_counts="${target_dir}/${corpus_name}.counts" # corpus vocabulary with counts (all words)


echo "[INFO] language: $language, recreate_count: $recreate_count, input: $corpus_file, output: $lm_counts"

if ${recreate_count} || ! [ -e ${lm_count} ] ; then
    echo "[INFO] Creating word-count of $corpus_file and saving it in $lm_vocab. "

    echo "[INFO] Counting word occurrences..."
    cat ${corpus_file} |
        pv -s $(stat --printf="%s" ${corpus_file}) | # show progress bar
        sed -e 's/-//g' -e 's/،//g' -e 's/–//g' -e 's/«//g' -e 's/»//g' -e 's/؛//g' -e 's/٬//g' | # remove
#        tr -dc '[:alnum:]\n\r' | # removes special characters including persian
        tr '[:space:]' '[\n*]' | # replace space with newline (one word per line)
        tr -d ' [:alpha:]äöü<>\203' |
        grep -v "^\s*$" | # remove empty lines
        grep -v '#' | # remove words with numbers
        awk 'length($0)>1' | # remove words with length 1, I doesn't count persian characters :)
        sort | uniq -c | sort -bnr > ${lm_counts} # sort alphanumeric, count unique words, then sort result

    echo "[INFO] Successfully generated words and their number of counts to ${lm_counts}!" # writing $top_words top words to vocabulary"
else
  echo "[INFO] word-count ${lm_counts} is already exists & re-create is set to ${recreate_count}!"
fi

