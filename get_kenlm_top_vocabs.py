from argparse import ArgumentParser
from tqdm import tqdm

parser = ArgumentParser()
parser.add_argument("--counts", default="wiki_fa.counts")
parser.add_argument("--vocab", default="wiki_fa.vocab")
parser.add_argument("--top-words", type=int, default=80000,
                    help="number of top words that will be chosen. Default is 80k")
parser.add_argument("--ignore-less", type=int, default=50,
                    help="vocabs with less than specified count number will be ignored. Default is 50")
parser.add_argument("--include-counts", action='store_true', help="Whether to include the counts")

args = parser.parse_args()

# Reading the file
with open(args.counts) as f:
    lines = f.readlines()

top_count = 0
total_count = len(lines)
vocabs = ""

for line in tqdm(lines, desc="number of vocabs", total=args.top_words):
    try:
        count, vocab = line.strip().split(" ")
        # if len(vocab) or its count is less than 1
        if len(vocab) <= 1 or int(count) < args.ignore_less:
            continue
        if args.include_counts:
            vocabs += f"{vocab} {count}\n"
            top_count += 1
        else:
            vocabs += f"{vocab} "
            top_count += 1
        if top_count > args.top_words:
            print(f"[INFO] Got {args.top_words}. Exiting...")
            break
    except ValueError:
        print(f"[ERROR] line: {line}")
        continue
print(f"[INFO] Number of written words: {top_count}")
print(f"[INFO] writing vocabs to {args.vocab}")
with open(args.vocab, mode='w') as f:
    f.write(vocabs)
