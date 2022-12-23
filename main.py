import sys
from clases import *

player = None


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
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


player = Player(random.randint(0, SIZE_MAP[0]), random.randint(0, SIZE_MAP[1]))
camera = Camera(player.x, player.y)


if __name__ == '__main__':
    board = GeneratePlay(SIZE_MAP[0], SIZE_MAP[1])
    cord = random.randint(0, SIZE_MAP[0]), random.randint(0, SIZE_MAP[1])
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.remove_cord(-STEP, 'ox')
                if event.key == pygame.K_RIGHT:
                    player.remove_cord(STEP, 'ox')
                if event.key == pygame.K_UP:
                    player.remove_cord(-STEP, 'oy')
                if event.key == pygame.K_DOWN:
                    player.remove_cord(STEP, 'oy')

        camera.update(player)

        for sprite in all_sprites:
            camera.apply(sprite)

        screen.fill(pygame.Color(0, 0, 0))
        all_sprites.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)
