# class for each tetrominos
import random
"""class Tetrominoes:
    def __init__(self):
        pass
    
    # 7 different Tetrominoes
    # L ___| 
    def orange_ricky(self):
        pass

    # J |___
    def blue_ricky(self):
        pass

    # I _____ light blue
    def hero(self):
        pass

    # T __|__ purple
    def teewee(self):
        pass

    # O [] yellow
    def smashboy(self):
        pass

    # Z -|_ red
    def cleveland_z(self):
        pass

    # S _|- green
    def rhode_island_z(self):
        pass

    def get_random_tetrominoes(self):
        pass
"""
class Tetrominoes:
    x = 0
    y = 0

    """
    Figure-matrix:
    0   1   2   3
    4   5   6   7
    8   9   10  11
    12  13  14  15
    """
    # they should all have 4 positions, except block
    Tetrominoes = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],  # Gerade
        [[1, 2, 5, 9], [4, 5, 6, 10], [1, 5, 9, 8], [0, 4, 5, 6]],  # Rev L
        [[1, 2, 6, 10], [3, 5, 6, 7], [2, 6, 10, 11], [5, 6, 7, 9]],  # L
        [[1, 2, 5, 6]],  # BLOCK
        [[6, 7, 9, 10], [1, 5, 6, 10]],  # S
        [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]],  # T
        [[4, 5, 9, 10], [2, 6, 5, 9]],  # Reverse S
    ]
    colors = [
                (0,0,0),       # space holder
                (0,240,240),   # I
                (0,0,240),     # J
                (240,0,160),   # L
                (0,240,0),     # S
                (240, 240, 0), # O
                (160,0,240),   # T
                (240,0,0)      # Z
            ]

    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord
        self.type = random.randint(0, len(self.Tetrominoes) - 1)
        self.rotation = 0
        self.color = self.colors[self.type + 1]

    def image(self):
        return self.Tetrominoes[self.type][self.rotation]

    def rotate_right(self):
        self.rotation = (self.rotation + 1) % len(self.Tetrominoes[self.type])

    def rotate_left(self):
        self.rotation = (self.rotation - 1) % len(self.Tetrominoes[self.type])


