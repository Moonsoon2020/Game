import random

import pygame

from src.constans.gameconst import *
from src.game.functools import restarted, circle_collision
from src.game.opens import load_level
from src.game.bot import Bot
from src.game.player import Player
from src.game.camera import Camera
from src.game.generate import GeneratePlay
from src.game.entity import AnimatedBlock, Block, Mine, Wall_Ust, Core, Turel
from src.game.screen_info import ScreenInfo
from src.database.ContolBD import ControlDataBase



class Game:
    """Игра"""

    def __init__(self, flag, name, key=-1, size=-1):
        self.init_game(name)
        # Загрузка всех изображений
        if flag:
            self.create_map(key, size)
        else:
            self.dowland_map(name)
        self.camera = Camera(self.player.rect.x // TILE_WIDTH, self.player.rect.y // TILE_WIDTH)

    def init_game(self, name):
        self.timer = time.time()
        self.position = ''
        self.screen, self.sound_v, self.sound_g = restarted()
        self.screen_map = pygame.Surface((WIDTH_MAP, HEIGHT))
        self.name = name
        self.controlDB = ControlDataBase()
        self.col_bur = 0
        self.allowed_to_move = True
        self.screeninfo_obj = ScreenInfo()
        pygame.display.set_caption('Flight_Of_The_Clones')
        # self.sound_g.play()

    def create_map(self, key, size):
        global SIZE_MAP
        self.key = key
        random.seed(key)
        # Создание размеров относительно введённых запросов
        if size == 1:
            SIZE_MAP = random.randint(50, 100), random.randint(50, 100)
        elif size == 2:
            SIZE_MAP = random.randint(100, 200), random.randint(100, 200)
        elif size == 3:
            SIZE_MAP = random.randint(200, 300), random.randint(200, 300)
        else:
            SIZE_MAP = (60, 60)
        self.board = GeneratePlay(SIZE_MAP[0], SIZE_MAP[1])
        self.player = Player(*self.board.start_cord(), SIZE_MAP[0], SIZE_MAP[1])
        self.board.remove(Core(self.player.start_cords[0], self.player.start_cords[1], self.player.start_cords[0],
                               self.player.start_cords[1], 1000,
                               self.board.board[self.player.start_cords[1]][self.player.start_cords[0]].biom),
                          self.player.start_cords[0], self.player.start_cords[1])
        self.board_pole = self.board.board
        # Изначально время равно 0, а количество алмазов 300
        self.rud = 300
        self.time = 0

    def dowland_map(self, name):
        # Загрузка уже существующего мира
        self.id, self.key, x, y, self.time, self.rud = self.controlDB.get_info_of_name_world(name)
        self.board = load_level(str(self.id), self.player.start_cords[0], self.player.start_cords[1])
        self.board_pole = self.board
        SIZE_MAP = len(self.board_pole[0]), len(self.board_pole)
        self.player = Player(self.player.start_cords[0], self.player.start_cords[1], SIZE_MAP[0], SIZE_MAP[1])
        for i in self.board_pole:
            for j in i:
                if j.station == 'm':
                    self.col_bur += 1

    def play(self):
        """Процесс игры"""
        clock = pygame.time.Clock()
        running = True
        self.obn = 0
        self.sec = 0 + self.time % 60
        self.min = 0 + self.time // 60
        while running:
            self.handle_events()
            self.spawn_bots()
            self.update_entities()
            curl, attaks = self.check_collisions()
            self.update_screen(clock, attaks, curl)
            self.obn += 1
            clock.tick(FPS)
            self.allowed_to_move = True

    def handle_events(self):
        """Обработка событий игры"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
                return []
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.click(event.pos):
                    self.close()
                    return []
            elif event.type == pygame.KEYDOWN and self.allowed_to_move:
                if event.key == pygame.K_p:
                    self.close()
                    return []
                self.handle_movement(event)

    def spawn_bots(self):
        """Спавн ботов"""
        if self.sec % 30 == 1 and self.obn == 1:
            for _ in range(10):
                self.add(self.min)

    def update_entities(self):
        """Обновление всех сущностей"""
        self.camera.update(self.player)
        for sprite in all_sprites:
            self.camera.apply(sprite)
            if isinstance(sprite, AnimatedBlock) and self.obn % 10 == 0:
                sprite.update()

    def check_collisions(self):
        """Проверка на столкновения"""# проверка на столкновения
        curl, attaks = [], []
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
                    # self.sound_v.play()
                    collided_sprite_ust[0].xp -= collided_sprite_bot.damage
                    if collided_sprite_ust[0].xp <= 0:
                        x, y = collided_sprite_ust[0].x, collided_sprite_ust[0].y
                        rect = collided_sprite_ust[0].rect
                        collided_sprite_ust[0].kill()
                        collided_sprite_bot.flag = True
                        if self.player.start_cords[1] == y and self.player.start_cords[0] == x:
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
            for collided_sprite_tur, collided_sprite_bot in collided_sprites.items():
                # self.sound_v.play()
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
        return curl, attaks

    def update_screen(self, clock, attaks, curl):
        """Обновление экрана"""
        self.screen_map.fill(pygame.Color('black'))
        all_sprites.draw(self.screen_map)
        v_group.draw(self.screen_map)
        player_group.draw(self.screen_map)
        for i in curl:
            pygame.draw.aaline(self.screen_map, 'red', i[0], i[1], 4)
        for i in attaks:
            pygame.draw.aaline(self.screen_map, 'green', i[0], i[1], 2)
        attaks.clear()
        curl.clear()
        self.screeninfo_obj.update(clock.get_fps(), self)
        self.screen.blit(self.screen_map, (0, 0))
        self.screen.blit(self.screeninfo_obj.screen_info, (WIDTH_MAP, 0))
        pygame.display.flip()
    def add(self, xp):
        """Спавн ботов"""
        x, y = self.spawn_cord()
        bot = Bot(x, y, self.player.start_cords[0], self.player.start_cords[1], (xp + 1) * 35)
        bot.z_rect(self.player.cords[0], self.player.cords[1])

    def restart(self):
        """Возвращение на точку спавна"""
        self.player.remove_cord_for_m( (self.player.start_cords[0] - self.player.cords[0]) * TILE_WIDTH, (self.player.start_cords[1] - self.player.cords[1]) * TILE_WIDTH )

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
        id_zap = self.controlDB.add_world(self.name, self.time + self.obn, self.key, self.player.start_cords[0], self.player.start_cords[1], self.rud)
        f = open(f"""map/{id_zap}map.txt""", 'w')
        for i in range(len(self.board_pole)):
            for j in range(len(self.board_pole[i])):
                print(self.board_pole[i][j], file=f, end='\t')
                self.board_pole[i][j].kill()
            print(file=f)
        f.close()
        f = open(f"""map/{id_zap}play.txt""", 'w')
        for i in bots_group:
            if i.xp > 0:
                print(i, file=f)
            i.kill()
        f.close()
        pygame.quit()

    def handle_movement(self, event):
        """Обработка нажатий клавиш для перемещения игрока"""
        v = False
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            v = True
            self.player.remove_cord(-STEP, 'ox')
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            v = True
            self.player.remove_cord(STEP, 'ox')
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            v = True
            self.player.remove_cord(-STEP, 'oy')
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            v = True
            self.player.remove_cord(STEP, 'oy')
        elif event.key == pygame.K_m:
            v = True
            self.restart()
        if v:
            self.allowed_to_move = False


if __name__ == '__main__':
    Game = Game(True, "")
    Game.play()
