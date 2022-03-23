from argparse import ArgumentParser
from tqdm import tqdm

parser = ArgumentParser()
parser.add_argument("--counts", default="wiki_fa.counts")
parser.add_argument("--output", default="kenlm_vocabs.txt")
parser.add_argument("--top-vocabs", type=int, default=80000,
                    help="number of top words that will be chosen. Default is 80k")
parser.add_argument("--ignore-less", type=int, default=25,
                    help="vocabs with less than specified count number will be ignored. Default is 25")

args = parser.parse_args()

# Reading the file
with open(args.counts) as f:
    lines = f.readlines()

top_count = 0
total_count = len(lines)
vocabs = ""

for line in tqdm(lines, desc="number of vocabs", total=args.top_vocabs):
    try:
        count, vocab = line.strip().split(" ")
        # if len(vocab) or it's occurrence count is less than 1 ignore the vocab
        if len(vocab) <= 1 or int(count) < args.ignore_less:
            continue
        vocabs += f"{vocab} "
        top_count += 1
        if top_count > args.top_vocabs:
            print(f"[INFO] Got {args.top_vocabs} vocabs. Exiting...")
            break
    except Exception as e:
        print(f"[ERROR] {e} in line: {str(line)}")
        continue

print(f"[INFO] Number of written words: {top_count}")
print(f"[INFO] Successfully saved vocabs to {args.output}")
with open(args.output, mode='w') as f:
    f.write(vocabs)
