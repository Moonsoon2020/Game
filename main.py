import pygame
import random
from PerlinNoise import *
import PIL.Image

FPS = 50
WIDTH = 400
HEIGHT = 300
STEP = 10
SIZE_WINDOW = WIDTH, HEIGHT
SIZE_MAP = 500, 500
SIZE_MAP_IN_WINDOW = 12
RES_MAP = 60
RES_RUD = 10


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.noise_map = PerlinNoiseFactory(2, octaves=1, tile=(width // RES_MAP + 1, height // RES_MAP + 1))
        self.noise_rud = PerlinNoiseFactory(2, octaves=1, tile=(width // RES_RUD + 1, height // RES_RUD + 1))
        self.board = [[[self.noise_map(i / RES_MAP, j / RES_MAP),
                        self.noise_rud(i / RES_RUD, j / RES_RUD)]
                       for i in range(width)] for j in range(height)]
        board_new = []
        # значения по умолчанию
        self.left = 0
        self.top = 0
        self.cell_size = 10
        self.start = (0, 0)
        img = PIL.Image.new('RGB', (width, height))
        pix = img.load()
        for x in range(width):
            a = []
            for y in range(height):
                pix[x, y] = int((self.getcolor(self.board[y][x][0], 0) + 1) / 2 * 255 + 0.5), \
                            int((self.getcolor(self.board[y][x][0], 0) + 1) / 2 * 255 + 0.5), \
                            int((self.getcolor(self.board[y][x][1], 1) + 1) / 2 * 255 + 0.5)
                a.append((int((self.getcolor(self.board[y][x][0], 0) + 1) / 2 * 255 + 0.5) +
                         int((self.getcolor(self.board[y][x][0], 0) + 1) / 2 * 255 + 0.5) +
                         int((self.getcolor(self.board[y][x][1], 1) + 1) / 2 * 255 + 0.5)) // 3)
            board_new.append(a)
        img.save("pr3.png")
        self.board = board_new

    def getcolor(self, color, ind):
        if ind == 0:
            return 1 if color > 0.3 else 0
        else:
            return 1 if color > 0.5 else 0

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def render(self, hol, start, window):
        self.start = start
        for x in range(start[0], window[0]):
            for y in range(start[1], window[1]):
                if self.board[y][x] != 0:
                    pass
                    # pygame.draw.rect(hol, (0, 0, 200), ((j * self.cell_size + self.left, ч * self.cell_size + self.top), (self.cell_size, self.cell_size)), 1)
                else:
                    if self.board[y][x] == 10:
                        pygame.draw.rect(hol, (0, 200, 200),
                                         ((y * self.cell_size + self.left, x * self.cell_size + self.top),
                                          (self.cell_size, self.cell_size)))
                    else:
                        pygame.draw.rect(hol, (0, 0, 200),
                                         ((y * self.cell_size + self.left, x * self.cell_size + self.top),
                                          (self.cell_size, self.cell_size)))

    def get_cell(self, mouse_pos):
        pos = mouse_pos
        pos = pos[0] - self.left, pos[1] - self.top
        if 0 <= pos[0] / self.cell_size <= self.width and 0 <= pos[1] / self.cell_size <= self.height:
            return pos[0] // self.cell_size, pos[1] // self.cell_size
        else:
            return None

    def on_click(self, cell):
        if cell is not None:
            self.board[cell[1] - self.start[1]][cell[0] + self.start[0]] = \
                abs(self.board[cell[1] - self.start[1]][cell[0] + self.start[0]] - 1)

    def pers(self, x, y):
        self.board[y][x] = 10


if __name__ == '__main__':
    # инициализация Pygame:

    pygame.init()
    # размеры окна:
    board = Board(SIZE_MAP[0], SIZE_MAP[1])
    cord = random.randint(0, SIZE_MAP[0]), random.randint(0, SIZE_MAP[1])
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(SIZE_WINDOW)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render(screen, cord, (WIDTH // SIZE_MAP_IN_WINDOW, HEIGHT // SIZE_MAP_IN_WINDOW))
        pygame.display.flip()
        clock.tick(FPS)


print()
print()
print()
