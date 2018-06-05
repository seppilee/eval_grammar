#!/usr/bin/env python

import pprint
import pickle
from argparse import ArgumentParser

encoding_type = 'iso-8859-1'

objects = []

parser = ArgumentParser()                                                                 
parser.add_argument('fname', metavar='FILE', help='file to process')
args = parser.parse_args()

with open(args.fname, "rb") as openfile:
    while True:
        try:
            objects =  pickle.load(openfile, encoding=encoding_type)
        except EOFError:
            break

pprint.pprint(objects)
