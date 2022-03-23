import re
import string
from argparse import ArgumentParser
from hazm import sent_tokenize, word_tokenize, Normalizer
from tqdm import tqdm
from multiprocessing import Pool

parser = ArgumentParser()
parser.add_argument("--corpus-path", default="fawiki-latest-pages-articles_preprocessed.txt")
parser.add_argument("--corpus-clean", default="fawiki-latest-pages-articles_clean.txt")
parser.add_argument("--language", type=str, default="fa")
parser.add_argument("--min-words", type=int, default=3)
parser.add_argument("--n-workers", type=int, default=12)

args = parser.parse_args()


def main():
    count = 0
    pool = Pool(processes=args.n_workers)
    objects = []
    lines = open(args.corpus_path, mode='r').readlines()
    print(f"[INFO] Start preprocessing {args.corpus_path}, result is saved in {args.corpus_clean}")

    for line in tqdm(lines, desc='applying cleaning jobs:'):
        obj = pool.apply_async(process_line, (line, args.min_words))
        objects.append(obj)
    with open(args.corpus_clean, mode='w') as file:
        for obj in tqdm(objects, desc='processing cleaning jobs:'):
            sentences = obj.get()
            for sentence in sentences:
                if sentence:
                    file.write(sentence + "\n")
                    count += 1
    print(f'[INFO] Successfully cleaned {count} sentences.')


def process_line(line, min_words):
    sentences = []
    sents = sent_tokenize(line.strip())
    for sentence in sents:
        sentence_processed = process_sentence(sentence, min_words)
        if sentence_processed:
            sentences.append(sentence_processed)
    return sentences


def process_sentence(sent, min_words):
    words = [normalize_word(word) for word in word_tokenize(sent)]
    if len(words) >= min_words:
        return ' '.join(w for w in words if w).strip()  # prevent multiple spaces
    return ''


def clean_html(text):
    pattern = re.compile('<.*?>')
    return re.sub(pattern, '', text)


def cleaning(text):
    text = text.strip()
    text = clean_html(text)
    normalizer = Normalizer()
    text = normalizer.normalize(text)

    # removing wierd patterns
    wierd_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u'\U00010000-\U0010ffff'
                               u"\u200d"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\u3030"
                               u"\ufe0f"
                               u"\u2069"
                               u"\u2066"
                               # u"\u200c"
                               u"\u2068"
                               u"\u2067"
                               "]+", flags=re.UNICODE)

    text = wierd_pattern.sub(r'', text)

    # removing extra spaces, hashtags
    text = re.sub("#", "", text)
    text = re.sub("\s+", " ", text)
    return text


def normalize_word(token):
    _token = cleaning(token)
    _token = remove_punctuation(_token)  # remove any special chars
    _token = replace_other_lang(_token)
    _token = replace_numeric(_token, by_single_digit=True)
    _token = '<num>' if _token == '#' else _token  # if token was a number, replace it with <unk> token
    return _token.strip().lower()


def replace_other_lang(text, repl="<non-lang>"):
    alpha_pattern = re.compile('[a-z]+|[A-Z]')
    return re.sub(alpha_pattern, repl, text)


def remove_punctuation(text, punctiation_extended=string.punctuation + """"„“‚‘.٫ٔ"""):
    return ''.join(c for c in text if c not in punctiation_extended)


def replace_numeric(text, numeric_pattern=re.compile('[۰۱۲۳۴۵۶۷۸۹]+|٫'), digit_pattern=re.compile('[.-۹]|٫'),
                    repl='#', by_single_digit=False):
    return re.sub(numeric_pattern, repl, text) if by_single_digit else re.sub(digit_pattern, repl, text)


def contains_numeric(text):
    return any(char.isdigit() for char in text)


# def unidecode_keep_umlauts(text):
#     # modified version from unidecode.unidecode_expect_ascii that does not replace umlauts
#     # _warn_if_not_unicode(text)
#     try:
#         bytestring = text.encode('ASCII')
#     except UnicodeEncodeError:
#         return _unidecode_keep_umlauts(text)
#     if version_info[0] >= 3:
#         return text
#     else:
#         return bytestring


# def _unidecode_keep_umlauts(text):
#     # modified version from unidecode._unidecode that keeps umlauts
#     retval = []
#
#     for char in text:
#         codepoint = ord(char)
#
#         # Basic ASCII, ä/Ä, ö/Ö, ü/Ü
#         if codepoint < 0x80 or codepoint in [0xe4, 0xc4, 0xf6, 0xd6, 0xfc, 0xdc]:
#             retval.append(str(char))
#             continue
#
#         if codepoint > 0xeffff:
#             continue  # Characters in Private Use Area and above are ignored
#
#         if 0xd800 <= codepoint <= 0xdfff:
#             warnings.warn("Surrogate character %r will be ignored. "
#                           "You might be using a narrow Python build." % (char,),
#                           RuntimeWarning, 2)
#
#         section = codepoint >> 8  # Chop off the last two hex digits
#         position = codepoint % 256  # Last two hex digits
#
#         try:
#             table = Cache[section]
#         except KeyError:
#             try:
#                 mod = __import__('unidecode.x%03x' % (section), globals(), locals(), ['data'])
#             except ImportError:
#                 Cache[section] = None
#                 continue  # No match: ignore this character and carry on.
#
#             Cache[section] = table = mod.data
#
#         if table and len(table) > position:
#             retval.append(table[position])
#
#     return ''.join(retval)


if __name__ == '__main__':
    main()
