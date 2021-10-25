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

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.font.init()

MYFONT = pygame.font.Font(resource_path('assets/Nunito-Regular.ttf'), 24)

BACKGROUND = pygame.image.load(resource_path('assets/1.jpg'))

BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

with open(resource_path('assets/words.json'), 'r') as wordfile:
    data = wordfile.read()
words = json.loads(data)['data']


