from src.constans.gameconst import *
from src.game.functools import getimage

# Базовый класс для всех объектов на поле
class Entity(pygame.sprite.Sprite):
    def __init__(self, *alls):
        super().__init__(*alls)

# Класс для простых блоков на поле
class Block(Entity):
    def __init__(self, block_type, pos_x, pos_y, x, y, station, biom, *dop_group):
        super(Block, self).__init__(all_sprites, block_group, dop_group)
        self.image = getimage(block_type)  # Получаем изображение блока по его типу
        self.station = station  # Станция
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_WIDTH * pos_y)  # Позиция блока
        self.mask = pygame.mask.from_surface(self.image)  # Маска для коллизий
        self.xp = None  # Дополнительные параметры блока (например, уровень)
        self.x = x  # Координата x
        self.biom = biom  # Биом
        self.y = y  # Координата y

    # Получение данных о блоке для сохранения в файл
    def __str__(self):
        if self.xp is None:
            return self.station + self.biom
        else:
            return self.station + self.biom + str(self.xp)

    # Получение координат блока
    def get_cords(self):
        return self.x, self.y

# Класс для анимированных блоков на поле
class AnimatedBlock(Entity):
    def __init__(self, block_type, pos_x, pos_y, x, y, station, biom, *dop_group):
        super(Entity, self).__init__(all_sprites, block_group, *dop_group)
        self.frame = getimage(block_type)  # Получаем изображения кадров анимации
        self.image = self.frame[0]  # Текущее изображение блока
        self.station = station  # Станция
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_WIDTH * pos_y)  # Позиция блока
        self.mask = pygame.mask.from_surface(self.image)  # Маска для коллизий
        self.xp = None  # Дополнительные параметры блока (например, уровень)
        self.x = x  # Координата x
        self.biom = biom  # Биом
        self.y = y  # Координата y
        self.cur_frame = 0  # Текущий кадр анимации

    # Обновление изображения блока для анимации
    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frame)
        self.image = self.frame[self.cur_frame]

    # Получение данных о блоке для сохранения в файл
    def __str__(self):
        if self.xp is None:
            return self.station + self.biom
        else:
            return self.station + self.biom + str(self.xp)

    # Получение координат блока
    def get_cords(self):
        return self.x, self.y

# Класс для стены, которую спавнит игра
class Wall(Block):
    def __init__(self, var, pos_x, pos_y, x, y, xp):
        super().__init__(var + 'sten', pos_x, pos_y, x, y, 's', var, wall_group)
        self.xp = xp  # Уровень стены

# Класс для ядра - главного центра
class Core(AnimatedBlock):
    def __init__(self, pos_x, pos_y, x, y, xp, biom):
        super().__init__('yad', pos_x, pos_y, x, y, 'y', biom, ust_block)
        self.xp = xp  # Уровень ядра

# Класс для турели
class Turel(Block):
    def __init__(self, pos_x, pos_y, x, y, xp, biom):
        super().__init__('tur', pos_x, pos_y, x, y, 't', biom, turel_group, ust_block)
        self.xp = xp  # Уровень турели
        self.radius = 10 * TILE_WIDTH  # Радиус атаки турели
        self.damage = 10  # Урон турели

# Класс для бура
class Mine(AnimatedBlock):
    def __init__(self, pos_x, pos_y, x, y, xp, biom):
        super().__init__('mine', pos_x, pos_y, x, y, 'm', biom, mine_group, ust_block)
        self.xp = xp  # Уровень бура

# Класс для стен, которые устанавливает персонаж
class Wall_Ust(Block):
    def __init__(self, pos_x, pos_y, x, y, xp, biom):
        super().__init__('wal2', pos_x, pos_y, x, y, 'w', biom, wall_ust_group, ust_block)
        self.xp = xp  # Уровень стены

# Класс для объектов, которые могут двигаться самостоятельно
class MoveableEntity(Entity):
    def __init__(self, moveable_entity_group, pos_x, pos_y):
        super(MoveableEntity, self).__init__(moveable_entity_group, v_group)
        self.cords = [pos_x, pos_y]  # Координаты объекта
        self.mask = None
        self.rect = None

    # Изменение координаты по x с проверкой на столкновение со стенами
    def remove_cord_ox(self, step):
        self.rect.x += step
        for i in wall_group:
            if pygame.sprite.collide_mask(self, i):
                self.rect.x -= step
                return False
        self.rect.x -= step
        return True

    # Изменение координаты по y с проверкой на столкновение со стенами
    def remove_cord_oy(self, step):
        self.rect.y += step
        for i in wall_group:
            if pygame.sprite.collide_mask(self, i):
                self.rect.y -= step
                return False
        self.rect.y -= step
        return True
