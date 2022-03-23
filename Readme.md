# Download Persian Wiki-Dump, Train Kenlm & Spell Checker

In this project, I download persian wiki-dump dataset from wikipedia, preprocess it and finally train a spell checker and a kenlm language model.

## Download & preprocessing Persian Wiki-Dump 

### Download Persian wiki-Dump  
Download the persian wiki dump using the following bash script. The size of the dataset is about 1G so have patience!

**Note**: If you live in Iran, most surely you do because this repo is for the Persian language, turn on your vpn!

```
language=fa
bash download_wiki_dump.sh $language
```

### Extract TXT
Extract and convert `.bz2` format to `.txt`. Using `wikiextractor` the dump is cleaned and converted `.txt` file. This may take some time as well!

```
n_processors=16
bash extract_and_clean_wiki_dump.sh ${language}wiki-latest-pages-articles.xml.bz2 $n_processors
```

**Note**: In case of a pdb error, change the `expand_templates=True` variable to `expand_templates=False` which is an
input argument to the `clean_text` function located in around line 948 of wikiextractor/wikiextractor/extract.py.   

### Preprocessing and normalization
The output text should be preprocessed and normalized to remove unnecessary texts like "[doc]" and normalize the texts using `hazm` and `nltk` libraries! 

#### Install python requirements:
Install the requirements:
```
pip install -r requirements.txt
```

#### preprocess and normalize
Main Processing. It may take some time!
```
python preprocess_wiki_dump.py fawiki-latest-pages-articles.txt
python cleaner.py
```

## Get counts from corpus
`bash get_counts.sh -l fa -o 4 -c true`

## Get Top words
`python writing_top_words.py --top-words 80000 --ignore-less 25`


## Train the model
`bash train_kenlm.sh -o 4 -l fa`

# Inference
`python inference.py`

## References
1. https://github.com/tiefenauer/wiki-lm
2. https://towardsdatascience.com/pre-processing-a-wikipedia-dump-for-nlp-model-training-a-write-up-3b9176fdf67

