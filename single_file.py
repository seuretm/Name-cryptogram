from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("base")
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()

base = args.base

def get_count(name):
    codesize = 256
    count = [0 for x in range(codesize)]
    for x in name.lower():
        if x in (' ', ',', '.', '\n', '-', '!', '"', '~'):
            continue
        c = ord(x)
        if c<0 or c>=codesize:
            return None
        count[c] += 1
    count[255] = 0
    count[ord('u')] += count[ord('v')]
    count[ord('v')] = 0
    count[ord('i')] += count[ord('j')] + count[ord('y')]
    count[ord('j')] = 0
    count[ord('y')] = 0
    return count

def compare(base, count):
    missing = 0
    extra = 0
    for i in range(len(base)):
        missing += max(0, count[i] - base[i]) # how many chars are missing from the base string
        extra   += max(0, base[i] - count[i]) # how many chars in the base string are not used
    return (missing, extra)

base_count = get_count(base)

pos = 0
with open(args.output, 'wt') as out:
    lst = [x for x in open(args.input, 'rt')]
    for name in tqdm(lst):
        pos += 1
        name_count = get_count(name)
        if name_count is None:
            continue
        res = compare(base_count, name_count)
        if res[0]>0: # ignore names missing more than 0 chars
            continue
        out.write('%s' % name)
