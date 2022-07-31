import pygame as pg
from pygame.math import Vector2
from itertools import cycle
import random

WIDTH = 500
GRID = 20
CELLSIZE = WIDTH / GRID
FONT = 'fonts/DiloWorld.ttf'
APPLE_IMG = pg.transform.scale(pg.image.load('assets/apple.png'), (CELLSIZE, CELLSIZE))

BROWN = (130, 90, 44)
MAUVE = (118, 96, 138)
GREEN = (46, 204, 113)
PINK = (233, 30, 99)
YELLOW = (241, 196, 15)
VIOLET = (156, 39, 176)
CYAN = (27, 161, 226)
RED = (229, 20, 0)
TEAL = (0, 150, 136)
ORANGE = (230, 126, 34)

BGCOLORS = cycle([BROWN, MAUVE, TEAL])
SNAKECOLORS = cycle([CYAN, GREEN, VIOLET])


class Game:
    TIMER = {'easy': (200, 8000), 'normal': (150, 6000), 'hard': (100, 4000)}

    def __init__(self, title):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, WIDTH))
        self.clock = pg.time.Clock()

        self.title = title
        self.bgcolor = next(BGCOLORS)
        self.snake_color = next(SNAKECOLORS)
        self.snake_shape = 'circle'
        self.playing = False
        self.is_gameover = False
        self.level = 'easy'
        self.score = 0
        self.hi_score = 0
        self.snake_clk = 0
        self.apple_clk = 0
        self.snake = Snake(self.snake_shape, self.snake_color)
        self.apple = Food()

    def write(self, text, size, x, y, color):
        font = pg.font.Font(FONT, size)
        render_text = font.render(text, True, color)
        text_rect = render_text.get_rect()
        if x == 'center':
            x = WIDTH / 2 - text_rect.width / 2
        elif x == 'right':
            x = WIDTH - text_rect.width - 10
        elif x == 'left':
            x = 10
        if y == 'center':
            y = WIDTH / 2 - text_rect.height / 2
        self.screen.blit(render_text, (x, y))

    def change_theme(self):
        self.bgcolor = next(BGCOLORS)
        self.snake_color = next(SNAKECOLORS)
        self.snake.color = self.snake_color

    def change_shape(self):
        self.snake_shape = 'rect' if self.snake_shape == 'circle' else 'circle'
        self.snake.shape = self.snake_shape

    def change_level(self):
        if self.level == 'easy':
            self.level = 'normal'
        elif self.level == 'normal':
            self.level = 'hard'
        else:
            self.level = 'easy'

    def restart(self):
        self.snake = Snake(self.snake_shape, self.snake_color)
        self.apple = Food()
        self.playing = True
        self.is_gameover = False
        self.score = 0
        self.snake_clk = 0
        self.apple_clk = 0

    def display_startmenu(self):
        self.screen.fill(MAUVE)
        self.write(self.title, 72, 'center', 12, PINK)
        self.write(self.title, 70, 'center', 10, YELLOW)
        # Difficulty
        self.write('Difficulty', 30, 'center', 150, YELLOW)
        pg.draw.rect(self.screen, PINK, (WIDTH / 2 - 50, 200, 100, 30))
        self.write(f"<<     {self.level}     >>", 25, 'center', 200, 'white')
        # Theme Box
        self.write('Theme', 25, WIDTH / 2 - 195, 150, YELLOW)
        pg.draw.rect(self.screen, 'white', (WIDTH / 2 - 205, 180, 100, 85))
        pg.draw.rect(self.screen, self.bgcolor, (WIDTH / 2 - 200, 185, 90, 50))
        pg.draw.rect(self.screen, self.snake_color, (WIDTH / 2 - 200, 235, 90, 25))
        # Shape Shift
        self.write('Shape', 25, WIDTH / 2 + 120, 150, YELLOW)
        shape_box = pg.Rect(WIDTH / 2 + 125, 180, 60, 60)
        if self.snake_shape == 'circle':
            pg.draw.circle(self.screen, 'white', shape_box.center, 35)
            pg.draw.circle(self.screen, YELLOW, shape_box.center, 30)
        elif self.snake_shape == 'rect':
            pg.draw.rect(self.screen, 'white', shape_box)
            pg.draw.rect(self.screen, YELLOW,
                         (shape_box.x + 5, shape_box.y + 5, shape_box.width - 10, shape_box.height - 10))

        self.write('press [ SPACE ] to start', 30, 'center', WIDTH / 2 + 100, 'white')
        self.write('[T]-Theme      |       [D]-Difficulty     |       [S]-Shape', 20, 'center', WIDTH - 40, 'white')

    def display_gameover(self):
        self.screen.fill(RED)
        self.write('Gameover!', 72, 'center', 22, 'grey')
        self.write('Gameover!', 70, 'center', 20, 'white')
        pg.draw.rect(self.screen, 'white', (WIDTH / 2 - 120, WIDTH / 2 - 130, 240, 30))
        self.write('Scoreboard', 30, 'center', WIDTH / 2 - 128, ORANGE)
        pg.draw.rect(self.screen, 'white', (WIDTH / 2 - 120, WIDTH / 2 - 100, 240, 110), 5)
        self.write(f'Score: {self.score}', 40, 'center', WIDTH / 2 - 90, YELLOW)
        self.write(f'Highscore: {self.hi_score}', 35, 'center', WIDTH / 2 - 40, YELLOW)
        self.write('press [ SPACE ] to play again...', 30, 'center', WIDTH / 2 + 50, 'white')
        self.write('[M]-Main Menu', 30, 'center', WIDTH - 50, 'white')

    def draw(self):
        pg.display.set_caption(f'{self.title} (Mode: {self.level.upper()})')
        if not self.playing:
            self.display_startmenu()
            return
        if self.is_gameover:
            self.display_gameover()
            return

        self.screen.fill(self.bgcolor)
        self.snake.draw(self.screen)
        self.apple.draw(self.screen)
        self.write(f'Score: {self.score}', 30, 'left', 10, 'white')
        self.write(f'Best: {self.hi_score}', 30, 'right', 10, 'white')

    def control(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.snake.change_dir(0, -1)
        elif keys[pg.K_DOWN]:
            self.snake.change_dir(0, 1)
        elif keys[pg.K_LEFT]:
            self.snake.change_dir(-1, 0)
        elif keys[pg.K_RIGHT]:
            self.snake.change_dir(1, 0)

    def get_timer(self, index):
        return self.TIMER[self.level][index]

    def update(self):
        self.clock.tick(60)
        pg.display.update()
        if not self.playing or self.is_gameover:
            return

        now = pg.time.get_ticks()
        if now - self.snake_clk > self.get_timer(0):
            self.snake.move()
            self.snake_clk = now
        if now - self.apple_clk > self.get_timer(1):
            self.apple_clk = now
            self.apple.place_random()
            while self.apple.pos in self.snake.body:
                self.apple.place_random()

        if self.snake.body[0] == self.apple.pos:
            self.score += 1
            if self.score >= self.hi_score:
                self.hi_score = self.score
            self.snake.eat()
            self.apple_clk = now
            self.apple.place_random()
            while self.apple.pos in self.snake.body:
                self.apple.place_random()

        if self.snake.is_collision():
            self.is_gameover = True


class Snake:
    def __init__(self, shape, color):
        self.direction = Vector2(1, 0)  # Right
        self.body = [Vector2(10, 10), Vector2(9, 10), Vector2(8, 10)]
        self.shape = shape
        self.color = color

    def get_segment(self, i: int) -> pg.Rect:
        return pg.Rect(self.body[i].x * CELLSIZE,
                       self.body[i].y * CELLSIZE, CELLSIZE,
                       CELLSIZE)

    def draw(self, screen):
        if self.shape == 'circle':
            pg.draw.circle(screen, YELLOW, self.get_segment(0).center, CELLSIZE / 2)
            for i in range(1, len(self.body)):
                pg.draw.circle(screen, self.color, self.get_segment(i).center, CELLSIZE / 2)
        elif self.shape == 'rect':
            for i in range(len(self.body)):
                if i == 0:
                    pg.draw.rect(screen, YELLOW, self.get_segment(i))
                else:
                    pg.draw.rect(screen, self.color, self.get_segment(i))

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = self.body[i - 1].copy()
        self.body[0] += self.direction

    def change_dir(self, x, y):
        if self.direction.x == x or self.direction.y == y:
            return
        self.direction = Vector2(x, y)

    def eat(self):
        self.body.append(self.body[-1].copy())

    def is_collision(self):
        if 0 <= self.body[0].x < GRID and 0 <= self.body[0].y < GRID and self.body[0] not in self.body[1:]:
            return False
        return True


class Food:
    def __init__(self):
        self.x = 1000
        self.y = 1000

    @property
    def pos(self):
        return self.x, self.y

    def draw(self, screen):
        screen.blit(APPLE_IMG, (self.x * CELLSIZE, self.y * CELLSIZE))
        # pg.draw.circle(screen, 'red', (self.x * CELLSIZE + CELLSIZE // 2, self.y * CELLSIZE + CELLSIZE // 2),
        #                CELLSIZE / 2)

    def place_random(self):
        self.x, self.y = random.randrange(GRID), random.randrange(3, GRID)


def main():
    game = Game("Little Python")
    running = True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            if e.type == pg.KEYUP:
                if e.key == pg.K_SPACE:
                    if game.is_gameover or not game.playing:
                        game.restart()
                if e.key == pg.K_m:
                    if game.is_gameover:
                        game.playing = False
                if game.playing:
                    continue
                if e.key == pg.K_t:
                    game.change_theme()
                if e.key == pg.K_s:
                    game.change_shape()
                if e.key == pg.K_d:
                    game.change_level()

        game.control()
        game.update()
        game.draw()

    pg.quit()


if __name__ == '__main__':
    main()
