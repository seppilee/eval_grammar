#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import re
import codecs
import sys


"""
Evaluation Measures
-------------------

The spellchecker accuracy is measured in terms of standard precision/recall are measured.
Precision/recall measures are calculated at two levels: (i) detection and (ii) correction.
For both levels, precision/recall and other related measures are calculated as follows:

|Precision      - TP / (TP + FP)
|Recall         - TP / (TP + FN)
|F1-measure     - 2 * (precision * recall) / (precision + recall)
|F0.5-measure   - 1.25 * (precision * recall) /(0.25 * precision) +recall
|F2 -           -  5  * (precision * recall) /(4 * precision) +recall
|Accuracy       - (TP + TN) / (TP + FP + TN + FN)

Error detection
---------------

|**TP** - Number of words with spelling errors that the spell checker detected correctly
|**FP** - Number of words identified as spelling errors that are not actually spelling errors
|**TN** - Number of correct words that the spell checker did not flag as having spelling errors
|**FN** - Number of words with spelling errors that the spell checker did not flag as having spelling errors

Error correction
----------------
|**TP** - Number of words with spelling errors for which the spell checker gave the correct suggestion
|**FP** - Number of words (with/without spelling errors) for which the spell checker made suggestions, and for those,
|         either the suggestion is not needed (in the case of non-existing errors) or the suggestion is incorrect if
|         indeed there was an error in the original word.
|**TN** - Number of correct words that the spell checker did not flag as having spelling errors and no
|         suggestions were made.
|**FN** - Number of words with spelling errors that the spell checker did not flag as having spelling errors or did not
|         provide any suggestions

"""

