#
import re
import string
import csv
import io
import math
import os
import os.path
import subprocess
import sys


def run(runProgramSelection):
    if(runProgramSelection == "y"):
        print("starting...")
        runProgram(directory, listCvsexist, txtToReadExist)
    else:
        print("stopping...")
        exit()


directory = r"txtToRead"
listCvsexist = os.path.exists("list.csv")
txtToReadExist = os.path.exists("txtToRead")


def runProgram(directory, listCvsexist, txtToReadExist):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):

            print()
            print(" File: \033[1;32;40m"+filename+"\033[1;30;40m")

            filename = 'txtToRead/'+filename
            a_file = open(filename, "r", errors="replace", encoding="utf8")

            string_without_line_breaks = " "

            for line in a_file:

                stripped_line = line.rstrip()

                string_without_line_breaks += " "+stripped_line

            a_file.close()

            f = open("dataNoLineBreak.txt", "w", encoding="utf8")
            f.write(string_without_line_breaks)
            f.close()

            with io.open('dataNoLineBreak.txt', 'r', errors='replace', encoding="utf8",  newline=None) as file:

                data = file.readlines()

                data = str(data)

                data = str.lower(data)

                data = data.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))
                                      ).replace(' '*4, ' ').replace(' '*3, ' ').replace(' '*2, ' ').strip()
                data.translate(str.maketrans('', '', "!?.,'123456789"))
                wordList = re.sub(r"[^\w]", " ",  data).split()
            os.remove("dataNoLineBreak.txt")
            with open("list.csv", mode="r", encoding="utf8") as infile:
                reader = csv.reader(infile, delimiter=";",)

                newList = dict((rows[0], rows[1]) for rows in reader)

            index1 = 0
            for word in tqdm(wordList):
                if (index1 % math.ceil(len(wordList)/100) == 0):
                    w = csv.writer(
                        open("list.csv", "w", newline="", encoding="utf-8"), delimiter=";")
                    for key, val in newList.items():
                        w.writerow([key, val])

                index1 += 1
                if word in newList:
                    index = wordList.index(word)

                    newList[word] = int(newList[word]) + 1

                else:

                    newList[word] = 1

            # print(newList)
            print("\033[1;33;40m")
            continueInput = input("Next file? (y/n):")
            print('\033[m')
            if(continueInput != "y"):
                exit()
        else:
            continue


try:
    from tqdm import tqdm
    importTqdm = True
except ImportError:
    importTqdm = False

if not listCvsexist or not txtToReadExist or not importTqdm:
    print("Setup will install tqdm, create folder 'txtToRead' and file 'list.csv'")
    print("\033[1;33;40m")
    setup = input("Start setup? (y/n): ")
    print('\033[m')
    if(setup == "y"):
        try:
            from tqdm import tqdm
        except ImportError:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", 'tqdm'])
            print("imported tqdm")
        finally:
            from tqdm import tqdm
        if(not listCvsexist):
            csvList = open("list.csv", "w+")
            print("list.csv Created.")
        if(not txtToReadExist):
            os.mkdir("txtToRead/")
            print("Folder txtToRead Created")
        print("Ready to run, put your .txt files into txtToRead folder and run the program")
        print("\033[1;33;40m")
        runProgramSelection = input("run program? (y/n)")
        print('\033[m')
        run(runProgramSelection)
else:
    print("Ready to run, put your .txt files into txtToRead folder and run the program")
    print("\033[1;33;40m")
    runProgramSelection = input("run program? (y/n)")
    print('\033[m')
    run(runProgramSelection)


exit()
