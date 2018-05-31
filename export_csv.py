#!/usr/bin/env python
#-*- coding: UTF-8 -*-


import csv
import os

def get_text():
    with open('out.csv','wb') as out_file:   #use 'wb' to prevent extra blank line
        csv_out = csv.writer(out_file, delimiter='\t')
        for root, dirs, files in os.walk(r'./tmp'):
            for file in files:
                if file.lower().endswith('.txt'):
                    filepath = os.path.join(root,file)  
                    with open(filepath, 'r') as f:
                         content = f.read()
                         csv_out.writerow([content])   # change to wirterow

get_text()
