import pygame
import os
from PerlinNoise import *
import PIL.Image
from ContolBD import ControlDataBase
import sys
import time

FPS = 50
WIDTH_MAP = HEIGHT = 700
WIDTH = WIDTH_MAP + 300
STEP = 10
KOF_START = 0.45
KOF_ENEMY = 0.05
SIZE_WINDOW = WIDTH_MAP, HEIGHT
TILE_WIDTH = 20
RES_MAP = 5
RES_RUD = 2
SIZE_MAP = -1, -1

all_sprites = pygame.sprite.Group()
block_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
rud_group = pygame.sprite.Group()
mine_group = pygame.sprite.Group()
turel_group = pygame.sprite.Group()
v_group = pygame.sprite.Group()
y_grouop = pygame.sprite.Group()

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
    if name[0] == 'f':  # фон
        return Block('fon', x, y, 'f')
    elif name[0] == 'r':  # руда
        return Block('rud', x, y, 'r', dop_group=rud_group)
    elif name[0] == 's':  # стена
        return Block('sten', x, y, 's', dop_group=wall_group)
    elif name[0] == 'y':  # ядро
        return Core(x, y, int(name[1:]))
    elif name[0] == 'm':  # бур
        return Mine(x, y, int(name[2:]), name[1], dop_group=mine_group)
    elif name[0] == 't':  # турель
        return Turel(x, y, int(name[2:]), name[1], dop_group=turel_group)
    elif name[0] == 'w':  # стена само построенная
        return Wall(x, y, int(name[2:]), name[1])


def perep1(name, x0, y0):
    return Bot(float(name[name.index('#') + 1:name.index(':')]), float(name[name.index(':') + 1:]),
               x0, y0, int(name[:name.index('#')]))


def load_level(filename, x, y):
    ControlDataBase().del_world(filename)
    filename0 = "map/" + filename + 'map.txt'
    # читаем уровень, убирая символы перевода строки
    with open(filename0, 'r') as mapFile:
        level_map = [line.split() for line in mapFile]

    board0 = [[perep0(level_map[i][j], j, i) for j in range(len(level_map[i]))] for i in range(len(level_map))]
    os.remove(filename0)
    filename1 = "map/" + filename + 'play.txt'
    with open(filename1, 'r') as mapFile:
        level_map = [line for line in mapFile]

    board1 = [perep1(level_map[i], x, y) for i in range(len(level_map))]
    os.remove(filename1)
    return board0, board1


tile_images = {'rud': pygame.transform.scale(load_image('rud20.png'), (TILE_WIDTH, TILE_WIDTH)),
               'fon': pygame.transform.scale(load_image('fon/fon20.png'), (TILE_WIDTH, TILE_WIDTH)),
               'sten': pygame.transform.scale(load_image('sten.png'), (TILE_WIDTH, TILE_WIDTH)),
               'bot': pygame.transform.scale(load_image('player.png'), (TILE_WIDTH, TILE_WIDTH)),
               'yad': pygame.transform.scale(load_image('yadro.png'), (TILE_WIDTH, TILE_WIDTH)),
               'ur': pygame.transform.scale(load_image('bur.jpg'), (TILE_WIDTH, TILE_WIDTH)),
               'alm': load_image('almaz.png'),
               'mine': pygame.transform.scale(load_image('bur.jpg'), (TILE_WIDTH, TILE_WIDTH)),
               'bur_m': load_image('bur_magaz.jpg'),
               'tur': pygame.transform.scale(load_image('turel.jpg'), (TILE_WIDTH, TILE_WIDTH)),
               'turel_m': load_image('turel_m.jpg'),
               'wal': load_image('wal.png'),
               'wal2': pygame.transform.scale(load_image('wal.png'), (TILE_WIDTH, TILE_WIDTH)),
               'mar': pygame.transform.scale(load_image('bot.png'), (TILE_WIDTH, TILE_WIDTH)),
               'bur_for_magaz_no_ustan': pygame.transform.scale(load_image('bur_magaz_no_ustanovka.png'), (40, 40))}


