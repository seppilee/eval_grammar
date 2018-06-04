#!/usr/bin/env python
#-*- coding: UTF-8 -*-
#from __future__ import print_function

import sys
import re
import codecs


#utf-8 encoding for python2
reload(sys)
sys.setdefaultencoding("UTF-8")


def count_letters(word):
    return len(filter(lambda x: x not in " ", word))


def mean_char(n):
    return reduce(lambda x, y: x+y, n) /len(n)


num_sr_count = []
num_tr_count = []


line_number = 0
sum_chars1 = 0
sum_chars2 = 0

for x in sys.stdin:
    x.decode(encoding = "UTF-8")
    x.rstrip('\r\n')
    parts =x.split('\t')
    line_char1 = count_letters(parts[0])
    # num_sr_count.append(int(sr_count)) # into array

    #line_char1 = len(parts[0].decode('utf8'))
    line_char2 = len(parts[1].decode('utf8'))
    sum_chars1 += line_char1
    sum_chars2 += line_char2
    line_number += 1

    mean_line1 = float(sum_chars1/line_number)
    mean_line2 = float(sum_chars2/line_number)

    if line_number % 10000 == 0 :
        print line_number
    #num_tr_count.append(int(tr_count))

    # print "%s\t%s" % (count_letters(parts[0]), len(parts[1].decode('utf8')))

# print mean_char(num_sr_count), ":",
print mean_line1, ":",  mean_line2, "ratio", mean_line1/mean_line2
