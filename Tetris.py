# class for Tetris
from Tetrominoes import Tetrominoes
import copy
import pygame
import random

class Tetris: 
    # bag indexes to randomly collect tetrominoes from bag
    bag_idx_list = [0,1,2,3,4,5,6]

    def __init__(self, _height, _width):
        """ Construction of game interface

        Args:
            _height (int): definition of the height of the game interface
            _width (int): definition of the width of the game interface
        """        
        self.height = _height
        self.width = _width
        self.hold_figure = None
        self.Tetrominoes = None
        self.next_figure = Tetrominoes(3, 0)
        self.next_type = self.bag()
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
        """ Construction of a new tetromino
        """      
        if self.hold_bool:
            # set start coordinates for the hold figure
            self.hold_figure.x, self.hold_figure.y  = 3, 0
            self.Tetrominoes = self.hold_figure
            self.tetromino_type = self.hold_type
            self.hold_bool = False
            self.hold_draw = False
        else: 
            self.Tetrominoes = self.next_figure
            self.tetromino_type = self.next_type
            self.next_figure = Tetrominoes(3, 0)
            # set the type for the new tetromino  
            self.next_type = self.bag()

        # if the figure collides with another figure instantly, the player loses
        if not self.hold_bool and self.intersects(self.Tetrominoes):
            self.state = "gameover"
            return
    
    def bag(self):
        """ Picking of a tetromino from the bag of tetrominoes

        Returns:
            int: the new type for the next tetromino. Number between 0 - 6.
        """
        # if there are no more tetrominoes in the bag, fill it up with each once
        if self.bag_idx_list == []:
            self.bag_idx_list = [0, 1, 2, 3, 4, 5, 6]
            random.shuffle(self.bag_idx_list)
            self.type = self.bag_idx_list[0]
            self.bag_idx_list.pop(0)
            return self.type
            
        # randomly pick one tetromino
        else: 
            random.shuffle(self.bag_idx_list)
            self.type = self.bag_idx_list[0]
            self.bag_idx_list.pop(0)
            return self.type
   
    def new_shadow(self):
        """ Construction of a shadow of the current tetromino at the bottom of games's screen

        Returns:
            int: y coordinate of the shadow with the same shape as the current tetromino
        """        
        self.shadow = copy.copy(self.Tetrominoes)
        intersection = False
        while not intersection:
            self.shadow.y += 1
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in self.shadow.image(self.tetromino_type):
                        if (i + self.shadow.y  > self.height - 1  or self.field[i + self.shadow.y ][j + self.shadow.x] > 0 ):
                            intersection = True
        self.shadow.y -= 1
        return self.shadow.y 
 
    def move_down(self):
        """ Moving down of tetromino
        """        
        self.Tetrominoes.y += 1
        if self.intersects():
            self.Tetrominoes.y -= 1
            self.freeze()
   
    def side(self, dx):
        """ Moving tetromino to right or left

        Args:
            dx (int): current x-coordinate of tetromino
        """        
        old_x = self.Tetrominoes.x
        edge = False
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Tetrominoes.image(self.tetromino_type):
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
        """ Moving tetromino to left
        """        
        self.side(-1)
    
    def right(self):
        """ Moving tetromino to the right
        """        
        self.side(1)
      
    def hard_drop(self):
        """ Hard drop of tetromino
        """        
        while not self.intersects():
            self.Tetrominoes.y += 1
            # update the score
            self.score += 2
        self.Tetrominoes.y -= 1
        self.freeze()
    
    def soft_drop(self):
        """ Soft drop of tetromino
        """        
        old_tetro = self.Tetrominoes.y
        self.Tetrominoes.y += 1
        if self.intersects():
            self.Tetrominoes.y = old_tetro
        # update the score
        self.score += 1

    def rotate_right(self):
        """ Rotation of tetromino to 90 degrees to the right.
        """        
        old_rotation = self.Tetrominoes.rotation
        self.Tetrominoes.rotate_right(self.tetromino_type)
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Tetrominoes.image(self.tetromino_type):
                    if j + self.Tetrominoes.x > self.width - 1 or j + self.Tetrominoes.x < 0:
                        self.Tetrominoes.rotation = old_rotation
        if self.intersects():
            self.Tetrominoes.rotation = old_rotation
        
    def rotate_left(self):
        """ Rotation of tetromino to 90 degrees to the left
        """        
        old_rotation = self.Tetrominoes.rotation
        self.Tetrominoes.rotate_left(self.tetromino_type)
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Tetrominoes.image(self.tetromino_type):
                    if j + self.Tetrominoes.x > self.width - 1 or \
                            j + self.Tetrominoes.x < 0:
                        self.Tetrominoes.rotation = old_rotation
        if self.intersects():
            self.Tetrominoes.rotation = old_rotation           

    def hold(self): 
        """ Placing one of the tetrominoes in the hold state to reactivate it later on
        """     
        if self.hold_counter <= 1:
            if self.hold_counter == 0:
                self.hold_bool = False
                self.hold_draw = True
                self.hold_figure = copy.copy(self.Tetrominoes)
                self.hold_type = self.tetromino_type
                self.Tetrominoes = None
                self.hold_counter += 1
                self.new_figure()
            else:
                self.hold_bool = True
                self.hold_counter += 1  
    
    def level_up(self):
        """ Increasing the current level when respective score thresholds are reached
        """        
        if (self.score + 1) % (100 * self.level) == 0:
            self.level += 1          
            
    def intersects(self, fig=None):
        """ Checking for collision with bottom of game and other tetrominoes

        Args:
            fig (_type_, optional): _description_. Defaults to None.???

        Returns:
            bool: Indication of whether intersection is there or not
        """  
        fig = self.Tetrominoes if (fig is None) else fig
        intersection = False
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in fig.image(self.tetromino_type):
                    if (
                        i + fig.y > self.height - 1  # bottom intersection
                        or self.field[i + fig.y][j + fig.x] > 0  # figure intersection
                    ):
                        intersection = True
        return intersection
    
    def freeze(self):
        """ Making the tetromino freeze a couple of seconds after it reached the ground
        """        
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Tetrominoes.image(self.tetromino_type):
                    self.field[i + self.Tetrominoes.y][j + self.Tetrominoes.x] = (self.tetromino_type + 1)
        self.break_lines()
        self.hold_counter = 0
        self.new_figure()
        
    def break_lines(self):
        """ Removing lines which are fully filled by tetrominoes
        """        
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
        
        # update score
        self.score += lines ** 2 * self.level

    def pause(self, screen):
        """ Pausing of the game

        Args:
            screen (<class 'pygame.Surface'>): game interface
        """        
        paused = True
        # pause the music
        pygame.mixer.music.pause()

        while paused:
            for event in pygame.event.get():
                # quit the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    # continue the game
                    if event.key == pygame.K_c:
                        paused = False
                        pygame.mixer.music.unpause()
                    # quit the game
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                        
            # display the pause screen
            screen.fill((255, 255, 255))
            pause_font = pygame.font.SysFont("Calibri", 65, False, False)
            pause2_font = pygame.font.SysFont("Calibri", 20, False, False)
            text_pause = pause_font.render("Pause", True, (0, 0, 0))
            text_pause2 = pause2_font.render("Press C to continue or Q to quit", True, (0, 0, 0))
            screen.blit(text_pause, [300,250])
            screen.blit(text_pause2, [250,330])
            pygame.display.update()

    def game_over(self, screen):
        """ Updating the screen when the game over state is reached

        Args:
            screen (<class 'pygame.Surface'>): game interface
        """        
        end = False
        while not end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
            # display the game over screen
            color = (255, 0, 245)
            gameover_font = pygame.font.SysFont("Calibri", 65, True, False)
            text_gameover = gameover_font.render("Game Over!", True, color)
            score_font = pygame.font.SysFont("Calibri", 50, False, False)
            text_score = score_font.render("your score: " + str(self.score), True, color)
            q_font = pygame.font.SysFont("Calibri", 30, False, False)
            text_q = q_font.render("Press Q to quit", True, color)
            screen.fill((0,0,0))
            screen.blit(text_score, [230, 330])
            screen.blit(text_gameover, [220, 250])
            screen.blit(text_q, [290, 400])
            pygame.display.update()

    def draw_background(self, screen, background, zoom):
        """ Updating the screen when the game over state is reached

        Args:
            screen (<class 'pygame.Surface'>): game interface
            bacground(png): background image
            zoom(int): determines the zoom of the grid
        """   
        screen.blit(background, (0,0))
        WHITE = (255,255,255)
        pygame.draw.rect(screen, WHITE, [225, 60, 300, 600], 1)
        
        # display the tetrominoes
        for i in range(self.height):
            for j in range(self.width):
                if self.field[i][j] > 0:
                    color = Tetrominoes.colors[self.field[i][j]] 
                    just_border = 0
                    pygame.draw.rect(
                        screen,
                        color,
                        [225 + j * zoom, 30 + i * zoom, zoom, zoom],
                        just_border,
                    )
                    color = (128,128,128)
                    just_border = 1
                    pygame.draw.rect(
                        screen,
                        color,
                        [225 + j * zoom, 30 + i * zoom, zoom, zoom],
                        just_border,
                    )
                
        # display moving tetromino
        if self.Tetrominoes is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in self.Tetrominoes.image(self.tetromino_type):
                        pygame.draw.rect(
                            screen,
                            self.Tetrominoes.get_color(self.tetromino_type),
                            [
                                225 + (j + self.Tetrominoes.x) * zoom,
                                30 + (i + self.Tetrominoes.y) * zoom,
                                zoom,
                                zoom,
                            ], 
                        )
                        color = (128,128,128)
                        just_border = 1
                        pygame.draw.rect(
                            screen,
                            color,
                            [
                                225 + (j + self.Tetrominoes.x) * zoom,
                                30 + (i + self.Tetrominoes.y) * zoom,
                                zoom,
                                zoom,
                            ],
                            just_border,
                        )
                        # draw the shadow
                        color = (255,255,255)
                        just_border = 1
                        pygame.draw.rect(
                            screen,
                            color,
                            [225 + (j + self.Tetrominoes.x) * zoom,
                            30 + (i + self.new_shadow()) * zoom, zoom, zoom],
                            just_border,
                        )

        # display the score
        score_font = pygame.font.SysFont("Calibri", 30, True, False)
        text_score = score_font.render("Score: " + str(self.score), True, WHITE)
        screen.blit(text_score, [20,40])

        # display the current level
        text_level = score_font.render("Level: " + str(self.level), True, WHITE)
        screen.blit(text_level, [20,80])

        # display the function hold
        hold_font = pygame.font.SysFont("Calibri", 50, True, False)
        text_hold = hold_font.render("Hold ", True, WHITE)
        screen.blit(text_hold, [65, 310])
        pygame.draw.rect(screen, WHITE, [40, 360, 150, 150], 1)
        if self.hold_draw:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in self.hold_figure.image(self.hold_type):
                        pygame.draw.rect(
                            screen,
                            self.hold_figure.get_color(self.hold_type),
                            [70 + j * zoom, 400 + i * zoom, zoom, zoom],
                            )
                        pygame.draw.rect(
                            screen,
                            (128,128,128),
                            [70 + j * zoom, 400 + i * zoom, zoom, zoom],
                            1,
                        )
    
        # display the function next
        text_next = hold_font.render("Next ", True, WHITE)
        screen.blit(text_next, [560,40])
        pygame.draw.rect(screen, WHITE, [535, 90, 150, 150], 1)
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.next_figure.image(self.next_type):
                    pygame.draw.rect(
                        screen,
                        self.next_figure.get_color(self.next_type),
                            [475 + (j + self.next_figure.x) * zoom, 130 + (i + self.next_figure.y) * zoom, zoom, zoom,],
                        )
                    pygame.draw.rect(
                        screen,
                        (128,128,128),
                        [475 + (j + self.next_figure.x) * zoom, 130 + (i + self.next_figure.y) * zoom, zoom, zoom,],
                        1,  
                    )

        # display pause
        pause_font = pygame.font.SysFont("Calibri", 20, True, False)
        text_pause = pause_font.render("Press P to pause", True, WHITE)
        screen.blit(text_pause, [550,350])
