import random
import pygame
import os
from PerlinNoise import *
import PIL.Image
from ContolBD import ControlDataBase
import sys
import time
from pygame.math import Vector2

FPS = 50
WIDTH_MAP = HEIGHT = 700
WIDTH = WIDTH_MAP + 300
KOF_START = 0.45
KOF_ENEMY = 0.05
SIZE_WINDOW = WIDTH_MAP, HEIGHT
STEP = TILE_WIDTH = 34
RES_MAP = 5
RES_RUD = 2
RES_BIOM = 15
SIZE_MAP = -1, -1
KRAY = 10

all_sprites = pygame.sprite.Group()
block_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
rud_group = pygame.sprite.Group()
mine_group = pygame.sprite.Group()
turel_group = pygame.sprite.Group()
wall_ust_group = pygame.sprite.Group()
ust_block = pygame.sprite.Group()
v_group = pygame.sprite.Group()
bots_group = pygame.sprite.Group()

pygame.init()
pygame.key.set_repeat(200, 70)
screen_info = pygame.Surface((WIDTH - WIDTH_MAP, HEIGHT))
screen_map = pygame.Surface((WIDTH_MAP, HEIGHT))
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


def perep0(name, x, y):
    var = name[1:3]
    if name[0] == 'f':  # фон
        return Block(var + 'fon', x, y, x, y, 'f', var)
    elif name[0] == 'r':  # руда
        return Block(var + 'rud', x, y, x, y, 'r',  var, rud_group)
    elif name[0] == 's':  # стена
        return Wall(var, x, y, x, y, int(name[3:]))
    elif name[0] == 'y':  # ядро
        return Core(x, y, x, y, int(name[3:]), var)
    elif name[0] == 'm':  # бур
        return Mine(x, y, x, y, int(name[3:]), var)
    elif name[0] == 't':  # турель
        return Turel(x, y, x, y, int(name[3:]), var)
    elif name[0] == 'w':  # стена само построенная(персом)
        return Wall_Ust(x, y, x, y, int(name[3:]), var)


def perep1(name, x0, y0):
    bot = Bot(float(name[name.index('#') + 1:name.index(':')]), float(name[name.index(':') + 1:]),
               x0, y0, int(name[:name.index('#')]))
    bot.z_rect(x0, y0)


def load_level(filename, x, y):
    ControlDataBase().del_world(filename)
    filename0 = "map/" + filename + 'map.txt'
    with open(filename0, 'r') as mapFile:
        level_map = [line.split() for line in mapFile]

    board0 = [[perep0(level_map[i][j], j, i) for j in range(len(level_map[i]))] for i in range(len(level_map))]
    os.remove(filename0)
    filename1 = "map/" + filename + 'play.txt'
    with open(filename1, 'r') as mapFile:
        level_map = [line for line in mapFile]

    [perep1(level_map[i], x, y) for i in range(len(level_map))]
    os.remove(filename1)
    return board0


