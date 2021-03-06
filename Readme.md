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
input_term = "??????????"  # misspelling of "??????????" It's a city name!

# lookup the dictionary
suggestions = sym_spell.lookup(input_term, Verbosity.ALL, max_edit_distance=2)
# display suggestion term, term frequency, and edit distance
for suggestion in suggestions[:5]:
    print(suggestion)
```
The output is as follows. As you can see `??????????` is correctly chosen!

```commandline
??????????, 1, 4692
??????????, 1, 1350
??????????, 1, 651
??????????, 1, 305
??????????, 1, 225
```

### Get top frequent vocabs for KenLM
Using the following code, top most frequent 80K samples is written to `kenlm_vocabs.txt`. To make it faster vocabs with
less than 25 occurrences are discarded!  
```
python get_kenlm_top_vocabs.py --top-vocabs 80000 --ignore-less 25 --output wiki_fa_kenlm_vocabs.txt
```

### Train KenLM model
First install the KenLM requirements using the following commands:

```commandline
sudo apt-get update
sudo apt-get install cmake build-essential libssl-dev libeigen3-dev libboost-all-dev zlib1g-dev libbz2-dev liblzma-dev -y
```
Then `clone` and make the c++ modules:
```commandline
git clone https://github.com/kpu/kenlm.git
cd kenlm
mkdir -p build
cd build
cmake ..
make -j 4
```

If everything goes fine, you can find `lmplz` and `build_binary` under the `./kenlm/build/bin` directory. Eventually, 
train `kenlm` language model using following bash script.
```
bash train_kenlm.sh -o 4 -l fa
```

Note: the binary module is also created because it's much faster than the non-binarized one.

### Kenlm Inference on python
Install KenLm:
```commandline
pip install https://github.com/kpu/kenlm/archive/master.zip
```

How to use it:
```commandline
import kenlm

model = kenlm.Model('fa_wiki.binary')
print("score: ", model.score('???????? ?????????? ?????? ??????????', bos=True, eos=True))
print("score: ", model.score('???????? ?????????? ?????? ??????????', bos=True, eos=True))
# score:  -11.683658599853516
# score:  -15.572178840637207
```
For more examples check out the following link: https://github.com/kpu/kenlm/blob/master/python/example.py

## References
1. https://github.com/tiefenauer/wiki-lm
2. https://towardsdatascience.com/pre-processing-a-wikipedia-dump-for-nlp-model-training-a-write-up-3b9176fdf67
3. https://github.com/kpu/kenlm