class Entity(pygame.sprite.Sprite):
    def __init__(self, *alls):
        super().__init__(*alls)


class Block(Entity):
    def __init__(self, block_type, pos_x, pos_y, station, dop_group=block_group):
        super(Block, self).__init__(all_sprites, block_group, dop_group)
        self.image = tile_images[block_type]
        self.station = station
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_WIDTH * pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.xp = None
        self.past = ''

    def __str__(self):
        if self.xp is None:
            return self.station
        else:
            return self.station + self.past + str(self.xp)


class Core(Block):
    def __init__(self, pos_x, pos_y, xp, dop_group=block_group):
        super().__init__('yad', pos_x, pos_y, 'y', dop_group)
        self.xp = xp


class Turel(Block):
    def __init__(self, pos_x, pos_y, xp, past, dop_group=block_group):
        super().__init__('tur', pos_x, pos_y, 't', dop_group)
        self.xp = xp
        self.past = past


class Mine(Block):
    def __init__(self, pos_x, pos_y, xp, past, dop_group=block_group):
        super().__init__('mine', pos_x, pos_y, 'm', dop_group)
        self.xp = xp
        self.past = past


class Wall(Block):
    def __init__(self, pos_x, pos_y, xp, past, dop_group=block_group):
        super().__init__('wal2', pos_x, pos_y, 'w', dop_group)
        self.xp = xp
        self.past = past


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
        return True

    def remove_cord_oy(self, step):
        self.rect.y += step
        for i in wall_group:
            if pygame.sprite.collide_mask(self, i):
                self.rect.y -= step
                return False
        return True


