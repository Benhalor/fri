#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 16:54:59 2019

@author: gabriel
"""
import os
import numpy as np
import math
from colorama import *
import re
import time

BLOCK_SIZE = 1024
root_folder = "pa1-data/"
posting_filename = "output.txt"
id_filename = "CS276_ids.txt"
docs_filename = "CS276_doc_ids.txt"


def read_posting(filename):
    with open(filename, 'r') as f:
        d = dict()
        for line in f:
            l = line.split(' ')
            i = int(l[0][:-1])
            d[i] = dict()
            n = len(l) - 1
            for k in range(n // 2):
                a = int(l[2 * k + 1])
                b = int(l[2 * k + 2])
                d[i][a] = b
    return d


def read_id(filename):
    with open(filename, 'r') as f:
        d = dict()
        for line in f:
            l = line.split(' ')
            d[l[0].strip("\n")] = int(l[1])
    return d


def read_all(filename):
    with open(filename) as f:
        docs = dict()
        for line in f:
            l = line.split(' ')
            docs[int(l[0].strip("\n"))] = l[1].strip("\n")
    return docs


def maximum_frequency(d):
    L = []
    for key, value in d.items():
        L.append(value)
    return max(L)


def sum_frequency(d):
    L = []
    for key, value in d.items():
        L.append(value)
    return sum(L)


def colorize(document, query):
    for word in query:
        document = re.sub(word, Fore.RED + word + Fore.WHITE, document, flags=re.IGNORECASE)
    return document

def read_document_inline(filename):
    output = ""
    with open(filename) as f:
        for line in f:
            output += line
    return output

def tf_idf():
    # Read postings and ID and docs
    print("Loading documents...")
    postings = read_posting(root_folder + posting_filename)
    id = read_id(root_folder + id_filename)
    docs = read_all(root_folder + docs_filename)
    idf = dict()  # {termID: f(nombre de document dans lequel le terme apparait)}
    counter = dict()  # Used only to count number of documents
    normalization_dictionary = dict()
    document_terms = dict()

    # Calculate term frequency normalization. Used only when using normalization on TF
    """for key, value in postings.items():
        for document_id, weight in value.items():
            if document_id not in document_terms:
                document_terms[document_id] = {}
            document_terms[document_id][key] = weight"""
    print("Calculating TF")
    # Calculate TF and place it in the weight of the postings
    for termID, term_posting in postings.items():
        idf[termID] = len(term_posting)
        for document_id, weight in term_posting.items():
            counter[document_id] = 0
            if weight == 0:
                postings[termID][document_id] = 0
            else:
                # postings[termID][document_id] = weight > 0  # binary
                postings[termID][document_id] = weight  # Raw count
                # postings[termID][document_id] = weight / sum_frequency(document_terms[document_id])  # term frequency
                # postings[termID][document_id] = 1 + math.log10(weight)  # Log normalization
                # postings[termID][document_id] = 0.5 + 0.5*weight/maximum_frequency(document_terms[document_id])  # double normalization 0.5

    number_of_document = len(counter.items())

    print("Calculating IDF")
    # Calculate IDF
    for termID, value in idf.items():
        # idf[termID] = 1  # Unary
        # idf[termID] = 1/value  # Inverse
        idf[termID] = math.log10(number_of_document / value)  # inverse document frequency
        # idf[termID] = math.log10(number_of_document / (1 + value))  # inverse document frequency smooth
        # idf[termID] = math.log10((number_of_document - value) / value)  # probabilistic inverse document frequency

    print("Calculating TF x IDF")
    # Calculate TF * IDF and place it in the weight of the postings
    for key, value in postings.items():
        idf[key] = len(value)
        for document_id, weight in value.items():
            counter[document_id] = 0
            if weight == 0:
                postings[key][document_id] = 0
            else:
                # weight = TF
                postings[key][document_id] = weight * idf[document_id]

    print("Calculating normalization factors")
    # Calculate normalization factor for all documents
    for key, value in postings.items():
        for document_id, weight in value.items():
            if document_id not in normalization_dictionary:
                normalization_dictionary[document_id] = 0
            normalization_dictionary[document_id] += weight * weight
    return number_of_document, postings, normalization_dictionary, docs, id




def process_query(query, number_of_document, tfidf, normalization_dictionary, docs, id, number_of_output,
                  return_color=False):
    answer = []
    # Convert words to ids and count them in the request
    query_list = dict()
    separators = "\n,;:.-!?'()[]{} \"#@/<>\\"

    for sep in separators:
        query = query.replace(sep, separators[0])

    query_for_colorization = []
    for word in query.split(separators[0]):
        word = word.lower()
        if word in id:
            query_for_colorization.append(word)

    for word in query.split(separators[0]):
        word = word.lower()
        if word in id:
            element = id[word]
        else:
            element = -1
            # print("Error: Not present word: " + word)
        if element != -1:
            if element not in query_list:
                query_list[element] = 0
            query_list[element] += 1
    # print("query_list: " + str(query_list))

    # Calculate similarity with request for each document
    score = dict()
    nq = 0
    score = {i: 0 for i in range(0, number_of_document)}
    for id_word, query_weight in query_list.items():
        nq += query_weight * query_weight
        for document_id, document_weight in tfidf[id_word].items():
            score[document_id] += document_weight * query_weight

    # Apply normalization
    for i, value in score.items():
        score[i] = score[i] / (math.sqrt(normalization_dictionary[i]) * math.sqrt(nq))

    output = sorted(range(len(score)), key=lambda i: score[i], reverse=True)
    output_score = sorted(score, reverse=True)
    for i in range(number_of_output):
        answer.append({"doc_number": output[i], "score": output_score[i], "normalization":
            normalization_dictionary[output[i]], "text": read_document_inline(docs[output[i]])})
    if return_color:
        return answer, query_for_colorization
    else:
        return answer


if __name__ == "__main__":
    number_of_document, tfidf, normalization_dictionary, docs, id = tf_idf()
    query = "world"  # input("Enter query: ")
    answer, query_for_colorization = process_query(query, number_of_document, tfidf, normalization_dictionary, docs, id,
                                                   20, return_color=True)
    for line in answer:
        print(colorize(str(line), query_for_colorization))
