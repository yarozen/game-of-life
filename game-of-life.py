import sys
from itertools import cycle
from random import random

import pygame as pg

# Colors
BLACK = (0, 0, 0)
GREY = (60, 60, 60)
LIGHT_GREY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
CELL_COLORS = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN]

# Fonts
FONTSIZE = 15
FONT = 'courier new'

# Game settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "Conway's Game of Life"
TILESIZES = cycle([8, 16, 32, 64])
TILESIZE = next(TILESIZES)
GENERATIONS_PER_SECOND = 20
RANDOM_CHANCE_TO_ALIVE_CELL = 0.3

# Mouse buttons
LEFT = 0
RIGHT = 2


class Cell(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.off()

    def off(self, color=BLACK):
        self.alive = False
        self.image.fill(color)

    def on(self, color=WHITE):
        self.alive = True
        self.image.fill(color)
        self.color = color

    def survive(self):
        r, g, b = self.color
        if r != 255:
            r += 5
        if g != 255:
            g += 5
        if b != 255:
            b += 5
        self.color = (r, g, b)
        self.image.fill(self.color)


class Game:
    def __init__(self):
        pg.init()
        pg.font.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.new_generation_event = pg.USEREVENT+1
        pg.time.set_timer(self.new_generation_event, int(1000/GENERATIONS_PER_SECOND))

        self.menu_font = pg.font.SysFont(FONT, FONTSIZE)

    def new(self):
        self.gridwidth = int(WIDTH / TILESIZE)
        self.gridheight = int(HEIGHT / TILESIZE)
        self.pause = True
        self.show_menu = True
        self.show_grid = True
        self.colors = cycle(CELL_COLORS)
        self.color = next(self.colors)
        self.gps = GENERATIONS_PER_SECOND
        self.all_sprites = pg.sprite.Group()
        self.cells = []
        for x in range(self.gridwidth):
            self.cells.append([])
            for y in range(self.gridheight):
                self.cells[x].append(Cell(self, x, y))
        self.previous_click, self.previous_x, self.previous_y = None, None, None

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.events()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, GREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, GREY, (0, y), (WIDTH, y))

    def blit(self, position, text, color=LIGHT_GREY):
        self.screen.blit(self.menu_font.render(text, False, color), (FONTSIZE, FONTSIZE*position))

    def draw_menu(self):
        self.blit(0, f"{TITLE}")
        self.blit(1, f"   F1:  Show / Hide menu")
        self.blit(2, f"space:  Run / Pause {'(paused)' if self.pause else '(running)'}")
        self.blit(3, f"    c:  New cell color", self.color)
        self.blit(4, f"    g:  Show / Hide grid {'(shown)' if self.show_grid else '(hidden)'}")
        self.blit(5, f"  +|-:  Generations per second ({self.gps})")
        self.blit(6, f"    r:  Randomize new cells")
        self.blit(7, f"    t:  Tiles {self.gridwidth}x{self.gridheight} ({self.gridwidth*self.gridheight})")
        self.blit(8, f"  LMB:  Turn on dead cell")
        self.blit(9, f"  RMB:  Turn off living cell")
        self.blit(10, f"    e:  Reset game")
        self.blit(11, f"ESC|q:  Quit")
        self.blit(int(HEIGHT/FONTSIZE) - 1, f"Developed by Yaniv Rozenboim")

    def draw(self):
        self.all_sprites.draw(self.screen)
        if self.show_grid:
            self.draw_grid()
        if self.show_menu:
            self.draw_menu()
        pg.display.flip()

    def randomize(self, chance_for_alive_cell=RANDOM_CHANCE_TO_ALIVE_CELL):
        for x in range(self.gridwidth):
            for y in range(self.gridheight):
                if random() < chance_for_alive_cell:
                    self.cells[x][y].on(self.color)
                else:
                    self.cells[x][y].off()

    def new_generation(self):
        temp = []
        for x in range(self.gridwidth):
            temp.append([])
            for y in range(self.gridheight):
                prev_x = x-1
                prev_y = y-1
                next_x = (x+1) % self.gridwidth
                next_y = (y+1) % self.gridheight
                value = \
                    self.cells[prev_x][prev_y].alive + \
                    self.cells[prev_x][y].alive + \
                    self.cells[prev_x][next_y].alive + \
                    self.cells[x][prev_y].alive + \
                    self.cells[x][next_y].alive + \
                    self.cells[next_x][prev_y].alive + \
                    self.cells[next_x][y].alive + \
                    self.cells[next_x][next_y].alive
                if self.cells[x][y].alive:
                    if value < 2 or value > 3:
                        temp[x].append(False)
                    else:
                        temp[x].append(True)
                else:
                    if value == 3:
                        temp[x].append(True)
                    else:
                        temp[x].append(False)
        for x in range(self.gridwidth):
            for y in range(self.gridheight):
                if temp[x][y]:
                    if self.cells[x][y].alive:
                        self.cells[x][y].survive()
                    else:
                        self.cells[x][y].on(self.color)
                else:
                    if self.cells[x][y].alive:
                        self.cells[x][y].off(BLACK)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                    self.quit()
                if event.key == pg.K_SPACE:
                    self.pause = not(self.pause)
                if event.key == pg.K_F1:
                    self.show_menu = not(self.show_menu)
                if event.key == pg.K_g:
                    self.show_grid = not(self.show_grid)
                if event.key == pg.K_r:
                    self.randomize()
                if event.key == pg.K_c:
                    self.color = next(self.colors)
                if event.key == pg.K_e:
                    self.new()
                if event.key == pg.K_t:
                    global TILESIZE
                    TILESIZE = next(TILESIZES)
                    self.new()
                if event.unicode == "+":
                    if self.gps < FPS/2:
                        self.gps += 1
                        pg.time.set_timer(self.new_generation_event, int(1000/self.gps))
                if event.unicode == "-":
                    if self.gps > 1:
                        self.gps -= 1
                        pg.time.set_timer(self.new_generation_event, int(1000/self.gps))

            click = pg.mouse.get_pressed()
            x, y = pg.mouse.get_pos()
            x = int(x / TILESIZE)
            y = int(y / TILESIZE)

            if (click, x, y) != (self.previous_click, self.previous_x, self.previous_y):
                self.previous_click, self.previous_x, self.previous_y = click, x, y
                if click[LEFT] and not self.cells[x][y].alive:
                    self.cells[x][y].on(self.color)
                elif click[RIGHT] and self.cells[x][y].alive:
                    self.cells[x][y].off(BLACK)
            if event.type == self.new_generation_event and not self.pause:
                self.new_generation()


g = Game()
while True:
    g.new()
    g.run()
