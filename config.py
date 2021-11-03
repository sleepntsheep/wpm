import pygame
import sys
import os
import json

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

RUN = 1

FPS = 60

WIDTH, HEIGHT = 1200, 800

WIDTHCENTER, HEIGHTCENTER = WIDTH/2, HEIGHT/2

SAVEFILE = 'save.csv'

with open(resource_path('assets/words.json'), 'r') as wordfile:
    data = wordfile.read()
words = json.loads(data)['data']


