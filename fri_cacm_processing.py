#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 16:54:59 2019

@author: gabriel
"""
import os
import numpy as np

BLOCK_SIZE = 1024
root_folder = "CACM/"
files = [root_folder + "cacm_posting.txt"]


def read_posting_block(filename, block_id, block_size):
    with open(filename, 'r') as f:
        liste = []
        count = 0
        for j, line in enumerate(f):
            if block_id * block_size <= j < (block_id + 1) * block_size:
                l = line.split(' ')
                i = int(l[0][:-1])
                liste.append([i, dict()])
                n = len(l) - 1
                for k in range(n // 2):
                    a = int(l[2 * k + 1])
                    b = int(l[2 * k + 2])
                    liste[count][1][a] = b
                count += 1
        if len(liste) == 0:
            raise IndexError
    return liste


file_dictionary = {}
for filename in files:
    file_dictionary[filename] = {"block_id": 0, "current_index": 0, "memory_block": None}

output = dict()

# Init
for filename, values in file_dictionary.items():
    block_id = values["block_id"]
    if block_id != -1:
        file_dictionary[filename]["memory_block"] = read_posting_block(filename, block_id, BLOCK_SIZE)

while len(file_dictionary) > 0:
    # Select the index to append
    minimum = np.inf
    minimum_file = ""
    for filename, values in file_dictionary.items():
        val = values["memory_block"][values["current_index"]][0]
        if val < minimum:
            minimum_file = filename
            minimum = val

    # Append to output
    if minimum in output:
        output[minimum] = {**output[minimum],
                           **file_dictionary[minimum_file]["memory_block"][
                               file_dictionary[minimum_file]["current_index"]][
                               1]}
    else:
        output[minimum] = file_dictionary[minimum_file]["memory_block"][file_dictionary[minimum_file]["current_index"]][
            1]

    # Move on index
    if file_dictionary[minimum_file]["current_index"] < len(file_dictionary[minimum_file]["memory_block"]) - 1:
        file_dictionary[minimum_file]["current_index"] += 1
    elif len(file_dictionary[minimum_file]["memory_block"]) == BLOCK_SIZE:
        file_dictionary[minimum_file]["block_id"] += 1
        print(minimum_file, file_dictionary[minimum_file]["block_id"])
        file_dictionary[minimum_file]["memory_block"] = read_posting_block(minimum_file,
                                                                           file_dictionary[minimum_file]["block_id"],
                                                                           BLOCK_SIZE)
        file_dictionary[minimum_file]["current_index"] = 0
    else:
        del file_dictionary[minimum_file]
        print("Close " + minimum_file)

print("Writing output")
with open(root_folder + "output.txt", 'w') as f:
    for i, di in output.items():
        f.write(str(i) + ':')
        for d, o in di.items():
            f.write(' ' + str(d) + ' ' + str(o))
        f.write('\n')