tile_images = {'v1rud': pygame.transform.scale(load_image('v1/rud.png'), (TILE_WIDTH, TILE_WIDTH)),
               'v1fon': pygame.transform.scale(load_image('v1/fon.png'), (TILE_WIDTH, TILE_WIDTH)),
               'v1sten': pygame.transform.scale(load_image('v1/sten.png'), (TILE_WIDTH, TILE_WIDTH)),
               'v2rud': pygame.transform.scale(load_image('v2/rud.png'), (TILE_WIDTH, TILE_WIDTH)),
               'v2fon': pygame.transform.scale(load_image('v2/fon.png'), (TILE_WIDTH, TILE_WIDTH)),
               'v2sten': pygame.transform.scale(load_image('v2/sten.png'), (TILE_WIDTH, TILE_WIDTH)),
               'v3rud': pygame.transform.scale(load_image('v3/rud.png'), (TILE_WIDTH, TILE_WIDTH)),
               'v3fon': pygame.transform.scale(load_image('v3/fon.png'), (TILE_WIDTH, TILE_WIDTH)),
               'v3sten': pygame.transform.scale(load_image('v3/sten.png'), (TILE_WIDTH, TILE_WIDTH)),
               'bot': pygame.transform.scale(load_image('bot.png'), (TILE_WIDTH, TILE_WIDTH)),
               'yad': [pygame.transform.scale(load_image(f'yadro/sprite_{str(i) if i >=10 else "0" + str(i)}.png'),
                                              (TILE_WIDTH, TILE_WIDTH)) for i in range(18)],
               'alm': load_image('almaz.png'),
               'mine': [pygame.transform.scale(load_image(f'bur/sprite_{str(i) if i >=10 else "0" + str(i)}.png'),
                                               (TILE_WIDTH, TILE_WIDTH)) for i in range(25)],
               'bur_m': load_image('bur_magaz.jpg'),
               'tur': pygame.transform.scale(load_image('turel.png'), (TILE_WIDTH, TILE_WIDTH)),
               'turel_m': load_image('turel.png'),
               'wal': load_image('wal.png'),
               'wal2': pygame.transform.scale(load_image('wal.png'), (TILE_WIDTH, TILE_WIDTH)),
               'mar': pygame.transform.scale(load_image('player.png'), (TILE_WIDTH, TILE_WIDTH)),
               'bur_for_magaz_no_ustan': pygame.transform.scale(load_image('bur_magaz_no_ustanovka.png'), (40, 40))}


class Entity(pygame.sprite.Sprite):
    def __init__(self, *alls):
        super().__init__(*alls)


class Block(Entity):
    def __init__(self, block_type, pos_x, pos_y, x, y, station, biom, *dop_group):
        super(Block, self).__init__(all_sprites, block_group, dop_group)
        self.image = tile_images[block_type]
        self.station = station
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_WIDTH * pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.xp = None
        self.x = x
        self.biom = biom
        self.y = y

    def __str__(self):
        if self.xp is None:
            return self.station + self.biom
        else:
            return self.station + self.biom + str(self.xp)

    def get_cords(self):
        return self.x, self.y


class AnimatedBlock(Entity):
    def __init__(self, block_type, pos_x, pos_y, x, y, station, biom, *dop_group):
        super(Entity, self).__init__(all_sprites, block_group, *dop_group)
        self.frame = tile_images[block_type]
        self.image = self.frame[0]
        self.station = station
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_WIDTH * pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.xp = None
        self.x = x
        self.biom = biom
        self.y = y
        self.cur_frame = 0

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frame)
        self.image = self.frame[self.cur_frame]

    def __str__(self):
        if self.xp is None:
            return self.station + self.biom
        else:
            return self.station + self.biom + str(self.xp)

    def get_cords(self):
        return self.x, self.y


class Wall(Block):
    def __init__(self, var, pos_x, pos_y, x, y, xp):
        super().__init__(var + 'sten', pos_x, pos_y, x, y, 's', var, wall_group)
        self.xp = xp


class Core(AnimatedBlock):
    def __init__(self, pos_x, pos_y, x, y, xp, biom):
        super().__init__('yad', pos_x, pos_y, x, y, 'y', biom, ust_block)
        self.xp = xp


class Turel(Block):
    def __init__(self, pos_x, pos_y, x, y, xp, biom):
        super().__init__('tur', pos_x, pos_y, x, y, 't', biom, turel_group, ust_block)
        self.xp = xp
        self.radius = 10 * TILE_WIDTH
        self.damage = 10


class Mine(AnimatedBlock):
    def __init__(self, pos_x, pos_y, x, y, xp, biom):
        super().__init__('mine', pos_x, pos_y, x, y, 'm', biom, mine_group, ust_block)
        self.xp = xp


class Wall_Ust(Block):
    def __init__(self, pos_x, pos_y, x, y, xp, biom):
        super().__init__('wal2', pos_x, pos_y, x, y, 'w', biom, wall_ust_group, ust_block)
        self.xp = xp


class MoveableEntity(Entity):
    def __init__(self, moveable_entity_group, pos_x, pos_y):
        super(MoveableEntity, self).__init__(moveable_entity_group, v_group)
        self.cords = [pos_x, pos_y]
        self.mask = None
        self.rect = None

    def remove_cord_ox(self, step):
        self.rect.x += step
        for i in wall_group:
            if pygame.sprite.collide_mask(self, i):
                self.rect.x -= step
                return False
        self.rect.x -= step
        return True

    def remove_cord_oy(self, step):
        self.rect.y += step
        for i in wall_group:
            if pygame.sprite.collide_mask(self, i):
                self.rect.y -= step
                return False
        self.rect.y -= step
        return True


