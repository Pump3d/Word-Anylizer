import keyboard
import json
from os import getcwd
from os.path import isfile

words = []
endings = []

curWord = ''

allowedWords = [
    'a', 'b', 'c',
    'd', 'e', 'f',
    'g', 'h', 'i',
    'j', 'k', 'l',
    'm', 'n', 'o',
    'p', 'q', 'r',
    's', 't', 'u',
    'v', 'w', 'x',
    'y', 'z', '-',

    '1', '2', '3',
    '4', '5', '6',
    '7', '8', '9',
    '0',

    'space', 'enter', '-',
    'delete', 'backspace'
]
modifiers = [
    "shift", "ctrl", 'alt'
]

spaced = False


def updateJSON():
    file = open("words.json", mode="w")
    file.write(json.dumps(words))

    file = open("endings.json", mode="w")
    file.write(json.dumps(endings))


def modifierDown():
    for mod in modifiers:
        if keyboard.is_pressed(mod):
            return True

    return False


def initJSON():
    global words
    global endings

    if isfile(getcwd() + "\\words.json") and isfile(getcwd() + "\\endings.json"):
        with open("words.json", mode="r") as read:
            words = json.load(read)

        with open("endings.json", mode="r") as read:
            endings = json.load(read)


def onKey(event):
    global curWord
    global words
    global spaced

    if not event.name.lower() in allowedWords:
        return

    mod = modifierDown()
    if event.name.lower() == 'space' or (event.name.lower() == 'enter' and not mod):
        if spaced:
            spaced = False

        if curWord == '':
            return

        words.append(curWord)
        endings.append(event.name.lower())
        curWord = ''
    elif event.name.lower() == 'delete' or event.name.lower() == 'backspace':
        if curWord != '':
            curWord = curWord[:-1]
        else:
            if len(words) == 0:
                return

            if endings[(len(words) - 1)] == "enter":
                return

            if spaced:
                curLen = len(words)
                words[(len(words) - 1)] = words[(len(words) - 1)][:-1]

                if words[(len(words) - 1)] == '':
                    spaced = False
                    words.remove('')
            else:
                spaced = True
    elif mod:
        return
    else:
        curWord += event.name

    print(curWord, words)
    updateJSON()


def main():
    initJSON()
    keyboard.on_press(onKey)

    while True:
        pass


main()
