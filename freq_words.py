#! /usr/bin/python3

import re
import sys
from collections import Counter

count = Counter()

def main():
    for line in sys.stdin:
        line = re.sub("\r|\n|\uFEFF", "", line)
        for word in line.split():
            count[word] += 1

    for key,freq in sorted(count.items(), key=lambda x: x[1], reverse=True):
        print(key+"\t"+ str(freq))

if __name__ == '__main__':
            main()
