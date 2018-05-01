#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import argparse
import codecs
import re
import sys
import spelleval

"""
************************************
Spell checker main evaluation script
************************************

usage: eval_spell_checking.py [-h] model_output reference_file

positional arguments:
  model_output     Model output in UTF-8
  reference_file      Gold file in UTF-8

optional arguments:
  -h, --help     show this help message and exit
"""



if __name__ == '__main__':

    # parser the command line arguments
    parser = argparse.ArgumentParser(description="Spellchecker Evaluation")
    #parser.add_argument("test_file", help="Input file in UTF-8")
    parser.add_argument("system_output", help="Model output file")
    parser.add_argument("gold_file", help="Gold file in UTF-8")
    #parser.add_argument("n_best", help="Evaluate top-n suggestions", type=int)
    #parser.add_argument("dataset_name", help="Name of the Test")
    args = parser.parse_args()

    korektor_evaluation = spelleval.SpellEval(args.system_output, args.gold_file)
    korektor_evaluation.print_summary()
    print ""
    korektor_evaluation.evaluate()
    korektor_evaluation.print_results()

