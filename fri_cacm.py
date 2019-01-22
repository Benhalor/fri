#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 16:54:59 2019

@author: armand
"""

import math
import matplotlib.pyplot as plt


#%% CACM Common words and separators
common_words = set()
with open("CACM/common_words") as f:
    for line in f:
        common_words.add(line.strip())
        
separators = "\n,;:.-!?'()[]{} \"#@/<>\\"


#%% CACM parsing
with open("CACM/cacm.all") as f:
    docs = dict()
    to_read = (".T", ".W", ".K")
    to_ignore = (".B", ".A", ".N", ".X")
    current_marker = ""
    
    for line in f:
        if len(line) > 1 and line[0:2] == ".I":
            i = int(line.replace(".I", ""))
            docs[i] = {".T": "", ".W": "", ".K": ""}
        elif len(line) > 1 and line[0:2] in to_ignore:
            current_marker = ""
        elif len(line) > 1 and line[0:2] in to_read:
            current_marker = line[0:2]
        elif current_marker:
            docs[i][current_marker] += line


#%% CACM tokenisation

def tokenization(docs, separators, stop_list):
    word_list = []
    
    for doc in docs.values():
        for content in doc.values():
            s = content
            for sep in separators:
                s = s.replace(sep, separators[0])
            l = list(filter(lambda a: a != "", s.split(separators[0])))
            for word in l:
                w = word.lower()
                if w not in stop_list:
                    word_list.append(w)
    return word_list


#%% Stats

word_list = tokenization(docs, separators, [])
print("Nombre de tokens dans CACM : ", len(word_list))

filtered_list = tokenization(docs, separators, common_words)
print("Nombre de tokens dans CACM filtré : ", len(filtered_list))
            
print("Taille du vocabulaire de CACM filtré : ", len(set(filtered_list)))


#%% Stats for half the collection

half = {key:value for i,(key,value) in enumerate(docs.items()) if i < len(docs)//2}

half_word_list = tokenization(half, separators, [])
print("Nombre de tokens dans la moitié de CACM : ", len(half_word_list))

half_filtered_list = tokenization(half, separators, common_words)
print("Nombre de tokens dans la moitié de CACM filtré : ", len(half_filtered_list))

print("Taille du vocabulaire de la moitié de CACM filtré : ", len(set(half_filtered_list)))


#%% k,b parameters estimation

M_full = len(set(filtered_list))
T_full = len(word_list)

M_half = len(set(half_filtered_list))
T_half = len(half_word_list)

b = (math.log(M_half) - math.log(M_full)) / (math.log(T_half) - math.log(T_full))
k = M_full / (T_full ** b)

print("b estimé : ", b)
print("k estimé : ", k)

print("Taille estimée du vocabulaire pour 1 million de tokens : ", k*(1000000**b))


#%% Frequencies

freq = dict()
for t in filtered_list:
    if t not in freq:
        freq[t] = 0
    freq[t] += 1

for t in freq:
    freq[t] /= len(filtered_list)

freqL = sorted(freq.values(), reverse=True)


#%% frequency vs rank graph

plt.plot(freqL, ".")
plt.xlabel("Rank")
plt.ylabel("frequency")
plt.title("CACM : Graphe fréquence vs Rang")
plt.show()


#%% log scale

plt.plot([math.log(i+1) for i in range(len(freqL))], [math.log(f) for f in freqL], ".")
plt.xlabel("log(Rank)")
plt.ylabel("log(frequency)")
plt.title("CACM : Graphe log(fréquence) vs log(Rang)")
plt.show()


#%% Indexation

posting = dict() # {id : {doc : occurences} }
term_id = dict() # {word : id}

i = 0

for doc in docs:
    for content in docs[doc].values():
        s = content
        for sep in separators:
            s = s.replace(sep, separators[0])
        l = list(filter(lambda a: a != "", s.split(separators[0])))
        for word in l:
            w = word.lower()
            if w not in common_words:
                if w not in term_id:
                    term_id[w] = i
                    posting[i] = dict()
                    i += 1
                if doc not in posting[term_id[w]]:
                    posting[term_id[w]][doc] = 0
                posting[term_id[w]][doc] += 1


#%% Writing some files

with open("CACM/cacm_ids.txt", 'w') as f:
    for w,i in term_id.items():
        f.write(w + ' ' + str(i) + '\n')

with open("CACM/cacm_posting.txt", 'w') as f:
    for i,di in posting.items():
        f.write(str(i) + ':')
        for d,o in di.items():
            f.write(' ' + str(d) + ' ' + str(o))
        f.write('\n')


#%% Read functions

def read_id(f):
    d = dict()
    for line in f:
        l = line.split(' ')
        d[int(l[0])] = l[1]
    return d

def read_posting(f):
    d = dict()
    for line in f:
        l = line.split(' ')
        i = int(l[0][:-1])
        d[i] = dict()
        n = len(l) - 1
        for k in range(n//2):
            a = int(l[2*k+1])
            b = int(l[2*k+2])
            d[i][a] = b
    return d


#%%










