import pygame
import os
import random
from PerlinNoise import *
import PIL.Image

FPS = 50
WIDTH = 800
HEIGHT = 600
STEP = 10
SIZE_WINDOW = WIDTH, HEIGHT
SIZE_MAP = 100, 100
TILE_WIDTH = 20
RES_MAP = 5
RES_RUD = 2

all_sprites = pygame.sprite.Group()
block_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
rud_group = pygame.sprite.Group()
moveable_entity_group = pygame.sprite.Group()

pygame.init()
pygame.key.set_repeat(200, 70)
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


class Entity(pygame.sprite.Sprite):
    def __init__(self, *alls):
        super().__init__(*alls)


class Block(Entity):
    def __init__(self, block_type, pos_x, pos_y, dop_group=block_group):
        super(Block, self).__init__(all_sprites, block_group, dop_group)
        self.image = tile_images[block_type]
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_WIDTH * pos_y)


class MoveableEntity(Entity):
    def __init__(self, moveable_entity_group, pos_x, pos_y):
        super(MoveableEntity, self).__init__(all_sprites, moveable_entity_group)
        self.cords = [pos_x, pos_y]
        self.mask = None
        self.rect = None

    def remove_cord_ox(self, step):
        self.rect.x += step
        for i in wall_group:
            if pygame.sprite.collide_mask(self, i):
                self.rect.x -= step
                return False
        return True

    def remove_cord_oy(self, step):
        self.rect.y += step
        for i in wall_group:
            if pygame.sprite.collide_mask(self, i):
                self.rect.y -= step
                return False
        return True


class Player(MoveableEntity):
    def __init__(self, pos_x, pos_y):
        super(Player, self).__init__(player_group, pos_x, pos_y)
        self.image = tile_images['mar']
        self.mask = pygame.mask.from_surface(self.image)
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_WIDTH * pos_y)

    def remove_cord(self, step, paral):
        st = 1 if step > 0 else -1
        if paral == 'ox':  # колво пикселей в человечке подредачь потом
            if 0 <= self.cords[0] + st <= SIZE_MAP[0] - 1 and self.remove_cord_ox(step):
                self.cords[0] += st
                self.rect.x += step
        else:
            if 0 <= self.cords[1] + st <= SIZE_MAP[1] - 2 and self.remove_cord_oy(step):
                self.cords[1] += st
                self.rect.y += step


class GeneratePlay:
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
            return Block('fon', x, y)
        elif n == 170:
            return Block('wall', x, y, dop_group=rud_group)
        else:
            return Block('omeg', x, y, dop_group=wall_group)

    # настройка внешнего вида
