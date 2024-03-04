import pygame
import os
import time
from pygame.math import Vector2

# Константы
FPS = 50
WIDTH_MAP = HEIGHT = 700
WIDTH = WIDTH_MAP + 300
KOF_START = 0.45
KOF_ENEMY = 0.05
SIZE_WINDOW = WIDTH_MAP, HEIGHT
STEP = TILE_WIDTH = 34
RES_MAP = 5
RES_RUD = 3
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

