#!/usr/bin/python
#-*- coding: UTF-8 -*-
"""
edit distace tagging 
INPUT: I'm not good witn english       I'm not good with english
OUTPUT: I ' m _ n o t _ g o o d _ w i t n _ e n g l i s h       I ' m _ n o t _ g o o d _ w i t <del> n </del> <ins> h </ins> _ e n g l i s h 
"""

import re
import sys
from difflib import SequenceMatcher
reload(sys)
sys.setdefaultencoding("UTF-8")

INS_START_SYM = "<ins>"
INS_END_SYM = "</ins>"
DEL_START_SYM = "<del>"
DEL_END_SYM = "</del>"

min_len_threshold = 8

for line in sys.stdin:
    line = line.strip()
    l = line.replace(" ","_")
    l = l.decode("UTF-8")
    (src, tgt) = l.split("\t")
    
    if len(src)< min_len_threshold:
        continue
    s = SequenceMatcher(None, src, tgt)
    d = ''
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if len(d) > 0:
            d += ' '
        if tag == "delete":
            d += DEL_START_SYM + " " + " ".join(list(src[i1:i2])) + " " + DEL_END_SYM
        elif tag == "equal":
            d += " ".join(list(src[i1:i2]))
        elif tag == "replace":
            d += DEL_START_SYM + " " + " ".join(list(src[i1:i2])) + " " + DEL_END_SYM + " " + INS_START_SYM + " " + " ".join(list(tgt[j1:j2])) + " " + INS_END_SYM
        else:
            d += INS_START_SYM +" " + " ".join(list(tgt[j1:j2])) + " " + INS_END_SYM
    
    
   #print "[DEBUG] %s\t%f\n%s\t%s" % (line.encode("utf-8"), s.ratio(),  " ".join(list(src)).encode("utf-8"),  d.encode("utf-8"))
    print "%s\t%s" % (" ".join(list(src)),  d)