class Bot(MoveableEntity):
    def __init__(self, *args):
        self.image = tile_images['bot']
        if len(args) == 7:
            pos_x, pos_y, x_p, y_p, yx, yy, xp = args
            super().__init__(bots_group, x_p, y_p)
            self.rect = self.image.get_rect().move(TILE_WIDTH * (pos_x + KRAY), TILE_WIDTH * (pos_y + KRAY))
        else:
            x_p, y_p, yx, yy, xp = args
            super().__init__(bots_group, x_p, y_p)
        self.mask = pygame.mask.from_surface(self.image)
        self.x_p = x_p
        self.y_p = y_p
        self.yadroy = yy
        self.yadrox = yx
        self.attak = 60
        self.delta_x = - self.x_p + self.yadrox
        self.delta_y = - self.y_p + self.yadroy
        self.xp = xp
        self.step_x = self.delta_x / 30
        self.step_y = self.delta_y / 30
        self.flag = True
        self.smes_x = 0
        self.smes_y = 0
        self.radius = 6 * TILE_WIDTH
        self.damage = 60

    def z_rect(self, x, y):
        self.rect = self.image.get_rect(). \
            move(TILE_WIDTH * (self.x_p - x + KRAY),
                 TILE_WIDTH * (self.y_p - y + KRAY))

    def movement(self):
        if self.flag:
            self.x_p, self.y_p = [self.x_p + self.step_x, self.y_p + self.step_y]
            self.delta_x = - self.x_p + self.yadrox
            self.delta_y = - self.y_p + self.yadroy
            self.step_x = min(0.5, self.delta_x / 30)
            self.step_y = min(0.5, self.delta_y / 30)
        self.flag = True

    def __str__(self):
        return str(self.xp) + '#' + str(float(self.x_p)) + ':' + str(float(self.y_p))


def terminate():
    pygame.quit()
    sys.exit()


class Player(MoveableEntity):
    def __init__(self, pos_x, pos_y):
        super(Player, self).__init__(player_group, pos_x, pos_y)
        self.image = tile_images['mar']
        self.mask = pygame.mask.from_surface(self.image)
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_WIDTH * pos_y)
        self.x_p = pos_x
        self.y_p = pos_y

    def remove_cord(self, step, paral):
        st = 1 if step > 0 else -1
        if paral == 'ox':
            if KRAY <= self.cords[0] + st <= SIZE_MAP[0] - KRAY - 1 and self.remove_cord_ox(step):
                self.cords[0] += st
                self.rect.x += step
                self.x_p += step
        else:
            if KRAY <= self.cords[1] + st <= SIZE_MAP[1] - KRAY - 1 and self.remove_cord_oy(step):
                self.cords[1] += st
                self.rect.y += step
                self.y_p += step

    def remove_cord_for_m(self, step_x, step_y):
        self.cords = [self.x, self.y]
        self.x_p = self.x
        self.y_p = self.y
        self.rect.x += step_x
        self.rect.y += step_y


