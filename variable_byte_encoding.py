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


# print(postings)


def write_integer_binary(integer, file):
    file.write(struct.pack(">i", integer))


def write_integer_binary_small(integer, file):
    file.write(struct.pack(">H", integer))


def write_integer_variable_length(integer, file):
    base = 128
    if integer < 0:
        raise ValueError("Integer should be positive")
    elif integer < 128:
        file.write(struct.pack(">B", integer + base))  # Bit de poids fort à 1
    else:
        integer_list = []
        r = 128 + integer % base
        integer_list.append(r)
        integer = int(integer / base)
        while integer > 128:
            r = integer % base
            integer_list.append(r)
            integer = int(integer / base)
        integer_list.append(integer)
        for element in list(reversed(integer_list)):
            file.write(struct.pack(">B", element))


def convert_integer_list_to_integer(integer_list):
    n = len(integer_list) - 1
    integer = 0
    base = 128
    for element in integer_list[:-1]:
        integer += element * (base ** n)
        n = n - 1
    integer += (integer_list[-1] - 128) * (base ** n)
    return integer


with open(root_folder + "test.txt", "wb") as f:
    for termID, posting_list in postings.items():
        write_integer_binary(termID, f)
        write_integer_binary(len(posting_list)*2, f)

        docID_list = [docID for docID, frequency in posting_list.items()]
        frequency_list = [frequency for docID, frequency in posting_list.items()]

        last_value = 0
        for docID in docID_list:
            write_integer_variable_length(docID-last_value, f)
            last_value = docID

        for frequency in frequency_list:
            write_integer_variable_length(frequency, f)


with open(root_folder + "test.txt", "rb") as f:
    output = bytes()
    for line in f:
        output += line
    i = 0
    print(output)
    postings_VLE = dict()
    while i < len(output) - 1:
        # Read termID
        termID = struct.unpack(">i", output[i:i+4])[0]
        postings_VLE[termID] = {}
        i += 4
        # Read len(posting_list) for this termID
        n = struct.unpack(">i", output[i:i + 4])[0]
        i += 4

        # Read docIDs
        values = []
        for j in range(n):
            integer_list = [struct.unpack(">B",output[i:i+1])[0]]
            i += 1
            while integer_list[-1] <128:
                integer_list.append(struct.unpack(">B", output[i:i+1])[0])
                i += 1
            values.append(convert_integer_list_to_integer(integer_list))
        last_value = 0
        for k in range(int(len(values)/2)):
            docID = values[k] + last_value
            last_value = docID
            frequency = values[k+int(len(values)/2)]
            postings_VLE[termID][docID] = frequency

print(postings == postings_VLE)

