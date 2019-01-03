#!/usr/bin/python
#-*- coding: UTF-8 -*-

import sys
import re

reload(sys)
sys.setdefaultencoding("UTF-8")

cnt = 0
vocab = {}
pl_tgt = {}
words = []

def bpe_code(word, ngram):
    words = list(word)
    middleIndex = len(words)/2
    words.insert(middleIndex, " ")
    #print "".join(words)
    for i in range(0,len(words)-1):
        print words[i], words[i+1], "\n", words[i] + words[i+1]
    return

for line in sys.stdin:
        line = line.decode("UTF-8")
        line = line.strip('\r\n ')
        vocab[line] = len(line)
for key, value in sorted(vocab.items(), key=lambda x: x[1]):
    if value == 2:
        continue
        #print " ".join(list(key.decode("UTF-8"))), value
    elif value == 5:
        #print " ".join(list(key.decode("UTF-8"))), value
         bpe_code(key, value)
    else:
        continue
