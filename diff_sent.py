#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
edit distance tagging:
  This script reads in the source and compare with the golden target.
  The difference represents as markup tag with edit distance
"""

import difflib
import os
import sys
import argparse
import codecs


INS_START_SYM = "<ins>"
INS_END_SYM = "</ins>"
DEL_START_SYM = "<del>"
DEL_END_SYM = "</del>"


def get_lines(filepath_with_name): 
    lines = []
    with codecs.open(filepath_with_name, encoding="utf-8") as f:
        for line in f:
            lines.append(line.strip().split())
    return lines
   
def save_lines(filename_with_path, line):   
    with codecs.open(filename_with_path, "a", encoding="utf-8") as f:
        f.write(line+"\n")

def remove_whitespace_from_line(line_string):
    line = line_string.strip().split()
    tok_line = []
    for token in line:
        if token not in string.whitespace:
            tok_line.append(token)
    return " ".join(tok_line)

def show_diff(seqm):
    """Unify operations between two compared strings
     seqm is a difflib.SequenceMatcher instance whose a & b are strings"""
    output= []
   
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output.append(seqm.a[a0:a1])
        elif opcode == 'insert':
            output.append(INS_START_SYM + seqm.b[b0:b1] + INS_END_SYM)
        elif opcode == 'delete':
            output.append(DEL_START_SYM + seqm.a[a0:a1] + DEL_END_SYM)
        elif opcode == 'replace':
            output.append(DEL_START_SYM + seqm.a[a0:a1] + DEL_END_SYM)
            output.append(INS_START_SYM + seqm.b[b0:b1] + INS_END_SYM)
        else:
            raise RuntimeError
    return ''.join(output)


def __unicode__(string):
   return unicode(string) or u''


def main(arguments):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)    
    parser.add_argument('-s', '--source', help="The source file.")
    parser.add_argument('-t', '--target', help="The target file.")    
    parser.add_argument('-o', '--output_file', help="The file in which to save the generated lines \
        that have been fixed (with diffs).")
    
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args(arguments)

    target_file = args.target
    source_file = args.source
    output_file = args.output_file
    
    target_lines = get_lines(target_file)
    source_lines = get_lines(source_file)
    
    if len(target_lines) != len(source_lines):
        print ("WARNING: len(target_lines) != len(source_lines)")
    
    for source_line, target_line in zip(source_lines, target_lines):     
        src = " ".join(str(x) for x in source_line)
        tgt = " ".join(str(x) for x in target_line)        
        
        try:
            sm = difflib.SequenceMatcher(None, src, tgt)
            sm_diff = show_diff(sm)
            print(sm_diff)
            save_lines(output_file, sm_diff)
        except:
            print("not working with" + src + "seqm")
            break       

if __name__ == '__main__':
     main(sys.argv[1:])

