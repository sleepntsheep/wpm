import os
import pygame
import random
import csv
import datetime
from config import *

class Player:
    def __init__(self):
        self.score: int = 0
        self.missed: int = 0
        self.input: str = ''
        self.key = None
        self.speed: int = 1000
        self.time: float = 0
        self.wpm: float = 0
        self.acc: float = 0.5
        self.health: int = 10

class Button:
    def __init__(self, text:str, x:int, y:int, win, font, padding = 4, color=(0, 0, 0, 100), textcolor=(240, 240, 240)):
        self.text = text
        self.color = color
        self.padding = padding
        self.x = x - padding
        self.y = y - padding
        self.textcolor = textcolor
        self.win = win
        self.font = font
        self.draw()

    def draw(self):
        if self.text == '':
            return

        text = self.font.render(self.text, 1, (self.textcolor))
        self.textwidth = text.get_width()
        self.textheight = text.get_height()

        self.nx = self.textwidth + 2 * self.padding
        self.ny = self.textheight + 2 * self.padding

        s = pygame.Surface((self.nx, self.ny), pygame.SRCALPHA)  
        s.fill(self.color)
        self.win.blit(s, (self.x - self.textwidth/2, self.y - self.textheight/2))
            
        self.win.blit(text, (self.x + self.padding - self.textwidth/2, self.y + self.padding - self.textheight/2))

    def isOver(self, pos):
        if self.nx - self.textwidth/2 + self.x > pos[0] > self.x - self.textwidth/2:
            if self.y - self.textheight/2 + self.ny > pos[1] > self.y - self.textheight/2:
                return True

class Word():
    def __init__(self):
        self.text = random.choice(WORDS)
        self.x = random.randint(0, 200)
        self.y = random.randint(0, HEIGHT - 100)

    def draw(self, win):
        ...


class Game():
    def __init__(self):
        self.state: str = 'intro'
        self.onscreen: list = []
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('WPM')
        self.player = Player()
        pygame.init()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.BACKGROUND = pygame.image.load(resource_path('assets/1.jpg'))
        self.BACKGROUND = pygame.transform.scale(self.BACKGROUND, (WIDTH, HEIGHT))

    def font(self, size=24):
        font = pygame.font.Font(resource_path('assets/Nunito-Regular.ttf'), size)
        return font


    def intro(self):
        global RUN
        self.WIN.blit(self.BACKGROUND, (0, 0))
        startbutton = Button('Start game', WIDTHCENTER, HEIGHTCENTER - 100, self.WIN, self.font(), padding=10)
        quitbutton = Button('Quit game', WIDTHCENTER, HEIGHTCENTER, self.WIN, self.font(), padding=10)

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

        self.WIN.blit(self.BACKGROUND, (0, 0))
        
        if self.player.health < 1:
            self.safegame(self.player, SAVEFILE)
            self.state = 'gameover'

        while len(self.onscreen) < 15:
            new_word: Word = Word()
            self.onscreen.append(new_word)

        for word in self.onscreen:
            word.x += self.player.speed / 1000
            if word.x > WIDTH:
                self.onscreen.remove(word)
                self.player.health -= 1
            if word.text.startswith(self.player.input):
                tt = self.font().render(self.player.input, True, (0, 255, 0))
                tt2 = self.font().render(word.text[len(self.player.input):], True, (240, 240, 240))
                self.WIN.blit(tt, (int(word.x), word.y))
                self.WIN.blit(tt2, (int(word.x) + int(tt.get_width()), word.y))
            else:
                self.WIN.blit(self.font().render(word.text, True, (240, 240, 240)),
                    (int(word.x), word.y))

        self.player.time = (pygame.time.get_ticks() - self.starttime) / 1000
        self.player.wpm = int((self.player.score) / (self.player.time / 60))

        pygame.draw.rect(self.BACKGROUND, (240, 240, 240),
                         pygame.Rect(0, HEIGHT-40, WIDTH, 70))

        self.WIN.blit(self.font().render(
            f'count:{self.player.score}, wpm:{self.player.wpm}, HP:{self.player.health}, T:{round(self.player.time, 2)}, [{self.player.input}]', True, (0, 0, 0)), (10, HEIGHT-35))

        pygame.display.update()

        self.player.speed += int(self.player.acc)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.player.key = event.key
                if event.key == pygame.K_BACKSPACE:  # backspace
                    self.player.input = self.player.input[:-1]
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:  # spacebar
                    found = 0
                    submit: str = self.player.input
                    for word in self.onscreen:
                        if word.text == submit:
                            self.onscreen.remove(word)
                            found = 1
                            break
                    if found:
                        self.player.input = ''
                        self.player.score += 1
                    else:
                        self.player.input = ''
                elif event.key == pygame.K_ESCAPE: # esc
                    self.safegame(self.player, SAVEFILE)
                    self.state = 'gameover'
                else:
                    self.player.input += event.unicode
            elif event.type == pygame.QUIT:
                RUN = False
                break

    def gameover(self):
        global RUN
            
        self.WIN.blit(self.BACKGROUND, (0, 0))

        restartbutton: Button = Button('Restart', WIDTH-250, HEIGHT-20, self.WIN, self.font())
        quitbutton: Button = Button('Quit', WIDTH-100, HEIGHT-20, self.WIN, self.font())
        gameover: Button = Button('Gameover', WIDTHCENTER, 100, self.WIN, self.font(50))

        pygame.draw.rect(self.BACKGROUND, (240, 240, 240),
                         pygame.Rect(0, HEIGHT-40, WIDTH, 70))

        self.WIN.blit(self.font().render(
            f'count:{self.player.score}, wpm:{self.player.wpm}, HP:{self.player.health}, T:{round(self.player.time, 2)}, [{self.player.input}]', True, (0, 0, 0)), (10, HEIGHT-35))

        with open(SAVEFILE, 'r') as f:
            lines = f.readlines()
        lines.sort(key=lambda x: int(float(x.split(',')[1])), reverse=True)
        for i, line in enumerate(lines):
            print(line)
            Button(line, WIDTHCENTER, 200 + i * 40, self.WIN, self.font(), textcolor = (240, 240, 240))
            if i > 9:
                break

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
                'survived': round(player.time, 2),
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
