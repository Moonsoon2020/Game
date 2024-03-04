from src.constans.gameconst import *
from src.game.functools import getimage

class ScreenInfo:
    def __init__(self):
        self.screen_info = pygame.Surface((WIDTH - WIDTH_MAP, HEIGHT))
        self.fill_rect()
        self.get_images()

    def get_images(self):
        self.rud_image = getimage('alm')
        self.bur_magaz_image = pygame.transform.scale(getimage('bur_m'), (40, 40))
        self.turel_magaz_image = pygame.transform.scale(getimage('turel_m'), (40, 40))
        self.bur_magaz_image_no_ust = getimage('bur_for_magaz_no_ustan')
        self.wall_magaz_image = getimage('wal')

    def fill_rect(self):
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

    def update_screen_info(self, fps, game_state):
        """загрузка окна с информацией"""
        pygame.draw.rect(self.screen_info, (0, 0, 0), (0, 0, 5, HEIGHT), 5)
        pygame.draw.rect(self.screen_info, (0, 0, 0), (0, HEIGHT // 2.5, WIDTH - WIDTH_MAP, 5), 3)
        string_text_rud = self.font.render('-  ' + str(game_state.rud), True, pygame.Color('black'))
        intro_rect_rud = string_text_rud.get_rect()
        intro_rect_rud.x = 60
        intro_rect_rud.y = 50
        string_text_cord = self.font.render(f' {game_state.player.cords[0] - KRAY} {game_state.player.cords[1] - KRAY}', True,
                                            pygame.Color('black'))
        intro_rect_cord = string_text_cord.get_rect()
        intro_rect_cord.x = 150
        intro_rect_cord.y = 90
        string_text_time = self.font.render(f' {game_state.min} {game_state.sec}', True, pygame.Color('black'))
        intro_rect_time = string_text_time.get_rect()
        intro_rect_time.x = 150
        intro_rect_time.y = 120
        string_text_fps = self.font.render(f' {round(fps, 2)}', True, pygame.Color('black'))
        intro_rect_fps = string_text_fps.get_rect()
        intro_rect_fps.x = 150
        intro_rect_fps.y = 150
        self.screen_info.blit(self.string_text_res_comlex, self.intro_rect_res_comlex)
        self.screen_info.blit(self.string_text_build_complex, self.intro_rect_build_complex)
        self.screen_info.blit(self.string_text_cords, self.intro_rect_cords)
        self.screen_info.blit(string_text_rud, intro_rect_rud)
        self.screen_info.blit(string_text_cord, intro_rect_cord)
        self.screen_info.blit(string_text_time, intro_rect_time)
        self.screen_info.blit(string_text_fps, intro_rect_fps)
        self.screen_info.blit(self.string_text_exit, self.intro_rect_exit)
        self.screen_info.blit(self.string_text_time, self.intro_rect_time)
        self.screen_info.blit(self.string_text_fps, self.intro_rect_fps)
        self.screen_info.blit(self.rud_image, (10, 40))
        self.screen_info.blit(self.bur_magaz_image, (10, 330))
        self.screen_info.blit(self.turel_magaz_image, (60, 330))
        self.screen_info.blit(self.wall_magaz_image, (110, 330))
        self.screen_info.blit(self.bur_magaz_image_no_ust, (10, 380))
        if game_state.position == 'bur':
            pygame.draw.rect(self.screen_info, (0, 0, 0), (8, 330, 42, 42), 2)
        elif game_state.position == 'tur':
            pygame.draw.rect(self.screen_info, (0, 0, 0), (58, 330, 42, 42), 2)
        elif game_state.position == 'wal':
            pygame.draw.rect(self.screen_info, (0, 0, 0), (108, 330, 42, 42), 2)
        elif game_state.position == 'lom':
            pygame.draw.rect(self.screen_info, (0, 0, 0), (8, 378, 42, 42), 2)

    def update(self, fps, game_state):
        self.screen_info.fill(pygame.Color('white'))
        self.update_screen_info(fps, game_state)
