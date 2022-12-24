import random

import pygame
import os
from PerlinNoise import *
import PIL.Image
from ContolBD import ControlDataBase

FPS = 50
WIDTH = 800
HEIGHT = 600
STEP = 10
KOF_START = 0.25
KOF_ENEMY = 0.05
SIZE_WINDOW = WIDTH, HEIGHT
SIZE_MAP = 300, 300
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


def perep(name, x, y):
    if name == 'f':
        return Block('fon', x, y, 'f')
    elif name == 'r':
        return Block('rud', x, y, 'r', dop_group=rud_group)
    else:
        return Block('sten', x, y, 's', dop_group=wall_group)


def load_level(filename):
    ControlDataBase().del_world(filename)
    filename = "map/" + filename + '.txt'
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.split() for line in mapFile]

    board = [[perep(level_map[i][j], i, j) for j in range(len(level_map[i]))]for i in range(len(level_map))]
    os.remove(filename)
    return board


tile_images = {'rud': load_image('rud20.png'), 'fon': load_image('fon/fon20.png'), 'sten': load_image('sten.png'),
               'mar': load_image('mar.png')}


class Entity(pygame.sprite.Sprite):
    def __init__(self, *alls):
        super().__init__(*alls)


class Block(Entity):
    def __init__(self, block_type, pos_x, pos_y, station, dop_group=block_group):
        super(Block, self).__init__(all_sprites, block_group, dop_group)
        self.image = tile_images[block_type]
        self.station = station
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_WIDTH * pos_y)

    def __str__(self):
        return self.station


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
    def __init__(self, width, height, seed):
        self.width = width
        self.height = height
        random.seed(seed)
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
            return 1 if color > 0.25 else 0
        else:
            return 1 if color > 0.6 else 0

    def enterprited(self, n, x, y):
        if n == 128:
            return Block('fon', x, y, 'f')
        elif n == 170:
            return Block('rud', x, y, 'r', dop_group=rud_group)
        else:
            return Block('sten', x, y,  's', dop_group=wall_group)

    def start_cord(self):
        cord = random.randint(int(KOF_START * SIZE_MAP[0]), int(SIZE_MAP[0] * (1 - KOF_START))), \
               random.randint(int(KOF_START * SIZE_MAP[1]), int(SIZE_MAP[1] * (1 - KOF_START)))
        while self.board[cord[0]][cord[1]] in wall_group or self.board[cord[0]][cord[1]] in rud_group:
            cord = random.randint(int(KOF_START * SIZE_MAP[0]), int(SIZE_MAP[0] * (1 - KOF_START))), \
                   random.randint(int(KOF_START * SIZE_MAP[1]), int(SIZE_MAP[1] * (1 - KOF_START)))
        return cord


class Camera:
    # зададим начальный сдвиг камеры и размер поля для возможности реализации циклического сдвига
    def __init__(self, x, y):
        self.dx = x
        self.dy = y

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class Game:
    def __init__(self, flag, name):
        self.name = name
        self.controlDB = ControlDataBase()
        if flag:
            self.key = random.randint(0, 10000000)
            self.board = GeneratePlay(SIZE_MAP[0], SIZE_MAP[1], self.key)
            self.player = Player(*self.board.start_cord())
            self.board_pole = self.board.board
            self.x, self.y = self.player.x, self.player.y
        else:
            self.id, self.key, self.x, self.y = self.controlDB.get_info_of_name_world(name)
            self.board = load_level(str(self.id))
            self.player = Player(self.x, self.y)
            self.board_pole = self.board
        self.camera = Camera(self.player.x, self.player.y)
        self.play()

    def play(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            v = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    running = False
                elif event.type == pygame.KEYDOWN and v:
                    if event.key == pygame.K_LEFT:
                        v = False
                        self.player.remove_cord(-STEP, 'ox')
                    if event.key == pygame.K_RIGHT:
                        v = False
                        self.player.remove_cord(STEP, 'ox')
                    if event.key == pygame.K_UP:
                        v = False
                        self.player.remove_cord(-STEP, 'oy')
                    if event.key == pygame.K_DOWN:
                        v = False
                        self.player.remove_cord(STEP, 'oy')

            self.camera.update(self.player)
            for sprite in all_sprites:
                self.camera.apply(sprite)
            screen.fill(pygame.Color(0, 0, 0))
            all_sprites.draw(screen)
            player_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

    def close(self):
        ID = self.controlDB.add_world(self.name, '100', self.key, self.x, self.y)
        f = open(f"map/{ID}.txt", 'w')
        for i in range(len(self.board_pole)):
            for j in range(len(self.board_pole[i])):
                print(self.board_pole[i][j], file=f, end='\t')
            print(file=f)
        f.close()
