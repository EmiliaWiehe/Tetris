# control of tetrominoes
# (music)
import pygame
from Tetrominoes import Tetrominoes
class Tetris:
    Tetrominoes = None
    def __init__(self, _height, _width):
        self.height = _height
        self.width = _width
        self.field = []
        self.score = 0
        self.level = 1
        self.counter = 0
        self.next_figure = None
        self.state = "start"
        self.paused = False
        for i in range(_height):
            new_line = []
            for j in range(_width):
                new_line.append(0)
            self.field.append(new_line)
        self.new_figure()

    
    def new_figure(self):
        if self.counter == 0:
            self.next_figure = Tetrominoes(3, 0)
            self.counter += 1
        curr_figure = self.next_figure      

        if self.intersects(curr_figure):
            self.state = "gameover"
            return
        self.Tetrominoes = curr_figure

        if self.counter > 0:
            self.next_figure = Tetrominoes(3, 0)

    def go_down(self):
        self.Tetrominoes.y += 1
        if self.intersects():
            self.Tetrominoes.y -= 1
            self.freeze()

    def go_up(self):
        self.Tetrominoes.y -= 1
            

    def side(self, dx):
        old_x = self.Tetrominoes.x
        edge = False
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Tetrominoes.image():
                    if (
                        j + self.Tetrominoes.x + dx > self.width - 1  # beyond right border
                        or j + self.Tetrominoes.x + dx < 0  # beyond left border
                    ):
                        edge = True
        if not edge:
            self.Tetrominoes.x += dx
        if self.intersects():
            self.Tetrominoes.x = old_x

    def left(self):
        self.side(-1)

    def right(self):
        self.side(1)

    def hard_drop(self):
        while not self.intersects():
            self.Tetrominoes.y += 1
        self.Tetrominoes.y -= 1
        self.freeze()

    def soft_drop(self):
        old_tetro = self.Tetrominoes.y
        self.Tetrominoes.y += 1
        if self.intersects():
            self.Tetrominoes.y = old_tetro

    def rotate_right(self):
        old_rotation = self.Tetrominoes.rotation
        self.Tetrominoes.rotate_right()
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Tetrominoes.image():
                    if j + self.Tetrominoes.x > self.width - 1 or \
                            j + self.Tetrominoes.x < 0:
                        self.Tetrominoes.rotation = old_rotation
        if self.intersects():
            self.Tetrominoes.rotation = old_rotation
        
    def rotate_left(self):
        old_rotation = self.Tetrominoes.rotation
        self.Tetrominoes.rotate_left()
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Tetrominoes.image():
                    if j + self.Tetrominoes.x > self.width - 1 or \
                            j + self.Tetrominoes.x < 0:
                        self.Tetrominoes.rotation = old_rotation
        if self.intersects():
            self.Tetrominoes.rotation = old_rotation

    def hold(self): 
            pass
            
    def intersects(self, fig=None):
        fig = self.Tetrominoes if (fig is None) else fig
        intersection = False
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in fig.image():
                    if (
                        i + fig.y > self.height - 1  # bottom intersection
                        # or i + fig.y < 0  #
                        or self.field[i + fig.y][j + fig.x] > 0 # figure intersection
                    ):
                        intersection = True
        return intersection

    def freeze(self):
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Tetrominoes.image():
                    self.field[i + self.Tetrominoes.y][j + self.Tetrominoes.x] = (
                        self.Tetrominoes.type + 1
                    )
        self.break_lines()
        self.new_figure()

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i2 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i2][j] = self.field[i2 - 1][j]
        # scoring system is not right
        # level() function is missing
        if (self.score + 1) % (2 * self.level) == 0:
                self.level += 1
        self.score += lines ** 2 * self.level