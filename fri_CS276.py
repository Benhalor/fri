#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 08:46:08 2019

@author: armand
"""

import os
import math
import matplotlib.pyplot as plt

#%% Stop list

from nltk.corpus import stopwords
stop_set = set(stopwords.words('english'))


#%% Parsing (tokenization is already done)
"""
def parsing(foo, half = False):
    subfolders = [f.path for f in os.scandir("pa1-data") if f.is_dir()]
    docID = 0
    for folder in subfolders:
        if half and folder[-1] == '5':
            break
        print(folder)
        for file_name in os.listdir(folder):
            with open(folder + "/" + file_name) as f:
                for word in f.read().split(" "):
                    w = word.lower()
                    foo(docID, folder + "/" + file_name, w)
            docID += 1


#%% Stats

token_count = 0
filtered_count = 0
voc = set()
freq = dict()

def co(docID, path, word):
    global token_count
    global filtered_count
    token_count += 1
    if word not in stop_set:
        filtered_count += 1
        voc.add(word)
        if word not in freq:
            freq[word] = 0
        freq[word] += 1
    
parsing(co)
print("Nombre de tokens dans CS276 :", token_count)
print("Nombre de tokens dans CS276 filtré :", filtered_count)
print("Taille du vocabulaire dans CS276 filtré:", len(voc))


#%% Stats for half the collection

token_half_count = 0
filtered_half_count = 0
voc_half = set()

def co_half(docID, path, word):
    global token_half_count
    global filtered_half_count
    token_half_count += 1
    if word not in stop_set:
        filtered_half_count += 1
        voc_half.add(word)
    
parsing(co_half, half = True)
print("Nombre de tokens dans la moitié de CS276 :", token_half_count)
print("Nombre de tokens dans la moitié de CS276 filtré :", filtered_half_count)
print("Taille du vocabulaire dans la moitié de CS276 filtré:", len(voc_half))


#%% k,b parameters estimation

M_full = len(voc)
T_full = token_count

M_half = len(voc_half)
T_half = token_half_count

b = (math.log(M_half) - math.log(M_full)) / (math.log(T_half) - math.log(T_full))
k = M_full / (T_full ** b)

print("b estimé :", b)
print("k estimé :", k)

print("Taille estimée du vocabulaire pour 1 million de tokens :", k*(1000000**b))


#%% Frequencies

for t in freq:
    freq[t] /= filtered_count

freqL = sorted(freq.values(), reverse=True)


#%% frequency vs rank graph

plt.plot(freqL, ".")
plt.xlabel("Rank")
plt.ylabel("frequency")
plt.title("CS276 : Graphe fréquence vs Rang")
plt.show()


#%% log scale

plt.plot([math.log(i+1) for i in range(len(freqL))], [math.log(f) for f in freqL], ".")
plt.xlabel("log(Rank)")
plt.ylabel("log(frequency)")
plt.title("CS276 : Graphe log(fréquence) vs log(Rang)")
plt.show()
"""

#%% Indexation and file writing

term_id = dict() # {word : id}
docs = dict() # {docID : path}
i = 0

subfolders = [f.path for f in os.scandir("pa1-data") if f.is_dir()]
docID = 0
for folder in subfolders:
    print(folder)
    posting = dict() # {id : {docID : occurences} }
    for file_name in os.listdir(folder):
        """with open(folder + "/" + file_name) as f:
            for word in f.read().strip().split(" "):
                w = word.lower()
                if w not in stop_set:
                    if w not in term_id:
                        term_id[w] = i
                        i += 1
                    if term_id[w] not in posting:
                        posting[term_id[w]] = dict()
                    if docID not in posting[term_id[w]]:
                        posting[term_id[w]][docID] = 0
                    posting[term_id[w]][docID] += 1"""
        docs[docID] = folder + '/' + file_name
        docID += 1
    """with open("pa1-data/CS276_posting" + folder[-1] + ".txt", 'w') as f:
        for termID in sorted(list(posting)):
            di = posting[termID]
            f.write(str(termID) + ':')
            for docID, occ in di.items():
                f.write(' ' + str(docID) + ' ' + str(occ))
            f.write('\n')"""

"""
with open("pa1-data/CS276_ids.txt", 'w') as f:
    for w,i in term_id.items():
        f.write(w + ' ' + str(i) + '\n')"""
        
with open("pa1-data/CS276_doc_ids.txt", 'w') as f:
    for i, p in docs.items():
        f.write(str(i) + ' ' + p)











