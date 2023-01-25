import pygame
import os
from PerlinNoise import *
from ContolBD import ControlDataBase
import sys
import time
from pygame.math import Vector2
import cProfile
from pympler import summary

# Константы
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

tile_images = None
screen_info = None
screen_map = None
screen = None


def restarted():
    global all_sprites, block_group, bots_group, player_group, wall_group, rud_group, mine_group, turel_group
    global wall_ust_group, ust_block, v_group, tile_images, screen, screen_map, screen_info

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

    tile_images = None
    screen_info = None
    screen_map = None
    screen = None


# fwefwfwfwfwfwfwfwf
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


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # Получение координат блока
    def get_cords(self):
        return self.x, self.y


# Стена, которая спавнится игрой
class Wall(Block):
    def __init__(self, var, pos_x, pos_y, x, y, xp):
        super().__init__(var + 'sten', pos_x, pos_y, x, y, 's', var, wall_group)
        self.xp = xp


# Ядро - главный центр
class Core(AnimatedBlock):
    def __init__(self, pos_x, pos_y, x, y, xp, biom):
        super().__init__('yad', pos_x, pos_y, x, y, 'y', biom, ust_block)
        self.xp = xp


# Турель

class Turel(Block):
    def __init__(self, pos_x, pos_y, x, y, xp, biom):
        super().__init__('tur', pos_x, pos_y, x, y, 't', biom, turel_group, ust_block)
        self.xp = xp
        self.radius = 10 * TILE_WIDTH
        self.damage = 10


# Бур

class Mine(AnimatedBlock):
    def __init__(self, pos_x, pos_y, x, y, xp, biom):
        super().__init__('mine', pos_x, pos_y, x, y, 'm', biom, mine_group, ust_block)
        self.xp = xp


# Стены, которые устанавливает персонаж
class Wall_Ust(Block):
    def __init__(self, pos_x, pos_y, x, y, xp, biom):
        super().__init__('wal2', pos_x, pos_y, x, y, 'w', biom, wall_ust_group, ust_block)
        self.xp = xp


# Объекты, которые могут двигаться самостоятельно
class MoveableEntity(Entity):
    def __init__(self, moveable_entity_group, pos_x, pos_y):
        super(MoveableEntity, self).__init__(moveable_entity_group, v_group)
        self.cords = [pos_x, pos_y]
        self.mask = None
        self.rect = None

    # Изменение координаты по x проверка, что не влетели в стену
    def remove_cord_ox(self, step):
        self.rect.x += step
        for i in wall_group:
            if pygame.sprite.collide_mask(self, i):
                self.rect.x -= step
                return False
        self.rect.x -= step
        return True

    # Изменение координаты по y проверка, что не влетели в стену
    def remove_cord_oy(self, step):
        self.rect.y += step
        for i in wall_group:
            if pygame.sprite.collide_mask(self, i):
                self.rect.y -= step
                return False
        self.rect.y -= step
        return True


# Объект Бота
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
        self.radius = 7 * TILE_WIDTH
        self.damage = 60

    # Расчёт стартового положения
    def z_rect(self, x, y):
        self.rect = self.image.get_rect(). \
            move(TILE_WIDTH * (self.x_p - x + KRAY),
                 TILE_WIDTH * (self.y_p - y + KRAY))

    # Движение ботов
    def movement(self):
        if self.flag:
            self.x_p, self.y_p = [self.x_p + self.step_x, self.y_p + self.step_y]
            self.delta_x = - self.x_p + self.yadrox
            self.delta_y = - self.y_p + self.yadroy
            self.step_x = min(0.5, self.delta_x / 30)
            self.step_y = min(0.5, self.delta_y / 30)
        self.flag = True

    # Загрука информации для файлов
    def __str__(self):
        return str(self.xp) + '#' + str(float(self.x_p)) + ':' + str(float(self.y_p))


# Отключение игры
def terminate():
    pygame.quit()
    # sys.exit()


# Игрок
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

    # Изменение координат
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

    # Возвращение на спавн
    def remove_cord_for_m(self, step_x, step_y):
        self.cords = [self.x, self.y]
        self.x_p = self.x
        self.y_p = self.y
        self.rect.x += step_x
        self.rect.y += step_y


