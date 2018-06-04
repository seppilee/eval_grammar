#!/usr/bin/python
#-*- coding: UTF-8 -*-

import sys
import re
import codecs
from itertools import izip
import glob

#utf-8 encoding for python2
reload(sys)
sys.setdefaultencoding("UTF-8")


line_num = 0
char_length = 0
sum_char_length = 0
char_lengths = []
threshold = 150

def count_letters(word):
    return len(filter(lambda x: x not in " ", word))

for line in sys.stdin:
    line = re.sub("\r|\n|\uFEFF", "", line)
    char_length = len(line.decode('utf8')) - line.count(' ')
    line_num += 1
    sum_char_length += char_length
    char_lengths.append(char_length)

    if line_num % 10000 == 0 :
        print "processing:", line_num
    #print line, "\t", char_length

print "total lines:", line_num, "\tmean length:", sum_char_length/line_num, "\tmax length:", max(char_lengths)
print "long sentences:",len([x for x in char_lengths if x >= threshold])
