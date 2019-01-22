import time
import numpy as np
import matplotlib.pyplot as plt
import fri_cacm_vectoriel_search

root_folder = "CACM/"
query_filename = "query.text"
query_answer_filename = "qrels.text"


def read_queries(filename):
    with open(filename) as f:
        queries = dict()
        to_read = (".W")
        to_ignore = (".T", ".B", ".A", ".N", ".X", ".K")
        current_marker = ""

        for line in f:
            if len(line) > 1 and line[0:2] == ".I":
                i = int(line.replace(".I", ""))
                queries[i] = {".W": "", "answers": []}
            elif len(line) > 1 and line[0:2] in to_ignore:
                current_marker = ""
            elif len(line) > 1 and line[0:2] in to_read:
                current_marker = line[0:2]
            elif current_marker:
                queries[i][current_marker] += line
    return queries


def read_answer(filename, queries):
    with open(filename) as f:
        for line in f:
            splitted = line.split(" ")
            queries[int(splitted[0])]["answers"].append(int(splitted[1]))
    return queries


def calculate_number_of_relevant_documents(guess, expected):
    if len(expected) == 0:
        return -1
    count = 0
    for element in expected:
        if element in guess:
            count += 1
    return count


queries = read_queries(root_folder + query_filename)
queries = read_answer(root_folder + query_answer_filename, queries)

last_time = time.time()
number_of_document, tfidf, normalization_dictionary, docs, id = fri_cacm_vectoriel_search.tf_idf()
print("Duration for building index : " + str((time.time() - last_time) * 1000) + " ms")
rappel_list = []
precision_list = []
query_duration_list = []

for NUMBER_OF_RETURNED_DOCUMENTS in range(1, 30):
    rappel_list_temp = []
    precision_list_temp = []
    for key, value in queries.items():
        query = value[".W"]
        last_time = time.time()
        answer = fri_cacm_vectoriel_search.process_query(query, number_of_document, tfidf, normalization_dictionary,
                                                         docs,
                                                         id, NUMBER_OF_RETURNED_DOCUMENTS)
        query_duration_list.append(time.time() - last_time)
        answer_list = []
        for element in answer:
            answer_list.append(element["doc_number"])

        if len(queries[key]["answers"]) == 0:
            pass  # print(key, queries[key])
        else:
            number_of_relevant_found_documents = calculate_number_of_relevant_documents(answer_list,
                                                                                        queries[key]["answers"])
            precision = number_of_relevant_found_documents / NUMBER_OF_RETURNED_DOCUMENTS
            rappel = number_of_relevant_found_documents / len(queries[key]["answers"])
            rappel_list_temp.append(rappel)
            precision_list_temp.append(precision)
    rappel_list.append(np.mean(rappel_list_temp))
    precision_list.append(np.mean(precision_list_temp))

print("Mean duration for one request: " + str(1000 * np.mean(query_duration_list)) + " ms")
plt.plot(precision_list, rappel_list)
plt.xlabel("Rappel")
plt.ylabel("Precision")
plt.title("CACM : Courbe précision/rappel")
plt.show()
