#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import random
import sys

extracted_lines = 700

lines = []
for line in sys.stdin:
    lines.append(line)
print(" ".join(str(s) for s in random.sample(lines, extracted_lines)))
