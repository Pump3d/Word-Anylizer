from os import listdir, getcwd
from os.path import isfile, isdir
import matplotlib.pyplot as plt
import json
import nltk

POSs = {
    "CC": "Coordinating Conjunction",
    "CD": "Cardinal Digit",
    "DT": "Determiner",
    "EX": "Existential",
    "FW": "Foreign Word",
    "IN": "Preposition",
    "JJ": "Adjective",
    "JJR": "Adjective",
    "JJS": "Adjective",
    "LS": "List",
    "MD": "Modal",
    "NN": "Noun",
    "NNS": "Noun",
    "NNP": "Proper Noun",
    "NNPS": "Proper Noun",
    "PDT": "Predeterminer",
    "POS": "Possessive Ending",
    "PRP": "Pronoun",
    "PRP$": "Pronoun",
    "RB": "Adverb",
    "RBR": "Adverb",
    "RBS": "Adverb",
    "RP": "Particle",
    "TO": "To",
    "UH": "Interjection",
    "VB": "Verb",
    "VBD": "Verb",
    "VBG": "Verb",
    "VBN": "Verb",
    "VBP": "Verb",
    "VBZ": "Verb",
    "WDT": "Determiner",
    "WP": "Pronoun",
    "WP$": "Pronoun",
    "WRB": "Adverb"
}


def check():
    path = getcwd() + "\\JSONs"
    if not isdir(path):
        return False

    if len(listdir(path)) == 0:
        return False

    lists = listdir(path)
    if "num.txt" in lists:
        lists.remove("num.txt")

    for file in lists:
        if isfile(path + "\\{}\\words.json".format(file)):  # and isfile(path + "\\{}\\endings.json".format(file)):
            return lists

    return False


def write(txt):
    file = open("results.txt", mode="w")
    file.write(txt)
    file.close()


def decodeWords(lists):
    words = []

    for file in lists:
        if isfile(getcwd() + "\\JSONs\\{}\\words.json".format(file)):
            openFile = open(getcwd() + "\\JSONs\\{}\\words.json".format(file), "r")
            words += json.load(openFile)
            openFile.close()

    return words


def sortSpeech(words):
    partOfSpeech = nltk.pos_tag(words)
    words = None

    percents = {}
    for k, v in POSs.items():
        if not v in percents:
            percents[v] = 0

        percents[v] += (len([ele for ele in partOfSpeech if ele[1] == k]) / len(partOfSpeech)) * 100

    print(partOfSpeech)
    print(percents)

    for k, v in percents.copy().items():
        if v == 0:
            del percents[k]

    fig1, ax1 = plt.subplots()
    ax1.pie(list(percents.values()), labels=list(percents.keys()), autopct='%1.2f%%', shadow=True, startangle=90)
    ax1.axis('equal')

    plt.show()


def main():
    lists = check()
    if not lists:
        write("JSON files not found. Have you ran the program or misplaced the JSONs folder?")
        quit()

    sortSpeech(decodeWords(lists))


if __name__ == '__main__':
    main()
