#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 10:43:29 2019

@author: armand
"""

# Read the ids
term_id = dict()

with open("pa1-data/CS276_ids.txt") as f:
    for line in f:
        l = line.split(' ')
        term_id[l[0]] = int(l[1])
        
doc_id = dict()

with open("pa1-data/CS276_doc_ids.txt") as f:
    for line in f:
        l = line.split(' ')
        doc_id[int(l[0])] = l[1].strip()


# read the postings
postings = dict()

for k in range(10):
    with open("pa1-data/CS276_posting" + str(k) + ".txt") as f:
        for line in f:
            l = line.split(' ')
            i = int(l[0][:-1])
            if i not in postings:
                postings[i] = dict()
            n = len(l) - 1
            for kk in range(n//2):
                a = int(l[2*kk+1])
                b = int(l[2*kk+2])
                postings[i][a] = b

all_docs = set(range(len(doc_id) - 1))


# Supposing the requests are in disjunctive normal form
# req = '(mot1 ∧ mot2 ∧ ¬mot3) ∨ (mot2 ∧ ¬mot5 ∧ mot6)'

def split_clauses(request):
    r = request.replace(' ∨', '∨')
    r = r.replace('∨ ', '∨')
    l = []
    for clause in r.split('∨'):
        l.append(clause.strip('()'))
    return l

def find_docs(clause):
    # Returns a set containing all docs corresponding to the boolean clause
    # clause format example: 'mot1 ∧ mot2 ∧ ¬mot3'
    c = clause.replace(' ∧', '∧')
    c = c.replace('∧ ', '∧')
    s = all_docs.copy()
    for word in c.split('∧'):
        if word[0] == '¬':
            i = term_id[word[1:]]
            s = s - set(postings[i].keys())
        else:
            i = term_id[word]
            s = s & set(postings[i].keys())
    return s


def bool_request(req):
    # Returns a set containing all docs corresponding to the boolean request
    # request format example: '(mot1 ∧ mot2 ∧ ¬mot3) ∨ (mot2 ∧ ¬mot5 ∧ mot6)'
    clauses = split_clauses(req)
    s = set()
    for c in clauses:
        s = s | find_docs(c)
    return s


#%% Examples

req1 = '(square ∧ root ∧ approximations)'
print(bool_request(req1))

req2 = '(international ∧ ¬report ∧ matrix) ∨ (¬proposal ∧ equivalence)'
print(bool_request(req2))







