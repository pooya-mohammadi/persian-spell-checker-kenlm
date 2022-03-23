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

### Get the word-count of the corpus 
Using this script the corpus words will be counted. Before that some extra normalization and cleaning will be applied to the words as well.
```commandline
sudo apt-get install pv
bash get_counts.sh 
```

### Get top frequent vocabs for SymSpell[Spell-Checker]
Symspell needs a text file that contains vocabs and their occurrence. `fa_wiki.counts` that created in the
`Get the word-count of the corpus` section should be trimmed to only contain the 80k top frequent words and
prevent those that have lower frequency than 50.
```terminal
python get_spellchecker_top_vocabs.py --top-vocabs 80000 --ignore-less 25 --output wiki_fa_80k.txt 
```

### Symspell
Symspell is a simple spell checker. First, install it from pypi using the following command:
```commandline
pip install symspellpy
```
For using it, just instantiate it with the vocab dictionary we created in the `Get top frequent vocabs for SymSpell` section
```python
# import symspell
from symspellpy import SymSpell, Verbosity

# instantiate it
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = "wiki_fa_80k.txt"
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

# input sample:
input_term = "اهوار"  # misspelling of "اهواز" It's a city name!

# lookup the dictionary
suggestions = sym_spell.lookup(input_term, Verbosity.ALL, max_edit_distance=2)
# display suggestion term, term frequency, and edit distance
for suggestion in suggestions[:5]:
    print(suggestion)
```
The output is as follows. As you can see `اهواز` is correctly chosen!

```commandline
اهواز, 1, 4692
ادوار, 1, 1350
الوار, 1, 651
انوار, 1, 305
اهورا, 1, 225
```

### Get top frequent vocabs for KenLM
Using the following code, top most frequent 80K samples is written to `wiki_fa.vocab`. To make it faster words with
less than 25 occurrence are discarded!  
```
python get_top_words.py --top-words 80000 --ignore-less 25
```

## Train the model
`bash train_kenlm.sh -o 4 -l fa`


# Inference
`python inference.py`

## References
1. https://github.com/tiefenauer/wiki-lm
2. https://towardsdatascience.com/pre-processing-a-wikipedia-dump-for-nlp-model-training-a-write-up-3b9176fdf67

