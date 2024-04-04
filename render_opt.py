import pygame


def render_options(screen, font, FPS, m, r, color=False):
    text_FPS_now = font.render(f'Текущий лимит FPS: {FPS}', True,
                               'green')
    text_FPS_red = font.render(f'Изменить лимит FPS', True,
                               'green')
    screen.blit(text_FPS_now, (10, 10))
    screen.blit(text_FPS_red, (10, 60))
    pygame.draw.lines(screen, 'green', True,
                      [[350, 100 - 20 + 100 + 5], [400, 100 - 20 + 100 + 5], [375, 125 - 20 + 100 + 5]])
    pygame.draw.lines(screen, 'green', True,
                      [[350, 100 - 20 + 100 - 5], [400, 100 - 20 + 100 - 5], [375, 75 - 20 + 100 - 5]])
    text_m_now = font.render(f'Текущий масса тела: {m}кг', True,
                             'green')
    text_m_red = font.render(f'Изменить массу тела', True,
                             'green')
    screen.blit(text_m_now, (10, 10 + 100))
    screen.blit(text_m_red, (10, 60 + 100))
    pygame.draw.lines(screen, 'green', True, [[350, 100 - 20 + 5], [400, 100 - 20 + 5], [375, 125 - 20 + 5]])
    pygame.draw.lines(screen, 'green', True, [[350, 100 - 20 - 5], [400, 100 - 20 - 5], [375, 75 - 20 - 5]])
    text_r_now = font.render(f'Текущий радиус тела: {r}м', True,
                             'green')
    text_r_red = font.render(f'Изменить радиус тела', True,
                             'green')
    screen.blit(text_r_now, (10, 10 + 200))
    screen.blit(text_r_red, (10, 60 + 200))
    pygame.draw.lines(screen, 'green', True,
                      [[350, 100 - 20 + 5 + 200], [400, 100 - 20 + 5 + 200], [375, 125 - 20 + 5 + 200]])
    pygame.draw.lines(screen, 'green', True,
                      [[350, 100 - 20 - 5 + 200], [400, 100 - 20 - 5 + 200], [375, 75 - 20 - 5 + 200]])
    text_sample_choose = font.render(f'Выбрать шаблон карты', True,
                                     'green')
    screen.blit(text_sample_choose, (20, 315))
    pygame.draw.rect(screen, 'green', (10, 315, 370, 50), 1)
    text_sample_save = font.render(f'Сохранить шаблон карты', True,
                                   'green')
    screen.blit(text_sample_save, (20, 365 + 5))
    pygame.draw.rect(screen, 'green', (10, 365 + 5, 370, 50), 1)
    pygame.draw.lines(screen, 'green', True,
                      [[350, 100 - 20 + 5 + 400], [400, 100 - 20 + 5 + 400], [375, 125 - 20 + 5 + 400]])
    pygame.draw.lines(screen, 'green', True,
                      [[350, 100 - 20 - 5 + 400], [400, 100 - 20 - 5 + 400], [375, 75 - 20 - 5 + 400]])
    text_color = font.render(f'Цвет: ', True,
                             'green')
    screen.blit(text_color, (20, 460))
    pygame.draw.rect(screen, 'green', (100, 460, 250, 50), 1)
    text_color_choose = font.render(color, True, color)
    screen.blit(text_color_choose, (185, 462))


def message(info, screen, w, h):
    font = pygame.font.SysFont('arial', 60)
    text_sample_choose = font.render(info, True,
                                     'red')
    ots = w / 2 - len(info) * 15
    h = h - 160
    screen.blit(text_sample_choose, (ots, h))
