from Tetrominoes import Tetrominoes
import copy
import pygame
class Tetris:
    Tetrominoes = None
    def __init__(self, _height, _width):
        self.height = _height
        self.width = _width
        #self.field = [[0]*_width]*_height
        self.hold_figure = None
        self.Tetrominoes = None
        self.field = []
        self.score = 0
        self.level = 1
        self.counter = 0
        self.hold_counter = 0
        self.hold_draw = False
        self.state = "start"
        self.hold_bool = False
        for _ in range(_height):
            new_line = []
            for _ in range(_width):
                new_line.append(0)
            self.field.append(new_line)
        self.new_figure()
        self.new_shadow()

    
    def new_figure(self):
        if self.counter == 0:
            self.next_figure = Tetrominoes(3, 0)
            self.counter += 1

        if self.hold_bool:
            self.hold_figure.x = 3
            self.hold_figure.y = 0
            self.Tetrominoes = self.hold_figure
            self.hold_bool = False
            self.hold_draw = False
        else: 
            self.Tetrominoes = self.next_figure
            self.next_figure = Tetrominoes(3, 0)

        if not self.hold_bool and self.intersects(self.Tetrominoes):
            self.state = "gameover"
            return


    def pause(self, screen):
        paused = True
        pygame.mixer.music.pause()
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                        pygame.mixer.music.unpause()
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
            screen.fill((255, 255, 255))
            pause_font = pygame.font.SysFont("Calibri", 65, False, False)
            pause2_font = pygame.font.SysFont("Calibri", 20, False, False)
            text_pause = pause_font.render("Pause", True, (0, 0, 0))
            text_pause2 = pause2_font.render("Press C to continue or Q to quit", True, (0, 0, 0))
            screen.blit(text_pause, [300,250])
            screen.blit(text_pause2, [250,330])
            pygame.display.update()

    def game_over(self, screen, mixer):
        end = False
        while not end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            gameover_font = pygame.font.SysFont("Calibri", 65, True, False)
            text_gameover = gameover_font.render("Game Over!", True, (255, 0, 245))
            score_font = pygame.font.SysFont("Calibri", 50, False, False)
            text_score = score_font.render("your score: " + str(self.score), True, (255, 0, 245))
            q_font = pygame.font.SysFont("Calibri", 30, False, False)
            text_q = q_font.render("Press Q to quit", True, (255, 0, 245))
            screen.fill((0,0,0))
            screen.blit(text_score, [230, 330])
            screen.blit(text_gameover, [220, 250])
            screen.blit(text_q, [290, 400])
            pygame.display.update()

    def new_shadow(self):
        self.shadow = copy.copy(self.Tetrominoes)
        intersection = False
        while not intersection:
            self.shadow.y += 1
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in self.shadow.image():
                        if (i + self.shadow.y  > self.height - 1  or self.field[i + self.shadow.y ][j + self.shadow.x] > 0 ):
                            intersection = True
        self.shadow.y -= 1
        return self.shadow.y 

    def move_down(self):
        self.Tetrominoes.y += 1
        if self.intersects():
            self.Tetrominoes.y -= 1
            self.freeze()
   
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
            self.score += 2
        self.Tetrominoes.y -= 1
        self.freeze()

    def soft_drop(self):
        old_tetro = self.Tetrominoes.y
        self.Tetrominoes.y += 1
        if self.intersects():
            self.Tetrominoes.y = old_tetro
        self.score += 1

    def rotate_right(self):
        old_rotation = self.Tetrominoes.rotation
        self.Tetrominoes.rotate_right()
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Tetrominoes.image():
                    if j + self.Tetrominoes.x > self.width - 1 or j + self.Tetrominoes.x < 0:
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
        if self.hold_counter == 0:
            self.hold_bool = False
            self.hold_draw = True
            self.hold_figure = copy.copy(self.Tetrominoes)
            self.Tetrominoes = None
            self.new_figure()
            self.hold_counter += 1
        else:
            self.hold_bool = True
            self.hold_counter = 0

    def level_up(self):
        if (self.score + 1) % (100 * self.level) == 0:
            self.level += 1
            
    def intersects(self, fig=None):
        """
        checks if the tetrominoes collides with the bottom or another figure
            Attr:
                fig(object): Is an object of the class Tetrominoes (default is none)
            Returns:
                True if fig collides with the bottom or another figure
        """
        fig = self.Tetrominoes if (fig is None) else fig
        intersection = False
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in fig.image():
                    if (
                        i + fig.y > self.height - 1  # bottom intersection
                        or self.field[i + fig.y][j + fig.x] > 0 # figure intersection
                    ):
                        intersection = True
        return intersection

    def freeze(self):
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Tetrominoes.image():
                    self.field[i + self.Tetrominoes.y][j + self.Tetrominoes.x] = (self.Tetrominoes.type + 1)
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

        self.score += lines ** 2 * self.level