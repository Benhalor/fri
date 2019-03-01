import struct
import traceback
import time

root_folder = "pa1-data/"
posting_filename = "output.txt"


def read_posting(filename):
    print("read_posting")
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


# Write an integer to a file to a 4-byte integer
def write_integer_binary(integer, file):
    file.write(struct.pack(">i", integer))


# Write an integer to a file to a 2-byte integer
def write_integer_binary_small(integer, file):
    file.write(struct.pack(">H", integer))


# Convert an integer to its representation in the variable length encoding and write it to file
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
        while integer >= 128:
            r = integer % base
            integer_list.append(r)
            integer = int(integer / base)
        integer_list.append(integer)
        for element in list(reversed(integer_list)):
            file.write(struct.pack(">B", element))


# Convert a list representing an integer in power of 128
def convert_integer_list_to_integer(integer_list):
    n = len(integer_list) - 1
    integer = 0
    base = 128
    for element in integer_list[:-1]:
        integer += element * (base ** n)
        n = n - 1
    integer += (integer_list[-1] - 128) * (base ** n)  # the last integer was increased by 128 because of the coding
    return integer


def write_variable_lenght_encoding(filename):
    print("write_variable_lenght_encoding")
    with open(filename, "wb") as f:
        for termID, posting_list in postings.items():
            # Write termID and length of posting list (4-byte integer)
            write_integer_binary(termID, f)
            write_integer_binary(len(posting_list) * 2, f)

            docID_list = [docID for docID, frequency in posting_list.items()]
            frequency_list = [frequency for docID, frequency in posting_list.items()]

            # Write the difference of termID (because it is ordered increasing)
            last_value = 0
            for docID in docID_list:
                write_integer_variable_length(docID - last_value, f)
                last_value = docID

            # Write the frequencies
            for frequency in frequency_list:
                write_integer_variable_length(frequency, f)


def read_variable_lenght_encoding(filename):
    print("read_variable_lenght_encoding")
    with open(filename, "rb") as f:
        # Read everything
        output = f.read()
        i = 0
        postings_VLE = dict()
        while i < len(output) - 1:
            print(i/len(output))
            # Read termID
            termID = struct.unpack(">i", output[i:i + 4])[0]
            postings_VLE[termID] = {}
            i += 4

            # Read n = 2 x Number_of_docID for this termID
            n = struct.unpack(">i", output[i:i + 4])[0]
            i += 4

            # Read docIDs and frequencies
            values = []
            for j in range(n):
                integer_list = [struct.unpack(">B", output[i:i + 1])[0]]
                i += 1
                # Read until find a "byte de poids fort"
                while integer_list[-1] < 128:
                    integer_list.append(struct.unpack(">B", output[i:i + 1])[0])
                    i += 1
                values.append(convert_integer_list_to_integer(integer_list))
            # Reconstituer la posting liste
            last_value = 0
            for k in range(int(len(values) / 2)):
                docID = values[k] + last_value
                last_value = docID
                frequency = values[k + int(len(values) / 2)]
                postings_VLE[termID][docID] = frequency
    return postings_VLE


write_variable_lenght_encoding(root_folder + "test.txt")
postings_VLE = read_variable_lenght_encoding(root_folder + "test.txt")
print(postings == postings_VLE)
