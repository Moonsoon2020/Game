from src.constans.gameconst import *


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