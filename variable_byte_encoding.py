import struct
import traceback
import time

root_folder = "CACM/"
posting_filename = "output.txt"


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


postings = read_posting(root_folder + posting_filename)
print(postings)


def write_integer_binary(integer, file):
    file.write(struct.pack(">i", integer))


with open(root_folder + "test.txt", "wb") as f:
    for termID, posting_list in postings.items():
        write_integer_binary(termID, f)

        docID_list = [docID for docID, frequency in posting_list.items()]
        frequency_list = [frequency for docID, frequency in posting_list.items()]

        for docID in docID_list:
            write_integer_binary(docID, f)

        write_integer_binary(-1, f)  # Separator

        for frequency in frequency_list:
            write_integer_binary(frequency, f)
        write_integer_binary(-1, f)  # Separator

with open(root_folder + "test.txt", "rb") as f:
    output = bytes()
    for line in f:
        output += line
    for i in range(int(len(output) / 4)):
        print(struct.unpack(">i", output[i * 4:(i + 1) * 4])[0])
