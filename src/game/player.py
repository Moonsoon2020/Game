import pygame.mask
from src.constans.gameconst import TILE_WIDTH, KRAY, player_group
from src.game.entity import MoveableEntity
from src.game.functools import getimage

class Player(MoveableEntity):
    def __init__(self, pos_x, pos_y, width, height):
        super(Player, self).__init__(
            player_group, pos_x, pos_y)
        self.image = getimage("mar")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_WIDTH * pos_y)
        self.width = width
        self.height = height
        self.cords = [pos_x, pos_y]

    def print_x(self):
        print("x:", self.rect.x)

    def print_y(self):
        print("y:", self.rect.y)

    def print_x_p(self):
        print("x_p:", self.cords[0])

    def print_y_p(self):
        print("y_p:", self.cords[1])

    def remove_cord(self, step, paral):
        st = 1 if step > 0 else -1
        if paral == 'ox':
            if KRAY <= self.cords[0] + st <= self.width - KRAY - 1 and self.remove_cord_ox(step):
                self.cords[0] += st
                self.rect.x += step
        else:
            if KRAY <= self.cords[1] + st <= self.height - KRAY - 1 and self.remove_cord_oy(step):
                self.cords[1] += st
                self.rect.y += step

    def remove_cord_for_m(self, step_x, step_y):
        self.cords = [self.rect.x // TILE_WIDTH, self.rect.y // TILE_WIDTH]
        self.rect.x += step_x
        self.rect.y += step_y
