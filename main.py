import keyboard
import winreg as reg
import json
from os import getcwd, mkdir

num = None
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


def startup():
    key = reg.HKEY_CURRENT_USER
    key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    opened = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
    reg.SetValueEx(opened, "Typing Analyser", 0, reg.REG_SZ, __file__)
    reg.CloseKey(opened)


def updateJSON():
    file = open("JSONs\\{}\\words.json".format(num), mode="w")
    file.write(json.dumps(words))
    file.close()


#    file = open("JSONs\\{}\\endings.json".format(num), mode="w")
#    file.write(json.dumps(endings))
#    file.close()


def modifierDown():
    for mod in modifiers:
        if keyboard.is_pressed(mod):
            return True

    return False


def initNum():
    global num

    file = open("JSONs\\num.txt", mode="r")
    num = str(int(file.read()) + 1)
    file.close()

    file = open("JSONs\\num.txt", mode="w")
    file.write(num)
    file.close()

    mkdir(getcwd() + "\\JSONs\\{}".format(num))


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
    startup()
    initNum()
    keyboard.on_press(onKey)

    while True:
        pass


if __name__ == '__main__':
    main()
