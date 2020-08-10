import re
import string
import csv
import io
import math
import os
from tqdm import tqdm
directory = r"txtToRead"

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        print()
        print("\033[1;32;40m"+filename+"\033[1;30;40m")

        filename = 'txtToRead/'+filename
        a_file = open(filename, "r", encoding="utf8")

        string_without_line_breaks = " "

        for line in a_file:

            stripped_line = line.rstrip()

            string_without_line_breaks += " "+stripped_line

        a_file.close()

        f = open("dataNoLineBreak.txt", "w", encoding="utf8")
        f.write(string_without_line_breaks)
        f.close()

        with io.open('dataNoLineBreak.txt', 'r', errors='ignore', encoding="utf8", newline=None) as file:

            data = file.readlines()

            data = str(data)

            data = str.lower(data)

            data = data.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))
                                  ).replace(' '*4, ' ').replace(' '*3, ' ').replace(' '*2, ' ').strip()
            data.translate(str.maketrans('', '', "!?.,'123456789"))
            wordList = re.sub(r"[^\w]", " ",  data).split()

        with open("list.csv", mode="r", encoding="utf8") as infile:
            reader = csv.reader(infile)

            newList = dict((rows[0], rows[1]) for rows in reader)

        index1 = 0
        for word in tqdm(wordList):
            if (index1 % 1000 == 0):
                #print(len(wordList), index1)
                pass
            if (index1 % math.ceil(len(wordList)/100) == 0):
                w = csv.writer(
                    open("list.csv", "w", newline="", encoding="utf-8"))
                for key, val in newList.items():
                    w.writerow([key, val])

            index1 += 1
            if word in newList:
                index = wordList.index(word)

                newList[word] = int(newList[word]) + 1

            else:

                newList[word] = 1

        # print(newList)
        os.remove("dataNoLineBreak.txt")
    else:
        continue

