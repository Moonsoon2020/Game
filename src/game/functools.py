from src.constans.gameconst import *
from src.constans.gameconst import WIDTH, HEIGHT
import os

# Updaters
def restarted():
    global all_sprites, block_group, bots_group, player_group, wall_group, rud_group, mine_group, turel_group
    global wall_ust_group, ust_block, v_group, tile_images, screen, screen_map, screen_info, sound_g, sound_v
    pygame.init()
    pygame.mixer.music.load('data/music/osn.wav')
    # pygame.mixer.music.play()
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
    sound_g = pygame.mixer.Sound('data/music/osn.wav')
    sound_v = pygame.mixer.Sound('data/music/v.wav')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.key.set_repeat(200, 70)
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
    return screen, sound_v, sound_g

# Загрузка изображений

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

def getimage(key):
    return tile_images[key]

# Отключение игры
def terminate():
    pygame.quit()
    # sys.exit()


# Проверка на соприкосновение и возможность атаки
def circle_collision(left, right):
    distance = Vector2(left.rect.center).distance_to(right.rect.center)
    return distance < left.radius