#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import re

reload(sys)
sys.setdefaultencoding("UTF-8")

text = False
bitext = {}
cleantag = re.compile('<.*?>')

for line in sys.stdin:
    line = line.decode("UTF-8");    
    line = re.sub("\r|\n|\uFEFF", "", line)
    line = re.sub(r'^\s+|\s+$', "", line)
    if re.search("&nbsp;", line): continue # skip line

    if text and ids:
       line = re.sub(cleantag, '', line)
       bitext.setdefault(ids, []).append(line)
       text = False
    if re.match("<SYNC Start", line) :
       line = re.match("<SYNC Start=(\d+)", line)
       ids = line.group(1)
       #print ids
       text = True
    else:
       continue

for key, val in bitext.items():
    print '\t'.join([bi for bi in val])