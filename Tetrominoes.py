# class for each tetrominos
import random
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
    Tetrominoes = [
        [[4, 5, 6, 7], [2, 6, 10, 14], [8, 9, 10, 11], [1, 5, 9, 13]], # I
        [[0, 4, 5, 6], [1, 2, 5, 9], [4, 5, 6, 10], [1, 5, 9, 8]],     # J
        [[4, 5, 6, 2], [1, 5, 9, 10], [8, 4, 5, 6], [0, 1, 5, 9]],     # L
        [[1, 2, 5, 6]],                                                # O
        [[4, 5, 1, 2], [1, 5, 6, 10], [8, 9, 5, 6], [0, 4, 5, 9]],     # S
        [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]],      # T
        [[0, 1, 5, 6], [2, 6, 5, 9], [4, 5, 9, 10], [1, 5, 4, 8]],     # Z
    ]

    colors = [
                (0,0,0),       # space holder
                (82,239,250),   # I
                (40,137,24),     # J
                (255,170,41),   # L
                (255, 236, 51), # O
                (53,240,78),     # S
                (166,36,252),   # T
                (252,36,58)      # Z
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