class SpellEval:
    def __init__(self, output_filename, gold_filename):
        # for top-n accuracy (precision, recall etc)
        self.nbest = 10

        # name of the dataset
        self.dataset_name = "Grammar Correction"

        # results : spelling error detection
        self.precision_d = 0.0
        self.recall_d = 0.0
        self.tp_d = 0
        self.fp_d = 0
        self.tn_d = 0
        self.fn_d = 0
        self.f1_d = 0.0
        self.f05_d = 0.0
        self.accuracy_d = 0.0

        # results: spelling error correction
        self.precision_c = [0.0] * self.nbest
        self.recall_c = [0.0] * self.nbest
        self.tp_c = [0] * self.nbest
        self.fp_c = [0] * self.nbest
        self.tn_c = [0] * self.nbest
        self.fn_c = [0] * self.nbest
        self.f1_c = [0.0] * self.nbest
        self.f05_c = [0.0] * self.nbest
        self.accuracy_c = [0.0] * self.nbest

        self.corpus_size = 0
        self.gold_standard = {}
        self.system_suggestions = {}

        # open files for reading
        fH = self.open_files(output_filename, gold_filename)
       
        gold_file_lines = fH[0].readlines()
        out_file_lines = fH[1].readlines()

        if len(out_file_lines) != len(gold_file_lines):
            print("error: file size differ between the test file and gold file")
            sys.exit(1)

        self.close_files(fH)

        # some required overall and specific info
        #self.gold_content, self.corpus_size) = self.read_file_into_map(gold_file_lines)

        # each error entry is a tuple of sentence number and word number
        #self.gold_standard = self.get_error_locations(output_file_lines, gold_file_lines)
        
        # get suggestions from system output
        self.gold_standard = self.get_suggestions_map(gold_file_lines)        
        self.system_suggestions = self.get_suggestions_map(out_file_lines)
        #print(self.sys_tag_num, self.gold_tag_num) 

        self.corpus_size = len(out_file_lines)


    def read_file_into_map(self, file_lines):
        i = 0
        total_words = 0
        content_map = {}
        while i < len(file_lines):
            line = file_lines[i]
            line = re.sub(r'\n$', '', line)
            words = re.split(r'\s+', line)
            total_words += len(words)
            j = 0
            while j < len(words):

                content_map[(i,j)] = words[j]
                j += 1
            i += 1
        return content_map, total_words

    def open_files(self, output_filename, gold_filename):
        file_handles = []
        try:
            gfh = codecs.open(gold_filename, "r", encoding="utf-8")
            ofh = codecs.open(output_filename, "r", encoding="utf-8")
        except IOError as err:
            print("I/O error: {0}".format(err))
        else:
            file_handles = [gfh, ofh]
        return file_handles

    def get_error_locations(self, test_file_lines, gold_file_lines):
        # error_data[error_location] = (error, gold)
        error_data = {}
        i = 0
        while i < len(test_file_lines):
            test_line = test_file_lines[i]
            gold_line = gold_file_lines[i]
            test_line = re.sub(r'\n$', '', test_line)
            gold_line = re.sub(r'\n$', '', gold_line)
            test_words = re.split(r'\s+', test_line)
            gold_words = re.split(r'\s+', gold_line)

            if len(test_words) != len(gold_words):
                print('error: the number of words in test sentence and gold sentence differ. Error line number - ', i)
            j = 0
            while j < len(test_words):
                if test_words[j] != gold_words[j]:
                    error_data[(i,j)] = (test_words[j], gold_words[j])
                j += 1
            i += 1
        return error_data

    def get_suggestions_map(self, out_file_lines):
        i = 0
        suggestions_map = {}
        while i < len(out_file_lines):
            out_line = out_file_lines[i]
            out_line = re.sub(r'\n$', '', out_line)
            matches = re.findall(r'(<(del|ins)> (.+?) <\/\2>)', out_line)
            #matches_num += len(matches)
            if matches:
                for m in matches:
                    corr_type = m[1]
                    sugg_orig = m[2]                
                    sugg_new = re.sub(r'\s+', '|', sugg_orig)
                    sugg_pat_orig = r'<' + corr_type + '> ' +sugg_orig + ' </' + corr_type +'>'
                    sugg_pat_orig = sugg_pat_orig.replace(')', '\)')
                    sugg_pat_orig = sugg_pat_orig.replace('(', '\(')
                    sugg_pat_new = r'<' + corr_type + '>' + sugg_new + '</' + corr_type +'>'
                    out_line = re.sub(sugg_pat_orig, sugg_pat_new, out_line, count=1)
            out_words = re.split(r'\s+', out_line)
            j = 0
            while j < len(out_words):
                suggestion_match = re.search(r'<(del|ins)>(.+)<', out_words[j])
                if suggestion_match:
                    suggestion_line= suggestion_match.group(2)
                    suggestions = re.split(r'\|', suggestion_line)
                    suggestions_map[(i,j)] = suggestions
                j += 1
            i += 1
        return suggestions_map


    def evaluate(self):

        total_errors = len(self.gold_standard)

        # fill/update true/false positives for correction/detection
        for err_loc in self.system_suggestions.keys():
            if err_loc in self.gold_standard.keys():
                #print(err_loc)
                self.tp_d += 1  # right detection comparing with gold corpus
                word_suggestions = self.system_suggestions[err_loc]
                #print(word_suggestions)
                error_found = False
                i = 0;
                print(len(self.system_suggestions[err_loc]))
                while i < len(self.system_suggestions[err_loc]):
                    print(word_suggestions[i], self.gold_standard[err_loc][i])
                    if word_suggestions[i] == self.gold_standard[err_loc][i]:
                        error_found = True 
                        self.tp_c[i] += 1  # right correction
                        j = i+1
                        while j < len(self.system_suggestions[err_loc]):
                            self.tp_c[j] += 1
                            j += 1
                        break
                    else:
                        self.fp_c[i] += 1  # fales correction
                    i += 1
                if len(self.system_suggestions[err_loc]) < self.nbest:
                        k = len(self.system_suggestions[err_loc])
                        while k < self.nbest:
                            if error_found:
                                self.tp_c[k] += 1
                            else:
                                self.fp_c[k] += 1
                            k += 1
            else:
                self.fp_d += 1     #false detection, only in suggestions > gold
                m = 0
                while m < self.nbest:
                    self.fp_c[m] += 1
                    m += 1

        # fill/update true/false negatives for correction/detection
        self.tn_d = len(self.gold_standard.keys()) - len(self.system_suggestions.keys())
        print(self.tn_d)
        for test_err_loc in self.gold_standard.keys():
            if not test_err_loc in self.system_suggestions.keys(): 
                #self.tn_d -= 1          # reduce true negasitive detection
                self.fn_d += 1          # increase false negative detection

        for i in range(self.nbest):
            self.fn_c[i] = self.fn_d

        for i in range(self.nbest):
            self.tn_c[i] = self.tn_d

        # precision/recall, f-measure for error detection

        self.precision_d = (1.0 * self.tp_d) / (self.tp_d + self.fp_d)
        self.recall_d = (1.0 * self.tp_d) / (self.tp_d + self.fn_d)
        self.f1_d = 2 * (self.precision_d * self.recall_d) / (self.precision_d + self.recall_d)
        self.f05_d = 1.25 * (self.precision_d * self.recall_d) / (0.25 * self.precision_d) + self.recall_d
        self.accuracy_d = (self.tp_d + self.tn_d)/ (self.tp_d + self.tn_d + self.fp_d + self.fn_d)

        # calculate precision/recall, f-measure for spelling correction
        for i in range(len(self.tp_c)):
            self.precision_c[i] = (1.0 * self.tp_c[i]) / (self.tp_c[i] + self.fp_c[i])
            self.recall_c[i] = (1.0 * self.tp_c[i]) / (self.tp_c[i] + self.fn_c[i])
            self.f1_c[i] = 2 * (self.precision_c[i] * self.recall_c[i]) / (self.precision_c[i] + self.recall_c[i])
            # F0.5-measure   - 1.25 * (precision * recall) /(0.25 * precision) +recall
            self.f05_c[i] = 1.25 * (self.precision_c[i] * self.recall_c[i]) / (0.25 * self.precision_c[i]) + self.recall_c[i]
            self.accuracy_c[i] = (self.tp_c[i] + self.tn_c[i])/ (self.tp_c[i] + self.tn_c[i] + self.fp_c[i] + self.fn_c[i])


    def print_results(self):
        print(''.rjust(20), "***************")
        print(''.rjust(20), "Error detection")
        print(''.rjust(20), "***************")
        print('TP:', self.tp_d, 'FP:', self.fp_d, 'TN:', self.tn_d, 'FN:', self.fn_d)
        print('Precision'.ljust(10), ':', '{:5.1f}'.format(self.precision_d * 100.0))
        print('Recall'.ljust(10), ':', '{:5.1f}'.format(self.recall_d * 100.0))
        print('F1-score'.ljust(10), ':', '{:5.1f}'.format(self.f1_d * 100.0))
        print('F0.5-score'.ljust(10), ':', '{:5.1f}'.format(self.f05_d * 100.0))
        print('Accuracy'.ljust(10), ':', '{:5.1f}'.format(self.accuracy_d * 100.0))
        print("")

        print(''.rjust(20), "***************")
        print(''.rjust(20), "Error correction")
        print(''.rjust(20), "***************")
        print("")
        print('TP:', self.tp_c, 'FP:', self.fp_c, 'FN:', self.tn_c, 'FN:', self.fn_c)
        print("top-n".ljust(6), 'Precision'.rjust(10), 'Recall'.rjust(10), 'F1-score'.rjust(10), 'F05-score'.rjust(10), 'Accuracy'.rjust(10))
        print("-----".ljust(6), '---------'.rjust(10), '------'.rjust(10), '--------'.rjust(10), '--------'.rjust(10), '--------'.rjust(10))
        i = 0
        while i < len(self.precision_c):
            top = 'top-' + str(i+1)
            print(top.ljust(6), ''.rjust(4), '{:5.1f}'.format(self.precision_c[i]*100.0), \
                ''.rjust(4), '{:5.1f}'.format(self.recall_c[i]*100.0), \
                ''.rjust(4), '{:5.1f}'.format(self.f1_c[i] * 100.0), \
                ''.rjust(4), '{:5.1f}'.format(self.f05_c[i] * 100.0), \
                ''.rjust(4), '{:5.1f}'.format(self.accuracy_c[i] * 100.0))
            i += 1

    def print_summary(self):
        print(''.rjust(20), "***************")
        print(''.rjust(20), "Data summary")
        print(''.rjust(20), "***************")
        print('Dataset name'.ljust(20), ':', self.dataset_name)
        print('Corpus size'.ljust(20), ':', self.corpus_size)
        print('Errors in Gold Standard/System suggestions'.ljust(20), ':', len(self.gold_standard) ,"/", len(self.system_suggestions))
        # print 'Error details [format: "(sentence num, word position) => original word, gold word"]'
        # for err_loc in self.gold_standard:
        #     print str(err_loc).rjust(20), " => ", self.gold_standard[err_loc][0].rjust(20),
        # ", ",  self.gold_standard[err_loc][1].ljust(20)


    def close_files(self, file_handles):
        for fh in file_handles:
            fh.close()

