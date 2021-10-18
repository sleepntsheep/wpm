import pygame
import time
import json
import math
import random
import sys
import os
import csv
import datetime

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

with open(resource_path('assets/words.json'), 'r') as wordfile:
    data = wordfile.read()
words = json.loads(data)['data']


class Player:
    def __init__(self):
        self.score = 0
        self.missed = 0
        self.input = ''
        self.key = None
        self.speed = 1000
        self.time = 0
        self.wpm = 0
        self.acc = 0.1
        self.health = 10


class Word:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y


class GameState():
    def __init__(self):
        self.state = 'intro'

    def intro(self):
        global RUN
        WIN.blit(BACKGROUND, (0, 0))
        starttext = TITLEFONT.render(
            'Start Game', True, (0, 0, 0), (255, 255, 255))
        quittext = TITLEFONT.render('Quit', True, (0, 0, 0), (255, 255, 255))
        WIN.blit(starttext, (WIDTH/2, HEIGHT/2 - 150))
        WIN.blit(quittext, (WIDTH/2, HEIGHT/2 + 150))
        stwidth, stheight = starttext.get_width(), starttext.get_height()
        qtwidth, qtheight = quittext.get_width(), quittext.get_height()
        pygame.display.update()
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH/2 <= mouse[0] <= WIDTH/2 + stwidth and HEIGHT/2 - 150 <= mouse[1] <= HEIGHT/2 + stheight - 150:
                    self.starttime = pygame.time.get_ticks()
                    self.state = 'main_game'
                elif WIDTH/2 <= mouse[0] <= WIDTH/2 + qtwidth and HEIGHT/2 + 150 <= mouse[1] <= HEIGHT/2 + qtheight + 150:
                    RUN = 0
            elif event.type == pygame.QUIT:
                RUN = 0

    def main_game(self):
        global RUN

        WIN.blit(BACKGROUND, (0, 0))
        
        if player.health < 1:
            safegame(player, 'save.csv')
            self.state = 'gameover'

        while len(onscreen) < 10:
            onscreen.append(Word(random.choice(words), random.randint(1, 200), random.randint(1, HEIGHT - 100)))

        for word in onscreen:
            word.x += player.speed / 1000
            if word.x > WIDTH:
                onscreen.remove(word)
                player.health -= 1
            WIN.blit(MYFONT.render(word.text, 1, (0, 0, 0)),
                     (int(word.x), word.y))

        player.time = (pygame.time.get_ticks() - self.starttime) / 1000
        player.wpm = int((player.score) / (player.time / 60))

        pygame.draw.rect(BACKGROUND, (240, 240, 240),
                         pygame.Rect(0, HEIGHT-70, WIDTH, 70))

        WIN.blit(MYFONT.render(
            f'count:{player.score}, wpm:{player.wpm}, HP:{player.health}, T:{round(player.time, 2)}, [{player.input}]', 1, (0, 0, 0)), (10, HEIGHT-60))

        pygame.display.update()

        player.speed += player.acc

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                player.key = event.key
                if event.key == 8:  # backspace
                    player.input = player.input[:-1]
                elif event.key == 32 or event.key == 13:  # spacebar
                    found = 0
                    for word in onscreen:
                        if word.text == player.input:
                            found = 1
                            break
                    if found:
                        onscreen.remove(word)
                        player.input = ''
                        player.score += 1
                    else:
                        player.input = ''
                elif event.key == 27: # esc
                    safegame(player, 'save.csv')
                    self.state = 'gameover'
                else:
                    player.input += event.unicode
            elif event.type == pygame.QUIT:
                RUN = False
                break

    def gameover(self):
        global RUN, player
            
        WIN.blit(BACKGROUND, (0, 0))
        gameovertext = TITLEFONT.render('Game over', True, (0, 0, 0), (255, 255, 255))
        starttext = TITLEFONT.render(
            'Restart', True, (0, 0, 0), (255, 255, 255))
        quittext = TITLEFONT.render('Quit', True, (0, 0, 0), (255, 255, 255))
        
        stwidth, stheight = starttext.get_width(), starttext.get_height()
        qtwidth, qtheight = quittext.get_width(), quittext.get_height()
        gowidth, goheight = gameovertext.get_width(), gameovertext.get_height()
        
        WIN.blit(starttext, (WIDTH - 500, HEIGHT - 100))
        WIN.blit(quittext, (WIDTH - 200, HEIGHT - 100))
        WIN.blit(gameovertext, (WIDTH/2 - gowidth/2, HEIGHT/2 - goheight/2))
        
        pygame.draw.rect(BACKGROUND, (240, 240, 240),
                         pygame.Rect(0, HEIGHT-70, WIDTH, 70))

        WIN.blit(MYFONT.render(
            f'count:{player.score}, wpm:{player.wpm}, HP:{player.health}, T:{round(player.time, 2)}, [{player.input}]', 1, (0, 0, 0)), (10, HEIGHT-60))

        pygame.display.update()
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH - 500 <= mouse[0] <= WIDTH - 500 + stwidth and HEIGHT - 100 <= mouse[1] <= HEIGHT - 100 + stheight:
                    self.starttime = pygame.time.get_ticks()
                    player = Player()
                    self.state = 'main_game'
                elif WIDTH - 200 <= mouse[0] <= WIDTH - 200 + qtwidth and HEIGHT - 100 <= mouse[1] <= HEIGHT - 100 + qtheight:
                    RUN = 0
            elif event.type == pygame.QUIT:
                RUN = 0

    def state_manager(self):
        if self.state == 'intro':
            self.intro()
        elif self.state == 'main_game':
            self.main_game()
        elif self.state == 'gameover':
            self.gameover()


def safegame(player, filename):
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a') as csvfile:
        fieldnames = ['time', 'survived', 'wpm', 'score']
        writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()  # file doesn't exist yet, write a header
        writer.writerow({
            'time': datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
            'survived': player.time,
            'wpm': player.wpm,
            'score': player.score})

player = Player()
game_state = GameState()

BACKGROUND = pygame.image.load(resource_path('assets/bg.jfif'))
WIDTH, HEIGHT = BACKGROUND.get_width(), BACKGROUND.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
RUN = 1
FPS = 60
pygame.font.init()
MYFONT = pygame.font.Font(resource_path('assets/CozetteVector.ttf'), 30)
TITLEFONT = pygame.font.Font(resource_path('assets/CozetteVector.ttf'), 60)

pygame.display.set_caption("Typing of the dead")
clock = pygame.time.Clock()
onscreen = []

def main():
    while RUN:
        game_state.state_manager()
        clock.tick(FPS)
    pygame.quit()

if __name__ == '__main__':
    main()
