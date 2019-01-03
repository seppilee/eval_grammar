
#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import print_function

'''
the log ananlyzer for OpenNMT-lua version
 - Hyperparameter options check
 - Peplexity summary
 - error log detection
 - check traning time

 USAGE: analyse_logs.py [-h] [-i INPUT]
'''

import sys
import re
import os
import argparse
import codecs

#utf8 encoding for python2.7
#reload(sys)
#sys.setdefaultencoding("UTF-8")

# find setting for hyperparameters
# -brnn -start_decay_at 10 -learning_rate 1.0 -learning_rate_decay 0.7 -end_epoch 18 -save_every 20000 -gpuid 1
# -max_batch_size 64  -save_model /DEV/devling/ITKC/model/exp30/base/train/model
HY_OPTIONS = re.compile(r"-(\w+?) ([^-\/]+?)\s+")
P_OPTIONS = re.compile(r"\*(.+)")

# find error messages from log files
# error: running '/DEV/torch/install/bin/th train.lua -data /DEV/de
E_MESSAGE = re.compile(r"error\: (.+)")

# DONE time=63190 seconds
E_OPTIONS = re.compile(r"DONE time=(\d+ seconds)")

# [01/15/18 08:32:07 INFO] Epoch 1 ; Iteration 500/6289 ; Optim SGD LR 0.100000 ; Source tokens/s 3264 ; Perplexity 2907.71
STRING_RE = re.compile(r"(\d+)\s*;.+?;.+?;.+?; Perplexity ([0-9.]+)")

#saving checkpoint to '/DEV/devling/ITKC/model/exp30/base/train/model_epoch18_4.69.t7
CHPOINT_RE = re.compile(r".+ checkpoint to \'(.+(18).+)\'")

# Validation perplexity: 79.13
VAL_RE = re.compile(r"Validation perplexity: ([0-9.]+)")

def main(arguments):
    parser = argparse.ArgumentParser(description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-i', '--input', help="The log input file.")
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args(arguments)
    vppl = ""
    args = parser.parse_args(arguments)
    vppl = ""
    ppls = {}
    title = 1

    with codecs.open(args.input, encoding="utf-8") as fp:
        for line in fp:
            line = re.sub("\r|\n|\uFEFF", "", line)
            checkpoint = CHPOINT_RE.search(line)
            hyparams = HY_OPTIONS.search(line)
            pparams = P_OPTIONS.search(line)
            result = STRING_RE.search(line)
            val_ppl = VAL_RE.search(line)
            e_opt = E_OPTIONS.search(line)
            e_message = E_MESSAGE.search(line)

            if checkpoint:
                savepath = checkpoint.group(1)

            if hyparams:
                #print(hyparam.group(1), "\n",  hyparam.group(2))
                print("============ Hyperparameter options =====================")
                for keys, values in HY_OPTIONS.findall(line):
                    print("- ", keys, ":", values)

            if pparams:
               print("-"," ".join([x for x in P_OPTIONS.findall(line)]))

            if e_message:
                print ("found errors during training!\ntraining time:", e_message.group(1))
                return None

            if result:
                if title:
                    print("============ PPL Logs =====================")
                    print("Epoch PPL VPPL")
                    title = 0
                e = result.group(1)
                epoch = int(e)
                ppl = result.group(2)
                ppls[epoch] = ppl
                #print("[dpbug]", epoch , ",", ppl, ",", vppl)

            elif val_ppl:
                vppl = val_ppl.group(1)
                ppls[epoch] = ppl, vppl
                #print("[debug]", epoch, ",", ppl, ",", vppl)
            else:
                continue

        for key, value in sorted(ppls.items()):
           print(key, ' '.join(value))

        print("the last model saved in", savepath)
        print("============ Error Report ====================")




        print("the last model saved in", savepath)
        print("============ Error Report ====================")

        if e_opt:
            print ("No error message has been found during training!\ntraining time:", e_opt.group(1))

if __name__ == '__main__':
    main(sys.argv[1:])

