#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys

for line in sys.stdin:
  try:
    line.decode('utf-8')
    print(line, end='', file=sys.stdout)
  except UnicodeDecodeError:
    print(line, end='', file=sys.stderr)