import keyboard
import subprocess
from time import sleep
import re
from pynput.keyboard import Controller, Key

keyboard = Controller()

timeout = 5

translate = {
    "Jay": "J",
    "Elle": "L",
    "Seven": "7",
    "El": "L",
    "Tri": "3",
    "Zero": "0",
    "One": "1",
    "Two": "2",
    "Three": "3",
    "Four": "4",
    "Five": "5",
}

print("Macbook Command MQTT Script")

def pressRelease(key):
    keyboard.press(key)
    keyboard.release(key)

def decodeWords(raw):
    if re.search(r"\w\d{1,2}", raw):
        key = re.search(r"^\w", raw)
        times = re.search(r"\d+", raw)
        for n in range(int(times.group())):
            pressRelease(key[0])
    elif re.search("Volume Up", raw, re.IGNORECASE):
        for n in range(2):
            pressRelease(Key.media_volume_up)
    elif re.search("Volume Down", raw, re.IGNORECASE):
        for n in range(2):
            pressRelease(Key.media_volume_down)
    elif re.search(r"\w+\s\w+", raw):
        tokens = raw.split()
        for token in tokens:
            for word in translate:
                if word == token:
                    key = word
    elif re.search(r"\w+", raw):
        for word in translate:
            if raw == word:
                pressRelease(translate[word])
    else:
        print("NO MATCH")


while True:
    raw = subprocess.run("mosquitto_sub -t mbp/key -C 1", shell=True, capture_output=True, text=True)
    command = raw.stdout
    command = command.strip()
    decodeWords(command)
    print(command)
    print("sleeping", timeout)
    sleep(timeout)
    
