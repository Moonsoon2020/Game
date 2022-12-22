import sys

import pygame
import random
from PerlinNoise import *
import PIL.Image
import os

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 500
WIDTH = 800
HEIGHT = 600
STEP = 10
SIZE_WINDOW = WIDTH, HEIGHT
SIZE_MAP = 500, 500
TILE_WIDTH = 20
RES_MAP = 20
RES_RUD = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


tile_images = {'wall': load_image('rud20.png'), 'fon': load_image('fon/fon20.png'), 'omeg': load_image('sten.png'),
               'mar': load_image('mar.png')}
player_image = load_image('mar.png')

player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_WIDTH * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x + 15, TILE_WIDTH * pos_y + 5)


class Camera:
    # зададим начальный сдвиг камеры и размер поля для возможности реализации циклического сдвига
    def __init__(self, x, y):
        self.dx = x
        self.dy = y

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        # вычислим координату клетки, если она уехала влево за границу экрана
        # if obj.rect.x < -obj.rect.width:
        #     obj.rect.x += (self.field_size[0] + 1) * obj.rect.width
        # вычислим координату клетки, если она уехала вправо за границу экрана
        # if obj.rect.x >= (self.field_size[0]) * obj.rect.width:
        #     obj.rect.x += -obj.rect.width * (1 + self.field_size[0])
        obj.rect.y += self.dy
        # вычислим координату клетки, если она уехала вверх за границу экрана
        # if obj.rect.y < -obj.rect.height:
        #     obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
        # вычислим координату клетки, если она уехала вниз за границу экрана
        # if obj.rect.y >= (self.field_size[1]) * obj.rect.height:
        #     obj.rect.y += -obj.rect.height * (1 + self.field_size[1])

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


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
                a.append(self.enterprited((int((self.getcolor(self.board[y][x][0], 0) + 1) / 2 * 255 + 0.5) +
                                           int((self.getcolor(self.board[y][x][0], 0) + 1) / 2 * 255 + 0.5) +
                                           int((self.getcolor(self.board[y][x][1], 1) + 1) / 2 * 255 + 0.5)) // 3, x,
                                          y))
            board_new.append(a)
        img.save("pr3.png")
        self.board = board_new

    # 170 руда
    # 212 стены
    # 255 белый
    # 128 серый
    def getcolor(self, color, ind):
        if ind == 0:
            return 1 if color > 0.3 else 0
        else:
            return 1 if color > 0.6 else 0

    def enterprited(self, n, x, y):
        if n == 128:
            return Tile('fon', x, y)
        elif n == 170:
            return Tile('wall', x, y)
        else:
            return Tile('omeg', x, y)

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


camera = Camera(random.randint(0, SIZE_MAP[0]), random.randint(0, SIZE_MAP[1]))
player = Player(camera.dx, camera.dy)

if __name__ == '__main__':
    board = Board(SIZE_MAP[0], SIZE_MAP[1])
    cord = random.randint(0, SIZE_MAP[0]), random.randint(0, SIZE_MAP[1])
    clock = pygame.time.Clock()


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.rect.x -= STEP
                if event.key == pygame.K_RIGHT:
                    player.rect.x += STEP
                if event.key == pygame.K_UP:
                    player.rect.y -= STEP
                if event.key == pygame.K_DOWN:
                    player.rect.y += STEP

        camera.update(player)

        for sprite in all_sprites:
            camera.apply(sprite)

        screen.fill(pygame.Color(0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)