class GeneratePlay:
    # создание поля
    def __init__(self, width, height, seed):
        self.width = width
        self.height = height
        random.seed(seed)
        self.noise_map = PerlinNoiseFactory(2, octaves=1, tile=(width // RES_MAP + 1, height // RES_MAP + 1))
        self.noise_rud = PerlinNoiseFactory(2, octaves=1, tile=(width // RES_RUD + 1, height // RES_RUD + 1))
        self.noise_biom = PerlinNoiseFactory(2, octaves=1, tile=(width // RES_BIOM + 1, height // RES_BIOM + 1))
        self.board = [[[self.noise_map(i / RES_MAP, j / RES_MAP),
                        self.noise_rud(i / RES_RUD, j / RES_RUD),
                        self.noise_biom(i / RES_BIOM, j / RES_BIOM)]
                       for i in range(width)] for j in range(height)]
        board_new = []
        # значения по умолчанию
        img = PIL.Image.new('RGB', (width, height))
        pix = img.load()
        for y in range(height):
            a = []
            for x in range(width):
                pix[x, y] = int((self.get_color(self.board[y][x][0], 0) + 1) / 2 * 255 + 0.5), \
                            int((self.get_color(self.board[y][x][0], 0) + 1) / 2 * 255 + 0.5), \
                            int((self.get_color(self.board[y][x][1], 1) + 1) / 2 * 255 + 0.5)
                a.append(self.enterprited((int((self.get_color(self.board[y][x][0], 0) + 1) / 2 * 255 + 0.5) +
                                           int((self.get_color(self.board[y][x][0], 0) + 1) / 2 * 255 + 0.5) +
                                           int((self.get_color(self.board[y][x][1], 1) + 1) / 2 * 255 + 0.5)) // 3, x,
                                          y, int(self.get_color(self.board[y][x][2], 2)))
                         )
            board_new.append(a)
        img.save("pr3.png")
        self.board = board_new

    # 170 руда
    # 212 стены
    # 255 белый
    # 128 серый
    def get_color(self, color, ind):
        if ind == 0:
            return 1 if color > 0.25 else 0
        elif ind == 1:
            return 1 if color > 0.6 else 0
        else:
            return 1 if color > 0.2 else 2 if color > -0.2 else 0

    def enterprited(self, n, x, y, var):
        if var == 0:
            var = 'v1'
        elif var == 1:
            var = 'v2'
        if var == 2:
            var = 'v3'
        if n == 128:
            return Block(var + 'fon', x, y, x, y, 'f', var)
        elif n == 170:
            return Block(var + 'rud', x, y, x, y, 'r', var, rud_group)
        else:
            return Wall(var, x, y, x, y, 200)

    def start_cord(self):
        cord = random.randint(int(KOF_START * SIZE_MAP[0]), int(SIZE_MAP[0] * (1 - KOF_START))), \
               random.randint(int(KOF_START * SIZE_MAP[1]), int(SIZE_MAP[1] * (1 - KOF_START)))
        while self.board[cord[1]][cord[0]] in wall_group or self.board[cord[1]][cord[0]] in rud_group:
            cord = random.randint(int(KOF_START * SIZE_MAP[0]), int(SIZE_MAP[0] * (1 - KOF_START))), \
                   random.randint(int(KOF_START * SIZE_MAP[1]), int(SIZE_MAP[1] * (1 - KOF_START)))
        return cord

    def remove(self, tile, x, y):
        self.board[y][x] = tile


class Camera:
    # зададим начальный сдвиг камеры и размер поля для возможности реализации циклического сдвига
    def __init__(self, x, y):
        self.dx = x
        self.dy = y

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def apply_bots(self, obj, x, y):
        obj.rect.x = TILE_WIDTH * (obj.x_p - x + KRAY)
        obj.rect.y = TILE_WIDTH * (obj.y_p - y + KRAY)

    # позиционировать камеру на объекте target

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH_MAP // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


def circle_collision(left, right):
    distance = Vector2(left.rect.center).distance_to(right.rect.center)
    return distance < left.radius


class Game:
    def __init__(self, flag, name):
        global SIZE_MAP
        self.name = name
        self.controlDB = ControlDataBase()
        self.col_bur = 0
        if flag:
            self.key = random.randint(0, 100000000)
            SIZE_MAP = random.randint(50, 300), random.randint(50, 300)
            # SIZE_MAP = (60, 60)
            self.board = GeneratePlay(SIZE_MAP[0], SIZE_MAP[1], self.key)
            self.player = Player(*self.board.start_cord())
            self.x, self.y = self.player.x, self.player.y
            self.board.remove(Core(self.x, self.y, self.x, self.y, 1000, self.board.board[self.y][self.x].biom), self.x,
                              self.y)
            self.board_pole = self.board.board
            self.rud = 300
            self.time = 0
        else:
            self.id, self.key, self.x, self.y, self.time, self.rud = self.controlDB.get_info_of_name_world(name)
            self.board = load_level(str(self.id), self.x, self.y)
            self.player = Player(self.x, self.y)
            self.board_pole = self.board
            SIZE_MAP = len(self.board_pole[0]), len(self.board_pole)
            for i in self.board_pole:
                for j in i:
                    if j.station == 'm':
                        self.col_bur += 1
        self.camera = Camera(self.player.x, self.player.y)
        self.timer = time.time()
        self.position = ''
        print(SIZE_MAP)
        self.font = pygame.font.Font(None, 30)
        self.string_text1 = self.font.render('Ресурсы Комплекса:', True, pygame.Color('black'))
        self.intro_rect1 = self.string_text1.get_rect()
        self.intro_rect1.x = 60
        self.intro_rect1.y = 10
        self.string_text4 = self.font.render('Координаты:', True, pygame.Color('black'))
        self.intro_rect4 = self.string_text1.get_rect()
        self.intro_rect4.x = 10
        self.intro_rect4.y = 90
        self.string_text7 = self.font.render('Время:', True, pygame.Color('black'))
        self.intro_rect7 = self.string_text1.get_rect()
        self.intro_rect7.x = 10
        self.intro_rect7.y = 120
        self.string_text2 = self.font.render('Постройки Комплекса', True, pygame.Color('black'))
        self.intro_rect2 = self.string_text2.get_rect()
        self.intro_rect2.x = 50
        self.intro_rect2.y = 290
        self.string_text8 = self.font.render('FPS:', True, pygame.Color('black'))
        self.intro_rect8 = self.string_text1.get_rect()
        self.intro_rect8.x = 10
        self.intro_rect8.y = 150
        self.rud_image = tile_images['alm']
        self.bur_magaz_image = pygame.transform.scale(tile_images['bur_m'], (40, 40))
        self.turel_magaz_image = pygame.transform.scale(tile_images['turel_m'], (40, 40))
        self.bur_magaz_image_no_ust = tile_images['bur_for_magaz_no_ustan']
        self.wall_magaz_image = tile_images['wal']
        self.play()

    def play(self):
        clock = pygame.time.Clock()
        running = True
        self.obn = 0
        self.sec = 0 + self.time % 60
        self.min = 0 + self.time // 60
        attaks = []
        curl = []
        collided_sprites = None
        while running:
            v = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.click(event.pos)
                elif event.type == pygame.KEYDOWN and v:
                    if event.key == pygame.K_p:
                        self.close()
                        running = False
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        v = False
                        self.player.remove_cord(-STEP, 'ox')
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        v = False
                        self.player.remove_cord(STEP, 'ox')
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        v = False
                        self.player.remove_cord(-STEP, 'oy')
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        v = False
                        self.player.remove_cord(STEP, 'oy')
                    elif event.key == pygame.K_m:
                        self.restart()
            if self.sec % 30 == 1 and self.obn == 1:
                for i in range(10):
                    self.add(self.min)
            self.camera.update(self.player)
            for sprite in all_sprites:
                self.camera.apply(sprite)
                if isinstance(sprite, AnimatedBlock) and self.obn % 10 == 0:
                    sprite.update()
            collided_sprites = pygame.sprite.groupcollide(bots_group, wall_group, False,
                                                          False)
            z_bots = collided_sprites.keys()
            for collided_sprite_bot, collided_sprite_ust in collided_sprites.items():
                collided_sprite_bot.flag = False
                curl.append([collided_sprite_bot.rect.center, collided_sprite_ust[0].rect.center])
                if self.obn == 50:
                    collided_sprite_ust[0].xp -= collided_sprite_bot.damage
                    if collided_sprite_ust[0].xp <= 0:
                        x, y = collided_sprite_ust[0].x, collided_sprite_ust[0].y
                        collided_sprite_ust[0].kill()
                        collided_sprite_bot.flag = True
                        if random.randint(0, 10) == 0:
                            self.board_pole[y][x] = Block(self.board_pole[y][x].biom + 'rud',
                                                          x + KRAY - self.player.cords[0] - 0.2,
                                                          y + KRAY - self.player.cords[1] - 0.2, x,
                                                          y, 'r', self.board_pole[y][x].biom,
                                                          rud_group)
                        else:
                            self.board_pole[y][x] = Block(self.board_pole[y][x].biom + 'fon',
                                                          x + KRAY - self.player.cords[0] - 0.2,
                                                          y + KRAY - self.player.cords[1] - 0.2, x,
                                                          y, 'f', self.board_pole[y][x].biom)
                        if self.board_pole[y][x].rect.x < 0:
                            self.board_pole[y][x].rect.x -= 1
                        if self.board_pole[y][x].rect.y < 0:
                            self.board_pole[y][x].rect.y -= 1
            collided_sprites = pygame.sprite.groupcollide(bots_group, ust_block, False,
                                                          False, collided=circle_collision)
            for collided_sprite_bot, collided_sprite_ust in collided_sprites.items():
                if collided_sprite_bot not in z_bots:
                    curl.append([collided_sprite_bot.rect.center, collided_sprite_ust[0].rect.center])
                    collided_sprite_bot.flag = False
                    if self.obn == 50:
                        collided_sprite_ust[0].xp -= collided_sprite_bot.damage
                        if collided_sprite_ust[0].xp <= 0:
                            x, y = collided_sprite_ust[0].x, collided_sprite_ust[0].y
                            rect = collided_sprite_ust[0].rect
                            collided_sprite_ust[0].kill()
                            collided_sprite_bot.flag = True
                            if self.y == y and self.x == x:
                                self.end()
                                running = False
                            if isinstance(self.board_pole[y][x], Mine):
                                self.col_bur -= 1
                            if random.randint(0, 10) == 0:
                                self.board_pole[y][x] = Block(self.board_pole[y][x].biom + 'rud',
                                                              x + KRAY - self.player.cords[0] - 0.2,
                                                              y + KRAY - self.player.cords[1] - 0.2, x,
                                                              y, 'r', self.board_pole[y][x].biom,
                                                              rud_group)
                            else:
                                self.board_pole[y][x] = Block(self.board_pole[y][x].biom + 'fon',
                                                              x + KRAY - self.player.cords[0] - 0.2,
                                                              y + KRAY - self.player.cords[1] - 0.2, x,
                                                              y, 'f', self.board_pole[y][x].biom)
                            self.board_pole[y][x].rect = rect
            for sprite in v_group:
                if isinstance(sprite, Bot):
                    if self.obn == 50:
                        sprite.movement()
                    self.camera.apply_bots(sprite, self.player.cords[0],
                                           self.player.cords[1])
                else:
                    self.camera.apply(sprite)

            collided_sprites = pygame.sprite.groupcollide(turel_group, bots_group, False,
                                                          False, collided=circle_collision)
            for collided_sprite_tur, collided_sprite_bot in collided_sprites.items():
                if self.rud >= 1:
                    attaks.append([collided_sprite_tur.rect.center, collided_sprite_bot[0].rect.center])
            if self.obn == 50:
                # обновлять для экрана
                self.obn = 0
                self.rud += self.col_bur
                self.sec += 1
                for collided_sprite_tur, collided_sprite_bot in collided_sprites.items():
                    collided_sprite_bot = collided_sprite_bot[0]
                    if self.rud >= 1:
                        collided_sprite_bot.xp -= collided_sprite_tur.damage
                        self.rud -= 1
                        if collided_sprite_bot.xp <= 0:
                            collided_sprite_bot.kill()
                if self.sec == 60:
                    self.sec = 0
                    self.min += 1
                    self.rud += 1
            screen_map.fill(pygame.Color('black'))
            screen_info.fill(pygame.Color('white'))
            all_sprites.draw(screen_map)
            v_group.draw(screen_map)
            player_group.draw(screen_map)
            for i in curl:
                pygame.draw.aaline(screen_map, 'red', i[0], i[1], 4)
            for i in attaks:
                pygame.draw.aaline(screen_map, 'green', i[0], i[1], 2)
            attaks.clear()
            curl.clear()
            self.update_screen_info(clock.get_fps())
            screen.blit(screen_map, (0, 0))
            screen.blit(screen_info, (WIDTH_MAP, 0))
            pygame.display.flip()
            self.obn += 1
            clock.tick(FPS)

    def add(self, xp):
        x, y = self.spawn_cord()
        bot = Bot(x, y, self.x, self.y, (xp + 1) * 35)
        bot.z_rect(self.player.cords[0], self.player.cords[1])

    def restart(self):
        self.player.remove_cord_for_m(self.x - self.player.x_p, self.y - self.player.y_p)

    def click(self, pos):
        pos = pos[0] + 0.2 * TILE_WIDTH, pos[1] + 0.2 * TILE_WIDTH
        if pos[0] > WIDTH_MAP:
            pos = pos[0] - WIDTH_MAP, pos[1]
            if 10 <= pos[0] <= 50 and 330 <= pos[1] <= 370:
                self.position = 'bur'
            elif 60 <= pos[0] <= 100 and 330 <= pos[1] <= 370:
                self.position = 'tur'
            elif 110 <= pos[0] <= 150 and 330 <= pos[1] <= 370:
                self.position = 'wal'
            elif 10 <= pos[0] <= 50 and 380 <= pos[1] <= 420:
                self.position = 'lom'
        else:
            pos = int(pos[0] // TILE_WIDTH + self.player.cords[0] - KRAY), \
                  int(pos[1] // TILE_WIDTH + self.player.cords[1] - KRAY)
            print(pos)
            if self.rud >= 50 and self.position == 'bur' and \
                    (self.board_pole[pos[1]][pos[0]].station == 'm' or self.board_pole[pos[1]][pos[0]].station == 'r'):
                self.rud -= 50
                if self.board_pole[pos[1]][pos[0]].station != 'm':
                    self.col_bur += 1
                self.board_pole[pos[1]][pos[0]] = Mine(pos[0] + KRAY - self.player.cords[0] - 0.2,
                                                       pos[1] + KRAY - self.player.cords[1] - 0.2, pos[0], pos[1],
                                                       100, self.board_pole[pos[1]][pos[0]].biom)
            elif self.rud >= 70 and self.position == 'tur' and self.board_pole[pos[1]][pos[0]].station != 's' and \
                    self.board_pole[pos[1]][pos[0]].station != 'y':
                self.rud -= 70
                self.board_pole[pos[1]][pos[0]] = Turel(pos[0] + KRAY - self.player.cords[0] - 0.2,
                                                        pos[1] + KRAY - self.player.cords[1] - 0.2, pos[0], pos[1],
                                                        100, self.board_pole[pos[1]][pos[0]].biom)
            elif self.rud >= 50 and self.position == 'wal' and self.board_pole[pos[1]][pos[0]].station != 's' and \
                    self.board_pole[pos[1]][pos[0]].station != 'y':
                self.rud -= 50
                self.board_pole[pos[1]][pos[0]] = Wall_Ust(pos[0] + KRAY - self.player.cords[0] - 0.2,
                                                           pos[1] + KRAY - self.player.cords[1] - 0.2, pos[0], pos[1],
                                                           500, self.board_pole[pos[1]][pos[0]].biom)
            elif self.rud >= 30 and self.position == 'lom' and self.board_pole[pos[1]][pos[0]].station == 's':
                self.rud -= 30
                self.board_pole[pos[1]][pos[0]].kill()
                if random.randint(0, 10) == 0:
                    self.board_pole[pos[1]][pos[0]] = Block(self.board_pole[pos[1]][pos[0]].biom + 'rud',
                                                            pos[0] + KRAY - self.player.cords[0] - 0.2,
                                                            pos[1] + KRAY - self.player.cords[1] - 0.2, pos[0], pos[1],
                                                            'r', self.board_pole[pos[1]][pos[0]].biom,
                                                            rud_group)
                else:
                    self.board_pole[pos[1]][pos[0]] = Block(self.board_pole[pos[1]][pos[0]].biom + 'fon',
                                                            pos[0] + KRAY - self.player.cords[0] - 0.2,
                                                            pos[1] + KRAY - self.player.cords[1] - 0.2, pos[0], pos[1],
                                                            'f', self.board_pole[pos[1]][pos[0]].biom)

    def update_screen_info(self, fps):
        pygame.draw.rect(screen_info, (0, 0, 0), (0, 0, 5, HEIGHT), 5)
        pygame.draw.rect(screen_info, (0, 0, 0), (0, HEIGHT // 2.5, WIDTH - WIDTH_MAP, 5), 3)
        string_text3 = self.font.render('-  ' + str(self.rud), True, pygame.Color('black'))
        intro_rect3 = string_text3.get_rect()
        intro_rect3.x = 60
        intro_rect3.y = 50
        string_text5 = self.font.render(f' {self.player.cords[0] - KRAY} {self.player.cords[1] - KRAY}', True,
                                        pygame.Color('black'))
        intro_rect5 = string_text5.get_rect()
        intro_rect5.x = 150
        intro_rect5.y = 90
        string_text6 = self.font.render(f' {self.min} {self.sec}', True, pygame.Color('black'))
        intro_rect6 = string_text6.get_rect()
        intro_rect6.x = 150
        intro_rect6.y = 120
        string_text9 = self.font.render(f' {round(fps, 2)}', True, pygame.Color('black'))
        intro_rect9 = string_text6.get_rect()
        intro_rect9.x = 150
        intro_rect9.y = 150
        screen_info.blit(self.string_text1, self.intro_rect1)
        screen_info.blit(self.string_text2, self.intro_rect2)
        screen_info.blit(self.string_text4, self.intro_rect4)
        screen_info.blit(string_text3, intro_rect3)
        screen_info.blit(string_text5, intro_rect5)
        screen_info.blit(string_text6, intro_rect6)
        screen_info.blit(string_text9, intro_rect9)
        screen_info.blit(self.string_text7, self.intro_rect7)
        screen_info.blit(self.string_text8, self.intro_rect8)
        screen_info.blit(self.rud_image, (10, 40))
        screen_info.blit(self.bur_magaz_image, (10, 330))
        screen_info.blit(self.turel_magaz_image, (60, 330))
        screen_info.blit(self.wall_magaz_image, (110, 330))
        screen_info.blit(self.bur_magaz_image_no_ust, (10, 380))
        if self.position == 'bur':
            pygame.draw.rect(screen_info, (0, 0, 0), (8, 330, 42, 42), 2)
        elif self.position == 'tur':
            pygame.draw.rect(screen_info, (0, 0, 0), (58, 330, 42, 42), 2)
        elif self.position == 'wal':
            pygame.draw.rect(screen_info, (0, 0, 0), (108, 330, 42, 42), 2)
        elif self.position == 'lom':
            pygame.draw.rect(screen_info, (0, 0, 0), (8, 378, 42, 42), 2)

    def spawn_cord(self):
        z = random.randint(0, 3)
        if z == 0:
            x, y = random.randint(0, int(KOF_ENEMY * SIZE_MAP[0])) - 1, \
                   random.randint(0, SIZE_MAP[1]) - 1
        elif z == 1:
            x, y = random.randint(int((1 - KOF_ENEMY) * SIZE_MAP[0]), SIZE_MAP[0]) - 1, \
                   random.randint(0, SIZE_MAP[1]) - 1
        elif z == 2:
            x, y = random.randint(0, SIZE_MAP[0]) - 1, \
                   random.randint(0, int(KOF_ENEMY * SIZE_MAP[1])) - 1
        else:
            x, y = random.randint(0, SIZE_MAP[0]) - 1, \
                   random.randint(int((1 - KOF_ENEMY) * SIZE_MAP[1]), SIZE_MAP[1]) - 1

        if self.board_pole[y][x] in wall_group:
            return self.spawn_cord()
        return x, y

    def close(self):
        id_zap = self.controlDB.add_world(self.name, self.time + int(time.time()) - int(self.timer),
                                          self.key, self.x, self.y, self.rud)
        f = open(f"""map/{id_zap}map.txt""", 'w')
        for i in range(len(self.board_pole)):
            for j in range(len(self.board_pole[i])):
                print(self.board_pole[i][j], file=f, end='\t')
            print(file=f)
        f.close()
        f = open(f"""map/{id_zap}play.txt""", 'w')
        for i in bots_group:
            if i.xp > 0:
                print(i, file=f)
        f.close()

    def end(self):
        pass
