#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unicodedata
import sys
import re


#utf-8 encoding for python2
reload(sys)
sys.setdefaultencoding("UTF-8")

diacritics = ur'[\u0301\u030a\u030c]'

for line in sys.stdin:
    line_uni = unicode(line, "utf-8").rstrip()
    normalized_line = unicodedata.normalize('NFD', line_uni)
    no_diacritics_line = re.sub(diacritics, '', normalized_line)
    line_utf8 = no_diacritics_line.encode("utf-8")
    print line_utf8
