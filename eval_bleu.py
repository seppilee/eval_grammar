#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

'''
According to this paper: http://www.aclweb.org/anthology/I/I05/I05-2014.pdf
A Bleu_4 Score in Word Level corresponds to Bleu_18 Score in Character Level.
Hence, in this project, we are using a Character Level Bleus of values: 5, 10, 15, 20.
'''

import sys
import codecs
import argparse
from nltk.translate.bleu_score import sentence_bleu

def BLEU(candidate, reference, n=4):
    ref = [reference.strip().split()]
    can = candidate.strip().split()

    if len(candidate) == 0:

        bleu = 0

    else:

        if n == 1:
            bleu = sentence_bleu(ref, can, weights=(1, 0, 0, 0))
        elif n == 2:
            bleu = sentence_bleu(ref, can, weights=(.5, .5, 0, 0))
        elif n == 3:
            bleu = sentence_bleu(ref, can, weights=(.33, .33, .33, 0))
        elif n ==4:
            bleu = sentence_bleu(ref, can, weights=(.25, .25, .25, .25))
        else:
            print('Please Define n in BLEU function with integers from 1 to 4.')

    return bleu


def get_lines(filepath_with_name): 
    lines = []
    with codecs.open(filepath_with_name, encoding="utf-8") as f:
        for line in f:
            lines.append(line.strip().split())
    return lines

def main(arguments):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)    
    parser.add_argument('-c', '--candidate', help="The candidate file.")
    parser.add_argument('-r', '--reference', help="The reference file.")    
    sum_bleu = 0
    
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args(arguments)

    candidate_file = args.candidate
    reference_file = args.reference

    candidate_lines = get_lines(candidate_file)
    reference_lines = get_lines(reference_file)
    total_line = len(reference_lines)

    if len(reference_lines) != len(candidate_lines):
        print ("WARNING: len(candidate_lines) != len(reference_lines)")

    for can_line, ref_line in zip(reference_lines, candidate_lines):     
        can = " ".join(str(x) for x in can_line)
        ref = " ".join(str(x) for x in ref_line) 

        bleu = BLEU(can, ref, 2)
        print(can, "\t" , ref , "\t", bleu)
        sum_bleu += bleu
    print ('%s %2d %s %s' % ("bleu score:", sum_bleu/total_line*100, "/ lines:", total_line))

if __name__ == "__main__":
    main(sys.argv[1:])
   