class Bot(MoveableEntity):
    def __init__(self, *args):
        self.image = tile_images['bot']

        if len(args) == 7:
            pos_x, pos_y, x_p, y_p, yx, yy, xp = args
            super().__init__(v_group, x_p, y_p)
            self.rect = self.image.get_rect().move(TILE_WIDTH * (pos_x + 17), TILE_WIDTH * (pos_y + 17))
        else:
            x_p, y_p, yx, yy, xp = args
            super().__init__(v_group, x_p, y_p)
        self.mask = pygame.mask.from_surface(self.image)
        self.x_p = x_p
        self.y_p = y_p
        self.yadroy = yy
        self.yadrox = yx
        self.delta_x = - self.x_p + self.yadrox
        self.delta_y = - self.y_p + self.yadroy
        self.xp = xp
        self.step_x = self.delta_x / 100
        self.step_y = self.delta_y / 100
        self.flag = True
        self.smes_x = 0
        self.smes_y = 0

    def z_rect(self, x, y):
        if self.flag:
            self.flag = False
            self.rect = self.image.get_rect(). \
                move(TILE_WIDTH * (self.x_p - x + 17),
                     TILE_WIDTH * (self.y_p - y + 17))
        return self.flag

    def movement(self):
        if pygame.sprite.spritecollideany(self, player_group) or (
                abs(self.x_p - self.yadrox) <= 1 and abs(self.y_p - self.yadroy) <= 1):
            print(self.x_p, self.y_p, self.rect)
            return
        # self.rect.x += self.step_x
        # self.rect.y += self.step_y
        self.smes_y += self.step_y
        self.smes_x += self.step_x
        self.x_p, self.y_p = [self.x_p + self.step_x, self.y_p + self.step_y]
        self.delta_x = - self.x_p + self.yadrox
        self.delta_y = - self.y_p + self.yadroy
        self.step_x = min(0.5, self.delta_x / 100)
        self.step_y = min(0.5, self.delta_y / 100)

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
        if paral == 'ox':  # колво пикселей в человечке подредачь потом
            if 17 <= self.cords[0] + st <= SIZE_MAP[0] - 18 and self.remove_cord_ox(step):
                self.cords[0] += st
                self.rect.x += step
                self.x_p += step
        else:
            if 17 <= self.cords[1] + st <= SIZE_MAP[1] - 18 and self.remove_cord_oy(step):
                self.cords[1] += st
                self.rect.y += step
                self.y_p += step

    def remove_cord_for_m(self, step_x, step_y):
        self.cords = [self.x, self.y]
        self.x_p = self.x
        self.y_p = self.y
        self.rect.x += 2 * step_x
        self.rect.y += 2 * step_y


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
                                          y))
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
        else:
            return 1 if color > 0.6 else 0

    def enterprited(self, n, x, y):
        if n == 128:
            return Block('fon', x, y, 'f')
        elif n == 170:
            return Block('rud', x, y, 'r', dop_group=rud_group)
        else:
            return Block('sten', x, y, 's', dop_group=wall_group)

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

    def apply_bots(self, obj, x, y, flag):
        obj.rect.x = TILE_WIDTH * (obj.x_p - x + 17)
        obj.rect.y = TILE_WIDTH * (obj.y_p - y + 17)
        obj.rect.x += obj.smes_x
        obj.rect.y += obj.smes_y
        if flag:
            obj.movement()

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH_MAP // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class Game:
    def __init__(self, flag, name):
        global SIZE_MAP
        self.name = name
        self.controlDB = ControlDataBase()
        self.col_bur = 0
        self.bots = []
        if flag:
            self.key = random.randint(0, 100000000)
            SIZE_MAP = (60, 60) #random.randint(200, 400), random.randint(200, 400)
            self.board = GeneratePlay(SIZE_MAP[0], SIZE_MAP[1], self.key)
            self.player = Player(*self.board.start_cord())
            self.x, self.y = self.player.x, self.player.y
            self.board.remove(Core(self.x, self.y, 100), self.x, self.y)
            self.board_pole = self.board.board
            self.rud = 200
            self.time = 0
        else:
            self.id, self.key, self.x, self.y, self.time, self.rud = self.controlDB.get_info_of_name_world(name)
            self.board, self.bots = load_level(str(self.id), self.x, self.y)
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
        self.string_text1 = self.font.render('Ресурсы Комплекса', True, pygame.Color('black'))
        self.intro_rect1 = self.string_text1.get_rect()
        self.intro_rect1.x = 60
        self.intro_rect1.y = 10
        self.string_text2 = self.font.render('Постройки Комплекса', True, pygame.Color('black'))
        self.intro_rect2 = self.string_text2.get_rect()
        self.intro_rect2.x = 50
        self.intro_rect2.y = 290
        self.rud_image = tile_images['alm']
        self.bur_magaz_image = pygame.transform.scale(tile_images['bur_m'], (40, 40))
        self.turel_magaz_image = pygame.transform.scale(tile_images['turel_m'], (40, 40))
        self.bur_magaz_image_no_ust = tile_images['bur_for_magaz_no_ustan']
        self.wall_magaz_image = tile_images['wal']
        self.play()

    def play(self):
        clock = pygame.time.Clock()
        running = True
        obn = 0
        sec = 0
        while running:
            v = True
            if obn == 20:
                obn = 0
                self.rud += self.col_bur
                sec += 1
                if sec == 5:
                    self.add()
                    sec = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.click(event.pos)
                elif event.type == pygame.KEYDOWN and v:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        v = False
                        self.player.remove_cord(-STEP, 'ox')
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        v = False
                        self.player.remove_cord(STEP, 'ox')
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        v = False
                        self.player.remove_cord(-STEP, 'oy')
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        v = False
                        self.player.remove_cord(STEP, 'oy')
                    if event.key == pygame.K_m:
                        self.restart()

            self.camera.update(self.player)
            for sprite in all_sprites:
                self.camera.apply(sprite)
            for sprite in v_group:
                if isinstance(sprite, Bot):
                    if not sprite.z_rect(self.player.cords[0], self.player.cords[1]):
                        self.camera.apply_bots(sprite, self.player.cords[0], self.player.cords[1], obn == 0 or obn == 10)
                else:
                    self.camera.apply(sprite)

            screen_map.fill(pygame.Color(0, 0, 0))
            screen_info.fill(pygame.Color('white'))
            all_sprites.draw(screen_map)
            v_group.draw(screen_map)
            player_group.draw(screen_map)
            self.update_screen_info()
            screen.blit(screen_map, (0, 0))
            screen.blit(screen_info, (WIDTH_MAP, 0))
            pygame.display.flip()
            obn += 1
            # self.add()
            # for i in self.bots:
            #     i.movement()

            clock.tick(FPS)

    def add(self):
        x, y = self.spawn_cord()
        self.bots.append(Bot(x, y, self.x, self.y, 100))

    def restart(self):
        self.player.remove_cord_for_m(self.x - self.player.x_p, self.y - self.player.y_p)

    def click(self, pos):
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
            pos = pos[0] // TILE_WIDTH + self.player.cords[0] - 17, pos[1] // TILE_WIDTH + self.player.cords[1] - 17
            print(pos, self.board_pole[pos[1]][pos[0]].station)
            if self.board_pole[pos[1]][pos[0]].station == 'r' and self.rud >= 50 and self.position == 'bur':
                self.rud -= 50
                self.board_pole[pos[1]][pos[0]] = Mine(pos[0] + 17 - self.player.cords[0],
                                                       pos[1] + 17 - self.player.cords[1],
                                                       100, self.board_pole[pos[1]][pos[0]].station)
                self.col_bur += 1
            elif self.rud >= 50 and self.position == 'tur' and self.board_pole[pos[1]][pos[0]].station != 's' and \
                    self.board_pole[pos[1]][pos[0]].station != 'y':
                self.rud -= 50
                self.board_pole[pos[1]][pos[0]] = Turel(pos[0] + 17 - self.player.cords[0],
                                                        pos[1] + 17 - self.player.cords[1],
                                                        100, self.board_pole[pos[1]][pos[0]].station)
            elif self.rud >= 50 and self.position == 'wal' and self.board_pole[pos[1]][pos[0]].station != 's' and \
                    self.board_pole[pos[1]][pos[0]].station != 'y':
                self.rud -= 50
                self.board_pole[pos[1]][pos[0]] = Wall(pos[0] + 17 - self.player.cords[0],
                                                       pos[1] + 17 - self.player.cords[1],
                                                       100, self.board_pole[pos[1]][pos[0]].station)
            elif self.rud >= 50 and self.position == 'lom' and self.board_pole[pos[1]][pos[0]].station == 's':
                self.rud -= 50
                self.board_pole[pos[1]][pos[0]].kill()
                if random.randint(0, 10) == 0:
                    self.board_pole[pos[1]][pos[0]] = Block('rud', pos[0] + 17 - self.player.cords[0],
                                                            pos[1] + 17 - self.player.cords[1], 'r',
                                                            dop_group=rud_group)
                else:
                    self.board_pole[pos[1]][pos[0]] = Block('fon', pos[0] + 17 - self.player.cords[0],
                                                            pos[1] + 17 - self.player.cords[1], 'f')

    def update_screen_info(self):
        pygame.draw.rect(screen_info, (0, 0, 0), (0, 0, 5, HEIGHT), 5)
        pygame.draw.rect(screen_info, (0, 0, 0), (0, HEIGHT // 2.5, WIDTH - WIDTH_MAP, 5), 3)
        string_text3 = self.font.render('-  ' + str(self.rud) +
                                        f' {self.player.cords[0]}, {self.player.cords[1]}', True, pygame.Color('black'))
        intro_rect3 = self.string_text1.get_rect()
        intro_rect3.x = 60
        intro_rect3.y = 50
        screen_info.blit(self.string_text1, self.intro_rect1)
        screen_info.blit(self.string_text2, self.intro_rect2)
        screen_info.blit(string_text3, intro_rect3)
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
        for i in self.bots:
            print(i, file=f)
        f.close()
