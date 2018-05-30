#!/usr/bin/python
#-*- coding: UTF-8 -*-

from itertools import izip
import glob

file1l =[]
file2l =[]

file1l = glob.glob("*.ko")
file2l = glob.glob("*.en")

file1l.sort()
file2l.sort()


def count_letters(word):
    return len(filter(lambda x: x not in " ", word))

i = 0
while i < (len(file1l)):
    with open(file1l[i]) as textfile1, open(file2l[i]) as textfile2:
        for x, y in izip(textfile1, textfile2):
            x.rstrip()
            y.rstrip()
            print "%s\t%s" % (count_letters(x), len(y.decode('utf8')))
    i += 1
