#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import random
import math

# Configure paths to your dataset files here
DATASET_FILE = 'data.txt'
FILE_TRAIN = 'train.txt'
FILE_VALID = 'validation.txt'
FILE_TESTS = 'test.txt'

# Set to true if you want to copy first line from main
IS_CSV = False
IS_PER = False

# Set percentage for train, valid, test dataset
PERCENT_TRAIN = 98
PERCENT_VALID = 1
PERCENT_TESTS = 1

# Set line number for train, valid, test dataset
num_valid = 500
num_tests = 580

data = [l for l in open(DATASET_FILE, 'r')]

train_file = open(FILE_TRAIN, 'w')
valid_file = open(FILE_VALID, 'w')
tests_file = open(FILE_TESTS, 'w')

if IS_CSV:
    train_file.write(data[0])
    valid_file.write(data[0])
    tests_file.write(data[0])
    data = data[1:len(data)]

num_of_data = len(data)
num_train = int(num_of_data - num_valid - num_tests)

if IS_PER:
    num_train = int((PERCENT_TRAIN/100.0)*num_of_data)
    num_valid = int((PERCENT_VALID/100.0)*num_of_data)
    num_tests = int((PERCENT_TESTS/100.0)*num_of_data)

data_fractions = [num_train, num_valid, num_tests]
split_data = [[],[],[]]

rand_data_ind = 0

for split_ind, fraction in enumerate(data_fractions):
    for i in range(fraction):
        if len(data) > 0 :
            rand_data_ind = random.randint(0, len(data)-1)
            if len(data)%1000 == 0: print "remained processing line: " + str(len(data))
            split_data[split_ind].append(data[rand_data_ind])
            data.pop(rand_data_ind)

for l in split_data[0]:
    train_file.write(l)

for l in split_data[1]:
    valid_file.write(l)

for l in split_data[2]:
    tests_file.write(l)

train_file.close()
valid_file.close()
tests_file.close()
