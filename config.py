import sys
import os
import json

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

RUN = True

FPS: int = 60

WIDTH: int = 1200
HEIGHT: int = 800

WIDTHCENTER: int = int(WIDTH/2)
HEIGHTCENTER: int = int(HEIGHT/2)

SAVEFILE: str = 'save.csv'

with open(resource_path('assets/words.json'), 'r') as wordfile:
    data = wordfile.read()
WORDS: list = json.loads(data)['data']


