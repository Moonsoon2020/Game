import pygame
import os
from PerlinNoise import *
import PIL.Image
from ContolBD import ControlDataBase
import time
import sys

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
moveable_entity_group = pygame.sprite.Group()

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


def perep(name, x, y):
    if name[0] == 'f':
        return Block('fon', x, y, 'f')
    elif name[0] == 'r':
        return Block('rud', x, y, 'r', dop_group=rud_group)
    elif name[0] == 's':
        return Block('sten', x, y, 's', dop_group=wall_group)
    elif name[0] == 'y':
        return Core(x, y, int(name[1:]))
    elif name[0] == 'm':
        return Mine(x, y, int(name[1:]), dop_group=mine_group)
    elif name[0] == 't':
        return Turel(x, y, int(name[1:]), dop_group=turel_group)
    elif name[0] == 'w':
        return Wall(x, y, int(name[1:]))


def load_level(filename):
    ControlDataBase().del_world(filename)
    filename = "map/" + filename + '.txt'
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.split() for line in mapFile]

    board = [[perep(level_map[i][j], j, i) for j in range(len(level_map[i]))] for i in range(len(level_map))]
    os.remove(filename)
    return board


tile_images = {'rud': load_image('rud20.png'), 'fon': load_image('fon/fon20.png'), 'sten': load_image('sten.png'),
               'mar': load_image('mar.png'), 'yad': load_image('yadro.png'), 'ur': load_image('bur.jpg'),
               'alm': load_image('almaz.png'), 'mine': load_image('bur.jpg'), 'bur_m': load_image('bur_magaz.jpg'),
               'tur': load_image('turel.jpg'), 'turel_m': load_image('turel_m.jpg'), 'wal': load_image('wal.png'),
               'wal2': pygame.transform.scale(load_image('wal.png'), (20, 20))}


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

    def __str__(self):
        if self.xp is None:
            return self.station
        else:
            return self.station + str(self.xp)


class Core(Block):
    def __init__(self, pos_x, pos_y, xp, dop_group=block_group):
        super().__init__('yad', pos_x, pos_y, 'y', dop_group)
        self.xp = xp


class Turel(Block):
    def __init__(self, pos_x, pos_y, xp, dop_group=block_group):
        super().__init__('tur', pos_x, pos_y, 't', dop_group)
        self.xp = xp


class Mine(Block):
    def __init__(self, pos_x, pos_y, xp, dop_group=block_group):
        super().__init__('mine', pos_x, pos_y, 'm', dop_group)
        self.xp = xp


class Wall(Block):
    def __init__(self, pos_x, pos_y, xp, dop_group=block_group):
        super().__init__('wal2', pos_x, pos_y, 'w', dop_group)
        self.xp = xp


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
        self.rect_d = self.rect
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
        if flag:
            SIZE_MAP = random.randint(200, 400), random.randint(200, 400)
            self.key = random.randint(0, 10000000)
            self.board = GeneratePlay(SIZE_MAP[0], SIZE_MAP[1], self.key)
            self.player = Player(*self.board.start_cord())
            self.x, self.y = self.player.x, self.player.y
            self.board.remove(Core(self.x, self.y, 100), self.x, self.y)
            self.board_pole = self.board.board
            self.rud = 200
            self.time = 0

        else:
            self.id, self.key, self.x, self.y, self.time, self.rud = self.controlDB.get_info_of_name_world(name)
            self.board = load_level(str(self.id))
            self.player = Player(self.x, self.y)
            self.board_pole = self.board
            SIZE_MAP = len(self.board_pole), len(self.board_pole[0])
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
        self.wall_magaz_image = tile_images['wal']
        self.play()

    def play(self):
        clock = pygame.time.Clock()
        running = True
        obn = 0
        while running:
            v = True
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
            self.camera.update(self.player)
            for sprite in all_sprites:
                self.camera.apply(sprite)
            screen_map.fill(pygame.Color(0, 0, 0))
            screen_info.fill(pygame.Color('white'))
            obn += 1
            if obn == 20:
                obn = 0
                self.rud += self.col_bur
            all_sprites.draw(screen_map)
            player_group.draw(screen_map)
            self.update_screen_info()
            screen.blit(screen_map, (0, 0))
            screen.blit(screen_info, (WIDTH_MAP, 0))
            pygame.display.flip()
            clock.tick(FPS)

    def click(self, pos):
        if pos[0] > WIDTH_MAP:
            pos = pos[0] - WIDTH_MAP, pos[1]
            if 10 <= pos[0] <= 50 and 330 <= pos[1] <= 370:
                self.position = 'bur'
            elif 60 <= pos[0] <= 100 and 330 <= pos[1] <= 370:
                self.position = 'tur'
            elif 110 <= pos[0] <= 150 and 330 <= pos[1] <= 370:
                self.position = 'wal'
        else:
            pos = pos[0] // TILE_WIDTH + self.player.cords[0] - 17, pos[1] // TILE_WIDTH + self.player.cords[1] - 17
            print(pos, self.board_pole[pos[1]][pos[0]].station)
            if self.board_pole[pos[1]][pos[0]].station == 'r' and self.rud >= 50 and self.position == 'bur':
                self.rud -= 50
                self.board_pole[pos[1]][pos[0]] = Mine(pos[0] + 17 - self.player.cords[0],
                                                       pos[1] + 17 - self.player.cords[1], 100)
                self.col_bur += 1
            elif self.rud >= 50 and self.position == 'tur' and self.board_pole[pos[1]][pos[0]].station != 's':
                self.rud -= 50
                self.board_pole[pos[1]][pos[0]] = Turel(pos[0] + 17 - self.player.cords[0],
                                                        pos[1] + 17 - self.player.cords[1], 100)
            elif self.rud >= 50 and self.position == 'wal' and self.board_pole[pos[1]][pos[0]].station != 's':
                self.rud -= 50
                self.board_pole[pos[1]][pos[0]] = Wall(pos[0] + 17 - self.player.cords[0],
                                                       pos[1] + 17 - self.player.cords[1], 100)

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
        if self.position == 'bur':
            pygame.draw.rect(screen_info, (0, 0, 0), (8, 330, 42, 42), 2)
        elif self.position == 'tur':
            pygame.draw.rect(screen_info, (0, 0, 0), (58, 330, 42, 42), 2)
        elif self.position == 'wal':
            pygame.draw.rect(screen_info, (0, 0, 0), (108, 330, 42, 42), 2)

    def close(self):
        f = open(f"""map/{self.controlDB.add_world(self.name, self.time + int(time.time()) - int(self.timer),
                                                   self.key, self.x, self.y, self.rud)}.txt""", 'w')
        for i in range(len(self.board_pole)):
            for j in range(len(self.board_pole[i])):
                print(self.board_pole[i][j], file=f, end='\t')
            print(file=f)
        f.close()
