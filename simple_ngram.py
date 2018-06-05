#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import re
import codecs

def wordListToFreqDict(wordlist):
    #w =  " ".join([str(a) for k in wordlist for a in k]) 
        #return [(wordlist.count(p), p) for p in wordlist]
        k = [(wordlist.count(p), ' '.join(map(str,p))) for p in wordlist]
        #y = {s:v for  s,v  in k}
        return k
    
# order of descending frequency.
def sortFreqDict(freqdict):
 #aux = [(x, y) for x, y in freqdict]
# print freqdict
 dictfreq = dict(freqdict)
 aux = [(key, dictfreq[key]) for key in dictfreq]
 aux.sort()
 aux.reverse()
 return aux

def ngrams(input, n):
  input = input.split(' ')
  output = []
  for i in range(len(input)-n+1):
    output.append(input[i:i+n])
  return output


def main(filename, n_gram):
    n = int(n_gram)
    all_ntokens = []
    lines  = 0
    try:
        fH = codecs.open(filename, 'r', 'utf-8')

        for line in fH:
            line.rstrip('\r\n')
            line = line.strip()
            ntokens = ngrams(line, n)
            all_ntokens.extend(ntokens)
            lines +=  1
            if not  lines % 1000:
                print  ("[DEBUG] readline:", lines)
        freq = wordListToFreqDict(all_ntokens)
        print ("[DEBUG] done n-gram!\n")
        sortf= sortFreqDict(freq)

        for e, r in sortf:
            print (e,"\t", r)
            #print e,  ' '.join(map(str,r))

    except IOError as v:
        print(v)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print ('Usage: ./simple_ngram {input_file} {n-gram}')
        sys.exit(2)

    main(sys.argv[1], sys.argv[2])