# Генерация мира
class GeneratePlay:
    # создание поля
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
        board_new = []
        for y in range(height):
            a = []
            for x in range(width):
                a.append(self.enterprited((int((self.get_color(self.board[y][x][0], 0) + 1) / 2 * 255 + 0.5) +
                                           int((self.get_color(self.board[y][x][0], 0) + 1) / 2 * 255 + 0.5) +
                                           int((self.get_color(self.board[y][x][1], 1) + 1) / 2 * 255 + 0.5)) // 3, x,
                                          y, int(self.get_color(self.board[y][x][2], 2)))
                         )
            board_new.append(a)
        self.board = board_new

    # 170 руда
    # 212 стены
    # 255 белый
    # 128 серый
    # Сглаживание и настройка относительно руд и стен
    def get_color(self, color, ind):
        if ind == 0:
            return 1 if color > 0.25 else 0
        elif ind == 1:
            return 1 if color > 0.6 else 0
        else:
            return 1 if color > 0.2 else 2 if color > -0.2 else 0

    # Настройка и создание относительно биомов

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

    # Получение координат спавна

    def start_cord(self):
        cord = random.randint(int(KOF_START * SIZE_MAP[0]), int(SIZE_MAP[0] * (1 - KOF_START))), \
               random.randint(int(KOF_START * SIZE_MAP[1]), int(SIZE_MAP[1] * (1 - KOF_START)))
        while self.board[cord[1]][cord[0]] in wall_group or self.board[cord[1]][cord[0]] in rud_group:
            cord = random.randint(int(KOF_START * SIZE_MAP[0]), int(SIZE_MAP[0] * (1 - KOF_START))), \
                   random.randint(int(KOF_START * SIZE_MAP[1]), int(SIZE_MAP[1] * (1 - KOF_START)))
        return cord

    # Изменение клетки в поле
    def remove(self, tile, x, y):
        self.board[y][x].kill()
        self.board[y][x] = tile


# Камера просмотра игрока
class Camera:
    # зададим начальный сдвиг камеры и размер поля для возможности реализации циклического сдвига
    def __init__(self, x, y):
        self.dx = x
        self.dy = y

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # сдвиг объектов для ботов
    def apply_bots(self, obj, x, y):
        obj.rect.x = TILE_WIDTH * (obj.x_p - x + KRAY)
        obj.rect.y = TILE_WIDTH * (obj.y_p - y + KRAY)

    # позиционировать камеру на объекте target

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH_MAP // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


# Проверка на соприкосновение и возможность атаки
def circle_collision(left, right):
    distance = Vector2(left.rect.center).distance_to(right.rect.center)
    return distance < left.radius

def profile(func):
    """Decorator for run function profile"""
    def wrapper(*args, **kwargs):
        profile_filename = func.__name__ + '.prof'
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)
        profiler.dump_stats(profile_filename)
        return result
    return wrapper

