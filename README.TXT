These programs were written to try answering to the following problem:
https://twitter.com/ad_astra_1/status/1147076593413701632

The problem is as follows: the author name of a book is written as
aaabcdeeeeffgghhhhiiklnnnnnnooooooorrrrrrrsssssttuuuu
Who is the author?

We can make the following hypothesis: the author sorted the letters of
his name, and maybe something else, such as a place or a title. Thus,
if we can find a name or a combination of a name and a place corres-
ponding to this sequence of characters, then we might have found the
author of the book.

The two programs are:
- single_file.py: processes a single list of names or places to match
- combine_files.py: combines all text lines of two files together and
  matches all combinations (so, if the files contain respectively X and
  Y lines, there will be X*Y comparisons)

Two metrics are used:
- the number of missing characters in the base string (aaabc...)
- the number of extra-characters in the base string
A perfect match would have 0 for both measurements.

single_file.py will look for matches with 0 missing characters in the
base string, while combine_files.py has thresholds for both values. The
thresholds can be modified at the beginning of the source code.

So far, no perfect match for the sequence of letters above has been
found.

Technical details:
- Examples of script use are given in example.sh
- Important: if you change the input files for combine_files.py, then
  delete *.set and *.dat !
- You need python3 (who still uses python2 ?!)
- You need the tqdm and argparse packages
