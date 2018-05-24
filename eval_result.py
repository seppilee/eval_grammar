#!/usr/bin/python3
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
    parser.add_argument("model_output", help="Model output file")
    parser.add_argument("reference_file", help="Gold file in UTF-8")
    args = parser.parse_args()

    korektor_evaluation = spelleval.SpellEval(args.model_output, args.reference_file)
    korektor_evaluation.print_summary()
    print("")
    korektor_evaluation.evaluate()
    korektor_evaluation.print_results()

