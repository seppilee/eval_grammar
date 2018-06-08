#!/usr/bin/env python
#-*- coding: UTF-8 -*-
from __future__ import print_function
"""
SQL DUMP

(000000,'U.K.','English','Japanese','おてんきはいつよかったです、家の中で本を読んでいます','おてんきはいつよくなかったです、家の中で本を読んでいます','2017-01-13 22:49:45'),
可不可以加一下微信，我一般不怎么。',NULL,'2017-01-07 07:39:06'
"""

import sys
import re
import os
from langdetect import detect

#utf-8 encoding for python2
reload(sys)
sys.setdefaultencoding("UTF-8")

num_words = 0

#pattern for extraction
STRING_RE = re.compile(r"\((\d+),\'([^\']+?)\',\'([^\']+?)\',\'([^\']+?)\',\'(.+?)\',\'?(.+?)\'?,\'([^\']+?)\'\)")

#remove escape simbole
ESCAPE_RE = re.compile(r"\\(['\"])")

# remove text emoticon
# https://en.wikipedia.org/wiki/List_of_emoticons
# :‑) :) :-] :] :-3 :3 :-> :> 8-) 8) :-} :} :o) :c) :^) =] =)
EMOTXT_RE = re.compile(r'(:|;|=)(-|‑|o|c|\^)?(\)|\(|D|P|\[|\]|>|3|\})|\(?\^\^\)?|\)\)\)*|\(\(\(*')


EMOTICON_RE = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
                        )

def main():
    for line in sys.stdin:
        line = re.sub("\r|\n|\uFEFF", "", line)
        result = STRING_RE.findall(line, re.MULTILINE)
        if result:
            #print result.group(3), result.group(4), "\t",
            for sent in result:
                src_lang = sent[2].strip()
                tgt_lang = sent[3].strip()
                src_txt  = sent[4].strip()
                tgt_txt  = sent[5].strip()

                src_txt1 = ESCAPE_RE.sub(r'\1',src_txt)
                tgt_txt1 = ESCAPE_RE.sub(r'\1',tgt_txt)

                #print src_lang, "\t", tgt_lang, "\t", src_txt1, "\t", tgt_txt1


                #lang detection
                if src_lang == 'English' or tgt_lang == 'English':
                    try:
                        if detect(src_txt) == "en" and detect(tgt_txt) == "en":
                           words = src_txt.split()
                           num_words = len(words)
                           if 2 < num_words and 20 > num_words: # limitation of words length
                              #print num_words, src_lang,"\t", tgt_lang,"\t", src_txt, "\t\t", tgt_txt
                              src_txt1 = re.sub(r"\\(['\"])",r"\1", src_txt)
                              tgt_txt1 = re.sub(r"\\(['\"])",r"\1", tgt_txt)

                              print( src_txt1, "\t", tgt_txt1)

                    except KeyboardInterrupt:
                        print ('\tKeyboard Interrupted!')
                        try:
                            sys.exit(0)
                        except SystemExit:
                            os._exit(0)

                    except:
                        continue

                    
                    refined1_txt = EMOTXT_RE.sub('', extracted_txt)
                    refined2_txt = replace_unicode(refined1_txt, reps)
                    refined3_txt = EMOTICON_RE.sub('', refined2_txt)
                    #print extracted_txt
                    #print refined2_txt
                    #print refined3_txt



if __name__ == '__main__':
    main()