class Game:
    """Игра"""
    @profile
    def __init__(self, flag, name, key=-1, size=-1):
        global screen_info, screen_map, screen
        restarted()
        screen_info = pygame.Surface((WIDTH - WIDTH_MAP, HEIGHT))
        screen_map = pygame.Surface((WIDTH_MAP, HEIGHT))
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.init()
        pygame.key.set_repeat(200, 70)
        global SIZE_MAP
        self.name = name

        self.controlDB = ControlDataBase()
        self.col_bur = 0
        global tile_images
        # Загрузка всех изображений
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
                       'yad': [
                           pygame.transform.scale(load_image(f'yadro/sprite_{str(i) if i >= 10 else "0" + str(i)}.png'),
                                                  (TILE_WIDTH, TILE_WIDTH)) for i in range(18)],
                       'alm': load_image('almaz.png'),
                       'mine': [
                           pygame.transform.scale(load_image(f'bur/sprite_{str(i) if i >= 10 else "0" + str(i)}.png'),
                                                  (TILE_WIDTH, TILE_WIDTH)) for i in range(25)],
                       'bur_m': load_image('bur_magaz.jpg'),
                       'tur': pygame.transform.scale(load_image('turel.png'), (TILE_WIDTH, TILE_WIDTH)),
                       'turel_m': load_image('turel.png'),
                       'wal': pygame.transform.scale(load_image('wal.png'), (40, 40)),
                       'wal2': pygame.transform.scale(load_image('wal.png'), (TILE_WIDTH, TILE_WIDTH)),
                       'mar': pygame.transform.scale(load_image('player.png'), (TILE_WIDTH, TILE_WIDTH)),
                       'bur_for_magaz_no_ustan': pygame.transform.scale(load_image('bur_magaz_no_ustanovka.png'),
                                                                        (40, 40))}
        if flag:
            self.key = key
            random.seed(key)
            # Создание размеров относительно введённых запросов
            if size == 1:
                SIZE_MAP = random.randint(50, 100), random.randint(50, 100)
            elif size == 2:
                SIZE_MAP = random.randint(100, 200), random.randint(100, 200)
            elif size == 3:
                SIZE_MAP = random.randint(200, 300), random.randint(200, 300)
            # SIZE_MAP = (60, 60)
            self.board = GeneratePlay(SIZE_MAP[0], SIZE_MAP[1])
            self.player = Player(*self.board.start_cord())
            self.x, self.y = self.player.x, self.player.y
            self.board.remove(Core(self.x, self.y, self.x, self.y, 1000, self.board.board[self.y][self.x].biom), self.x,
                              self.y)
            self.board_pole = self.board.board
            # Изначально время равно 0, а количество алмазов 300
            self.rud = 300
            self.time = 0
        else:
            # Загрузка уже существующего мира
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
        self.string_text_res_comlex = self.font.render('Ресурсы Комплекса:', True, pygame.Color('black'))
        self.intro_rect_res_comlex = self.string_text_res_comlex.get_rect()
        self.intro_rect_res_comlex.x = 60
        self.intro_rect_res_comlex.y = 10
        self.string_text_cords = self.font.render('Координаты:', True, pygame.Color('black'))
        self.intro_rect_cords = self.string_text_cords.get_rect()
        self.intro_rect_cords.x = 10
        self.intro_rect_cords.y = 90
        self.string_text_time = self.font.render('Время:', True, pygame.Color('black'))
        self.intro_rect_time = self.string_text_time.get_rect()
        self.intro_rect_time.x = 10
        self.intro_rect_time.y = 120
        self.string_text_build_complex = self.font.render('Постройки Комплекса', True, pygame.Color('black'))
        self.intro_rect_build_complex = self.string_text_build_complex.get_rect()
        self.intro_rect_build_complex.x = 50
        self.intro_rect_build_complex.y = 290
        self.string_text_fps = self.font.render('FPS:', True, pygame.Color('black'))
        self.intro_rect_fps = self.string_text_fps.get_rect()
        self.intro_rect_fps.x = 10
        self.intro_rect_fps.y = 150
        self.string_text_exit = self.font.render('Выйти', True, pygame.Color('black'))
        self.intro_rect_exit = self.string_text_exit.get_rect()
        self.intro_rect_exit.x = 230
        self.intro_rect_exit.y = 670
        self.rud_image = tile_images['alm']
        self.bur_magaz_image = pygame.transform.scale(tile_images['bur_m'], (40, 40))
        self.turel_magaz_image = pygame.transform.scale(tile_images['turel_m'], (40, 40))
        self.bur_magaz_image_no_ust = tile_images['bur_for_magaz_no_ustan']
        self.wall_magaz_image = tile_images['wal']
        pygame.display.set_caption('Flight_Of_The_Clones')

    def play(self):
        """Процесс игры"""
        clock = pygame.time.Clock()
        running = True
        self.obn = 0
        self.sec = 0 + self.time % 60
        self.min = 0 + self.time // 60


        while running:
            attaks = []
            curl = []
            z_bots = None
            collided_sprites = None
            v = True
            collided_sprite_bot = None
            collided_sprite_ust = None
            collided_sprite_tur = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    return []
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Любое нажатие обрабатывается, если нажата кнопка выйти
                    # файл игры сохранится и будет доступен для доигрывания
                    if self.click(event.pos):
                        self.close()
                        return []
                elif event.type == pygame.KEYDOWN and v:
                    # Кнопка P автоматическое сохранение
                    # файл игры сохранится и будет доступен для доигрывания
                    if event.key == pygame.K_p:
                        self.close()
                        return []
                    # Движения
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
            # спавн ботов каждые полминуты
            if self.sec % 30 == 1 and self.obn == 1:
                for i in range(10):
                    self.add(self.min)
            self.camera.update(self.player)
            for sprite in all_sprites:
                self.camera.apply(sprite)
                if isinstance(sprite, AnimatedBlock) and self.obn % 10 == 0:
                    sprite.update()
            # проверка на столкновения
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
                                pygame.quit()
                                return self.time + int(time.time()) - int(self.timer), self.key
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
            # Движение ботов
            for sprite in v_group:
                if isinstance(sprite, Bot):
                    if self.obn == 50:
                        sprite.movement()
                    self.camera.apply_bots(sprite, self.player.cords[0],
                                           self.player.cords[1])
                else:
                    self.camera.apply(sprite)
            # атака турелей
            collided_sprites = pygame.sprite.groupcollide(turel_group, bots_group, False,
                                                          False, collided=circle_collision)
            for collided_sprite_tur, collided_sprite_bot in collided_sprites.items():
                if self.rud >= 1:
                    attaks.append([collided_sprite_tur.rect.center, collided_sprite_bot[0].rect.center])
            # обновления и перерисовки
            if self.obn == 50:
                # обновлять для экрана
                self.obn = 0
                self.rud += self.col_bur
                self.sec += 1
                sum1 = summary.summarize(v_group)
                summary.print_(sum1)
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
        """Спавн ботов"""
        x, y = self.spawn_cord()
        bot = Bot(x, y, self.x, self.y, (xp + 1) * 35)
        bot.z_rect(self.player.cords[0], self.player.cords[1])

    def restart(self):
        """Возвращение на точку спавна"""
        self.player.remove_cord_for_m(self.x - self.player.x_p, self.y - self.player.y_p)

    def click(self, pos):
        """Обработка кликов"""
        pos = pos[0] + 0.2 * TILE_WIDTH, pos[1] + 0.2 * TILE_WIDTH
        if pos[0] > WIDTH_MAP:
            # Магазин
            pos = pos[0] - WIDTH_MAP, pos[1]
            if 10 <= pos[0] <= 50 and 330 <= pos[1] <= 370:
                self.position = 'bur'
            elif 60 <= pos[0] <= 100 and 330 <= pos[1] <= 370:
                self.position = 'tur'
            elif 110 <= pos[0] <= 150 and 330 <= pos[1] <= 370:
                self.position = 'wal'
            elif 10 <= pos[0] <= 50 and 380 <= pos[1] <= 420:
                self.position = 'lom'
            elif 230 <= pos[0] <= 300 and 670 <= pos[1] <= 700:
                return True
        else:
            # поле и спавн построек
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
                if random.randint(0, 3) == 0:
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
        return False

    def update_screen_info(self, fps):
        """загрузка окна с информацией"""
        pygame.draw.rect(screen_info, (0, 0, 0), (0, 0, 5, HEIGHT), 5)
        pygame.draw.rect(screen_info, (0, 0, 0), (0, HEIGHT // 2.5, WIDTH - WIDTH_MAP, 5), 3)
        string_text_rud = self.font.render('-  ' + str(self.rud), True, pygame.Color('black'))
        intro_rect_rud = string_text_rud.get_rect()
        intro_rect_rud.x = 60
        intro_rect_rud.y = 50
        string_text_cord = self.font.render(f' {self.player.cords[0] - KRAY} {self.player.cords[1] - KRAY}', True,
                                            pygame.Color('black'))
        intro_rect_cord = string_text_cord.get_rect()
        intro_rect_cord.x = 150
        intro_rect_cord.y = 90
        string_text_time = self.font.render(f' {self.min} {self.sec}', True, pygame.Color('black'))
        intro_rect_time = string_text_time.get_rect()
        intro_rect_time.x = 150
        intro_rect_time.y = 120
        string_text_fps = self.font.render(f' {round(fps, 2)}', True, pygame.Color('black'))
        intro_rect_fps = string_text_fps.get_rect()
        intro_rect_fps.x = 150
        intro_rect_fps.y = 150
        screen_info.blit(self.string_text_res_comlex, self.intro_rect_res_comlex)
        screen_info.blit(self.string_text_build_complex, self.intro_rect_build_complex)
        screen_info.blit(self.string_text_cords, self.intro_rect_cords)
        screen_info.blit(string_text_rud, intro_rect_rud)
        screen_info.blit(string_text_cord, intro_rect_cord)
        screen_info.blit(string_text_time, intro_rect_time)
        screen_info.blit(string_text_fps, intro_rect_fps)
        screen_info.blit(self.string_text_exit, self.intro_rect_exit)
        screen_info.blit(self.string_text_time, self.intro_rect_time)
        screen_info.blit(self.string_text_fps, self.intro_rect_fps)
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
        """Получение координат спавна для ботов"""
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
        """Сохранение файлов"""
        id_zap = self.controlDB.add_world(self.name, self.time + self.obn, self.key, self.x, self.y, self.rud)
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
        pygame.quit()
