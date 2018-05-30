#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
import random

replacement_patterns = []
matched_num = 1


with open('aspell_dict', 'r') as f:
    for line in f:
            line.decode(encoding = "UTF-8")
            strs = line.rstrip('\r\n')
            pair = tuple(strs.split("\t"))
            replacement_patterns.append(pair)

class RegexpReplacer(object):

    def __init__(self, patterns=replacement_patterns):
        self.patterns = [(re.compile(regex), repl) for (repl, regex) in patterns]

    def replace(self, text):
        s = text
        matched = 0
        random.shuffle(self.patterns)  #shuffle pattern lists
        for (patt, repl) in self.patterns:
            if re.search(patt, s) and matched < matched_num:
                s = re.sub(patt, repl, s)
                #s = re.sub(patt, patt.pattern+"("+repl+")", s)
                matched += 1
        return s

reg = RegexpReplacer()
for line in sys.stdin:
        line.decode(encoding = "UTF-8")
        in_token=line.rstrip('\r\n')
        if in_token != reg.replace(in_token):
            print reg.replace(in_token), "\t", in_token

