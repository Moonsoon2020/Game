from src.constans.gameconst import *
from src.game.entity import MoveableEntity
from src.game.functools import getimage


# Объект Бота
class Bot(MoveableEntity):
    def __init__(self, *args):
        self.image = getimage('bot')
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
