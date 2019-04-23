#!/usr/bin/python
#-*- coding: UTF-8 -*-

from collections import defaultdict
import sys, re

def ngrams(words, n=2, padding=False):
    "Compute n-grams with optional padding"
    pad = [] if not padding else [None]*(n-1)
    grams = pad + words + pad
    return (tuple(grams[i:i+n]) for i in range(0, len(grams) - (n - 1)))

# grab n-grams
words = []
for line in sys.stdin:
    line = re.sub("\r|\n|\uFEFF|[-',!?‘’\".“~`…<>‥\[\]]|\s$", "", line)
    line = re.sub("[ㆍ·]", " ", line)
    word = line.split(" ")
    words.extend(word)

#words = ['the','cat','sat','on','the','dog','on','the','cat']
for size, padding in ((3, 0), (4, 0), (2, 1)):
    #print ('\n%d-grams padding=%d' % (size, padding))
    list(ngrams(words, size, padding))

# show frequency
counts = defaultdict(int)
for ng in ngrams(words, 2, False):
    counts[ng] += 1

print ('\nfrequencies of bigrams:')
for c, ng in sorted(((c, ng) for ng, c in counts.items()), reverse=True):
    print (" ".join(ng), c)


