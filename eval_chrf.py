#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
template for read two file for analysing chrf
"""
from __future__ import print_function, unicode_literals, division

import sys
import codecs
import io
import re
import argparse 
from collections import defaultdict

# hack for python2/3 compatibility
from io import open
argparse.open = open

def create_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=" program description")

    parser.add_argument(
        '--ref', '-r', type=argparse.FileType('r'), required=True,
        metavar='PATH',
        help="Reference file")
    parser.add_argument(
        '--hyp', type=argparse.FileType('r'), metavar='PATH',
        default=sys.stdin,
        help="Hypothesis file (default: stdin).")

    return parser

def extract_ngram(line, num_ngram):
	words = "".join(line.split()) # space ignored
	#words = line.strip()
	result = defaultdict(lambda: defaultdict(int)) #?
	for length in range(num_ngram):
		for start in range(len(words)):
		    end = start + length + 1
		    if end <= len(words):
		    	result[length][tuple(words[start:end])] += 1
	return result
    #{0: defaultdict(<class 'int'>, {('c',): 1, ('a',): 1, ('t',): 1}), 
     #1: defaultdict(<class 'int'>, {('c', 'a'): 1, ('a', 't'): 1}), 
     #2: defaultdict(<class 'int'>, {('c', 'a', 't'): 1})}

def main(args):
    #1) read file
	for line in args.ref:
		line2 = args.hyp.readline()
    #2) extraction of Ngam
		ngram = extract_ngram(line2, num_ngram=4)
    #3) get correct matching
    	#get_correct()
    #4) calurate Fscore
        #f1()
    #5) output
		print(ngram)

if __name__ == '__main__':

    # python 2/3 compatibility
    if sys.version_info < (3, 0):
        sys.stderr = codecs.getwriter('UTF-8')(sys.stderr)
        sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
        sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
    else:
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True, line_buffering=True)

    parser = create_parser()
    args = parser.parse_args()

    main(args)