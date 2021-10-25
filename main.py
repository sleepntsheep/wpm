# import time
# import json
# import math
# import sys
import os
import pygame
import random
import csv
import datetime
from config import *
# import pygame.gfxdraw

class Player:
    def __init__(self):
        self.score = 0
        self.missed = 0
        self.input = ''
        self.key = None
        self.speed = 1000
        self.time = 0
        self.wpm = 0
        self.acc = 0
        self.health = 10

class Button:
    def __init__(self, text:str, x:int, y:int, win, padding = 4, color=(0, 0, 0, 100), textcolor=(240, 240, 240)):
        self.text = text
        self.color = color
        self.padding = padding
        self.x = x - padding
        self.y = y - padding
        self.textcolor = textcolor
        self.draw(win)

    def draw(self, win):

        if self.text != '':
            text = MYFONT.render(self.text, 1, (self.textcolor))
            self.textwidth = text.get_width()
            self.textheight = text.get_height()

        self.nx = self.textwidth + 2 * self.padding
        self.ny = self.textheight + 2 * self.padding

        s = pygame.Surface((self.nx, self.ny), pygame.SRCALPHA)  
        s.fill(self.color)
        win.blit(s, (self.x - self.textwidth/2, self.y - self.textheight/2))
            
        win.blit(text, (self.x + self.padding - self.textwidth/2, self.y + self.padding - self.textheight/2))

    def isOver(self, pos):
        if self.nx - self.textwidth/2 + self.x > pos[0] > self.x - self.textwidth/2:
            if self.y - self.textheight/2 + self.ny > pos[1] > self.y - self.textheight/2:
                return True

class Game():
    def __init__(self):
        self.state = 'intro'
        self.onscreen = []
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('WPM')
        self.player = Player()

    def intro(self):
        global RUN
        WIN.blit(BACKGROUND, (0, 0))
        startbutton = Button('Start game', WIDTHCENTER, HEIGHTCENTER - 100, WIN, padding=10)
        quitbutton = Button('Quit game', WIDTHCENTER, HEIGHTCENTER, WIN, padding=10)

        pygame.display.update()
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if startbutton.isOver(mouse):
                    self.restart()
                elif quitbutton.isOver(mouse):
                    RUN = 0
            elif event.type == pygame.QUIT:
                RUN = 0

    def main_game(self):
        global RUN

        WIN.blit(BACKGROUND, (0, 0))
        
        if self.player.health < 1:
            self.safegame(self.player, 'save.csv')
            self.state = 'gameover'

        while len(self.onscreen) < 10:
            newword = [random.choice(words), random.randint(1, 200), random.randint(1, HEIGHT - 100)]
            self.onscreen.append(newword)

        for word in self.onscreen:
            word[1] += self.player.speed / 1000
            if word[1] > WIDTH:
                self.onscreen.remove(word)
                self.player.health -= 1
            if word[0].startswith(self.player.input):
                tt = MYFONT.render(self.player.input, 1, (0, 255, 0))
                tt2 = MYFONT.render(word[0][len(self.player.input):], 1, (240, 240, 240))
                WIN.blit(tt, (int(word[1]), word[2]))
                WIN.blit(tt2, (int(word[1]) + int(tt.get_width()), word[2]))
            else:
                WIN.blit(MYFONT.render(word[0], 1, (240, 240, 240)),
                    (int(word[1]), word[2]))

        self.player.time = (pygame.time.get_ticks() - self.starttime) / 1000
        self.player.wpm = int((self.player.score) / (self.player.time / 60))

        pygame.draw.rect(BACKGROUND, (240, 240, 240),
                         pygame.Rect(0, HEIGHT-40, WIDTH, 70))

        WIN.blit(MYFONT.render(
            f'count:{self.player.score}, wpm:{self.player.wpm}, HP:{self.player.health}, T:{round(self.player.time, 2)}, [{self.player.input}]', 1, (0, 0, 0)), (10, HEIGHT-35))

        pygame.display.update()

        self.player.speed += self.player.acc

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.player.key = event.key
                if event.key == pygame.K_BACKSPACE:  # backspace
                    self.player.input = self.player.input[:-1]
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:  # spacebar
                    found = 0
                    for word in self.onscreen:
                        if word[0] == self.player.input:
                            found = 1
                            break
                    if found:
                        self.onscreen.remove(word)
                        self.player.input = ''
                        self.player.score += 1
                    else:
                        self.player.input = ''
                elif event.key == pygame.K_ESCAPE: # esc
                    self.safegame(self.player, 'save.csv')
                    self.state = 'gameover'
                else:
                    self.player.input += event.unicode
            elif event.type == pygame.QUIT:
                RUN = False
                break

    def gameover(self):
        global RUN
            
        WIN.blit(BACKGROUND, (0, 0))

        restartbutton = Button('Restart', WIDTH-250, HEIGHT-20, WIN)
        quitbutton = Button('Quit', WIDTH-100, HEIGHT-20, WIN)
        gameover = Button('Gameover', WIDTHCENTER, HEIGHTCENTER, WIN)

        pygame.draw.rect(BACKGROUND, (240, 240, 240),
                         pygame.Rect(0, HEIGHT-40, WIDTH, 70))

        WIN.blit(MYFONT.render(
            f'count:{self.player.score}, wpm:{self.player.wpm}, HP:{self.player.health}, T:{round(self.player.time, 2)}, [{self.player.input}]', 1, (0, 0, 0)), (10, HEIGHT-35))

        pygame.display.update()
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restartbutton.isOver(mouse):
                    self.restart()
                elif quitbutton.isOver(mouse):
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
        elif self.state == 'result':
            pass
            
    def restart(self):
        self.player = Player()
        self.onscreen = []
        self.starttime = pygame.time.get_ticks()
        self.state = 'main_game'

    def safegame(self, player, filename):
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

    def run(self):
        while RUN:
            self.state_manager()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()