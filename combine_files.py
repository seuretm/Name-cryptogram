from tqdm import tqdm
import re
import pickle
import os
import argparse
from random import shuffle

max_missing_chars = 1
max_extra_chars = 10

parser = argparse.ArgumentParser()
parser.add_argument("base")
parser.add_argument("input1")
parser.add_argument("input2")
parser.add_argument("output")
args = parser.parse_args()

base = args.base
desired_length = len(base)

def get_count(name):
    count = [0 for x in range(256)]
    for x in name.lower():
        if x in (' ', ',', '.', '\n', '-', '!', '"', '~', '\'', '/'):
            continue
        c = ord(x)
        if c<0 or c>256:
            return None
        count[c] += 1
    count[32] = 0
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


place_map = {}
if os.path.exists('input1.dat'):
    with open('input1.dat', 'rb') as f:
        place_map = pickle.load(f)
else:
    for line in tqdm(open(args.input1, 'rt')):
        name = line.strip()
        if len(name)>25 or len(name)<6:
            continue
        count = get_count(name)
        code = ''
        for i in count:
            if i>0:
                code = '%s,%d' % (code, i)
            else:
                code = '%s,' % code
        if not code in place_map:
            s = 0
            for x in count:
                s += x
            place_map[code] = (count, set(), s)
        place_map[code][1].add(name)
    with open('input1.dat', 'wb') as f:
        pickle.dump(place_map, f)
print(len(place_map),'input1 values to process')

name_map = {}
if os.path.exists('input2.dat'):
    with open('input2.dat', 'rb') as f:
        name_map = pickle.load(f)
else:
    for line in tqdm(open(args.input2, 'rt')):
        name = re.sub('^[0-9]* [0-9]* ', '', line.strip())
        count = get_count(name)
        code = ''
        for i in count:
            if i>0:
                code = '%s,%d' % (code, i)
            else:
                code = '%s,' % code
        if not code in name_map:
            s = 0
            for x in count:
                s += x
            name_map[code] = (count, set(), s)
        name_map[code][1].add(name)
    with open('input2.dat', 'wb') as f:
        pickle.dump(name_map, f)
print(len(name_map),'input2 values to process')

comb_count = get_count(base) # will be overwritten
if True:
    count = [0 for x in range(256)]
    for key in name_map:
        x = name_map[key][0]
        for i in range(256):
            count[i] += x[i]
    for key in place_map:
        x = place_map[key][0]
        for i in range(256):
            count[i] += x[i]
    b = 0
    a = 256
    for i in range(0, 255):
        if count[i]>0:
            b = i+1
    for i in range(255, 0, -1):
        if count[i]>0:
            a = i-1
    b = min(b, 128)
    print('Keeping codes in [%d, %d]' % (a, b))
    
    
    for key in name_map:
        name_map[key] = (name_map[key][0][a:b], name_map[key][1], name_map[key][2])
    for key in place_map:
        place_map[key] = (place_map[key][0][a:b], place_map[key][1], place_map[key][2])
    base_count = base_count[a:b]
    comb_count = [0 for i in range(b-a)]
name_list = []
for person_code in name_map:
    name_list.append(person_code)
shuffle(name_list)

checked = set()
if os.path.exists('checked.set'):
    with open('checked.set', 'rb') as f:
        checked = pickle.load(f)
with open(args.output, 'at') as out:
    n = 0
    for person_code in tqdm(name_map):
        if person_code in checked:
            continue
        a = name_map[person_code][0]
        cnt = name_map[person_code][2]
        for place_code in tqdm(place_map):
            if abs(place_map[place_code][2]+cnt-53)>max_extra_chars:
                continue
            b = place_map[place_code][0]
            for i in range(len(a)):
                comb_count[i] = a[i] + b[i]
            res = compare(base_count, comb_count)
            if res[0]>max_missing_chars or res[1]>max_extra_chars:
                continue
            for name in name_map[person_code][1]:
                for place in place_map[place_code][1]:
                    out.write('%d %d %d %s:%s\n' % (res[0]+res[1], res[0], res[1], name, place))
            out.flush()
            print('%d %d %d %s:%s\n' % (res[0]+res[1], res[0], res[1], name, place))
        checked.add(person_code)
        
        n += 1
        if n % 100 == 0:
            with open('checked.set', 'wb') as f:
                pickle.dump(checked, f)
