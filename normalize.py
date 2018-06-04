#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unicodedata
import sys
import re

#utf-8 encoding for python2
reload(sys)

sys.setdefaultencoding("UTF-8")
#diacritics = ur'[\u0301\u030a\u030c]'
diacritics = re.compile(ur"([\u0300-\u036F])")


for line in sys.stdin:
    line_uni = unicode(line, "utf-8").rstrip()
    line = unicodedata.normalize('NFD', line_uni)
    line = line.replace(u"«", u"“").replace(u"»", u"”")
    normalized_line = line.encode('utf8').sub(r'(^|[^S\w])#([A-Za-z0-9_]+)', '\\1｟#\\2｠')
    no_diacritics_line = diacritis.sub('', normalized_line)
    line_utf8 = no_diacritics_line.encode("utf-8")
    print line_utf8
