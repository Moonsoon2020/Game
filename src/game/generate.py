import random
from src.constans.gameconst import *
from src.game.PerlinNoise import PerlinNoiseFactory
from src.game.entity import Block, Wall

class GeneratePlay:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.noise_map = PerlinNoiseFactory(2, octaves=1, tile=(width // RES_MAP + 1, height // RES_MAP + 1))
        self.noise_rud = PerlinNoiseFactory(2, octaves=1, tile=(width // RES_RUD + 1, height // RES_RUD + 1))
        self.noise_biom = PerlinNoiseFactory(2, octaves=1, tile=(width // RES_BIOM + 1, height // RES_BIOM + 1))
        self.board = [[[self.noise_map(i / RES_MAP, j / RES_MAP),
                        self.noise_rud(i / RES_RUD, j / RES_RUD),
                        self.noise_biom(i / RES_BIOM, j / RES_BIOM)]
                       for i in range(width)] for j in range(height)]
        self.board = [[self.interpreted((int((self.get_color(self.board[y][x][0], 0) + 1) / 2 * 255 + 0.5) +
                                          int((self.get_color(self.board[y][x][0], 0) + 1) / 2 * 255 + 0.5) +
                                          int((self.get_color(self.board[y][x][1], 1) + 1) / 2 * 255 + 0.5)) // 3, x,
                                         y, int(self.get_color(self.board[y][x][2], 2)))
                        for x in range(width)] for y in range(height)]

    def get_color(self, color, ind):
        if ind == 0:
            return 1 if color > 0.25 else 0
        elif ind == 1:
            return 1 if color > 0.4 else 0
        else:
            return 1 if color > 0.2 else 2 if color > -0.2 else 0

    def interpreted(self, n, x, y, var):
        if var == 0:
            var = 'v1'
        elif var == 1:
            var = 'v2'
        elif var == 2:
            var = 'v3'
        if n == 128:
            return Block(var + 'fon', x, y, x, y, 'f', var)
        elif n == 170:
            return Block(var + 'rud', x, y, x, y, 'r', var, rud_group)
        else:
            return Wall(var, x, y, x, y, 200)

    # Замененный метод start_cord
    def start_cord(self):
        available_coords = [(x, y) for y in range(int(KOF_START * self.height), int(self.height * (1 - KOF_START)))
                            for x in range(int(KOF_START * self.width), int(self.width * (1 - KOF_START)))
                            if self.board[y][x] not in wall_group and self.board[y][x] not in rud_group]
        if not available_coords:
            return random.randint(int(KOF_START * self.width), int(self.width * (1 - KOF_START))), \
                   random.randint(int(KOF_START * self.height), int(self.height * (1 - KOF_START)))
        return random.choice(available_coords)

    def remove(self, tile, x, y):
        self.board[y][x].kill()
        self.board[y][x] = tile
