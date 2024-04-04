import json
import random
import easygui
import pygame
import time
from render_opt import render_options, message
from new_sample import new_sample

WIDTH = 800
HEIGHT = 700
is_FS = False
FPS = 60
w_n = 800
h_n = 700
error = False
G = 6.67430 / (10 ** (11))
k = 1000000
m = 5.9722 * 10 ** 24
r = 6371000
w_x = -600000000
w_y = -450000000
error_list = {'wrong': 'Неверный тип файла!'}
set_stop = False
stop = False
setup = pygame.image.load('set.png')
vrem_k = 1
colors = ['white', 'red', 'orange', 'green', 'blue', 'yellow', 'pink']
color = colors[4]
color_k = 4
pygame.init()
mon_inf = pygame.display.Info()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Гравитация")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 36)
text_FPS = font.render('FPS: ' + str(FPS), True, 'green')
text_vrem_k = font.render('Время: x' + str(vrem_k), True, 'green')
text_pause = font.render(f'PAUSED', True, 'red')
last_size = screen.get_size()
FULLSCREEN_SIZE = (mon_inf.current_w, mon_inf.current_h)
currunt_size = screen.get_size()
ball_change = {'r': False, 'm': False}

class Ball():
    def __init__(self, real_x, real_y, real_r, m, colour, name=False, status=True):
        self.real_x = real_x
        self.real_y = real_y
        self.real_r = real_r
        self.m = m
        self.colour = colour
        self.speed = [0, 0]
        self.a = [0, 0]
        self.f = [0, 0]
        self.trace_count = 0
        self.trace = []
        self.status = status
        if not name:
            c = [chr(i) for i in range(97, 122)]
            name = ''.join([random.choice(c) for i in range(8)])
            self.name = name
        else:
            self.name = name

    def update(self):
        self.a[0] = (self.f[0] / self.m) * (vrem_k ** 2) / FPS ** 2
        self.a[1] = (self.f[1] / self.m) * (vrem_k ** 2) / FPS ** 2

        self.speed[0] += self.a[0]
        self.speed[1] += self.a[1]

        self.real_x += self.speed[0]
        self.real_y += self.speed[1]

        # траектория:
        self.trace_count += (self.speed[0] ** 2 + self.speed[1] ** 2) ** 0.5
        if self.trace_count / k >= 5:
            self.trace_count = 0
            self.trace.append((self.real_x,
                               self.real_y))
        if len(self.trace) > 1000:
            self.trace.pop(0)

    def draw(self):
        pygame.draw.circle(screen,
                           self.colour,
                           ((self.real_x - w_x) / k,
                            (self.real_y - w_y) / k),
                           self.real_r / k
                           )
        for i in self.trace:
            pygame.draw.circle(screen,
                               self.colour,
                               ((i[0] - w_x) / k,
                                (i[1] - w_y) / k),
                               1)

    def info(self):
        return {'name': self.name, 'real_x': self.real_x, 'real_y': self.real_y, 'real_r': self.real_r,
                'm': self.m, 'colour': self.colour, 'speed': self.speed}


balls = []
p = Ball(0, 0, 6371000, 5.9722 * 10 ** 24, 'blue')
balls.append(p)

p = Ball(149.6 * 10 ** 9, 0, 696_000_000, 1.9891 * 10 ** 30, 'red')
balls.append(p)
balls[0].speed[1] += 29782.77 * vrem_k / FPS

tick = 0
tm = time.time()
running = True
while running:
    clock.tick(FPS)
    tick += 1
    if tick == 100:
        tick = 0
        text_FPS = font.render('FPS: ' + str(int((100 / (time.time() - tm)))), True,
                               'green')

        tm = time.time()

    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            if is_FS:
                w_n = 800
                h_n = 700
            else:
                w_n = mon_inf.current_w
                h_n = mon_inf.current_h
            is_FS = not is_FS
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not set_stop:
                stop = not stop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            keys = pygame.key.get_pressed()
            xx = event.pos[0]
            yy = event.pos[1]
            jump_x = w_x + xx * k
            jump_y = w_y + yy * k
            if set_stop:
                if 10 <= xx <= 380:
                    if 370 <= yy <= 420:
                        input_file = easygui.fileopenbox(filetypes=["*.json"], default="*.json")
                        if input_file:
                            try:
                                new_sample([i.info() for i in balls], input_file, vrem_k)
                            except:
                                error = True
                                error_type = 'wrong'
                    elif 315 <= yy <= 365:
                        input_file = easygui.fileopenbox(filetypes=["*.json"], default="*.json")
                        if input_file:
                            try:
                                if input_file[-4:] == 'json':
                                    f = open(input_file)
                                    file = json.load(f)
                                    if file[0] == 'for planets':
                                        balls = []
                                        vrem_k = int(file[1])
                                        for i in file[2:]:
                                            balls.append(
                                                Ball(float(i['real_x']), float(i['real_y']), float(i['real_r']),
                                                     float(i['m'])
                                                     , i['colour'],
                                                     i['name']))
                                    else:
                                        error = True
                                        error_type = 'wrong'
                            except:
                                error = True
                                error_type = 'wrong'


                        else:
                            pass
                if 350 <= xx <= 400:
                    if 60 <= yy <= 84:
                        if FPS < 120:
                            FPS += 5
                    elif 85 <= yy <= 110:
                        if FPS > 5:
                            FPS -= 5
                    elif 160 <= yy <= 184:
                        m = round(m * 1.05, 4)
                        #m *= 1.05
                    elif 185 <= yy <= 210:
                        #m /= 1.05
                        m = round(m / 1.05, 4)
                    elif 260 <= yy <= 284:
                        #r *= 1.05
                        r = round(r * 1.05, 4)
                    elif 285 <= yy <= 310:
                        #r /= 1.05
                        r = round(r / 1.05, 4)

                    elif 450 <= yy <= 484:
                        color_k = (color_k + 1) % 7
                        color = colors[color_k]
                    elif 485 <= yy <= 510:
                        color_k = (color_k - 1) % 7
                        color = colors[color_k]

            if w_n - 60 <= xx <= w_n:
                if 0 <= yy <= 60:
                    if not set_stop:
                        stop = True
                        set_stop = not set_stop
                    else:
                        stop = True
                        set_stop = not set_stop
                        error = []

            if event.button == 4 and not set_stop:
                if keys[pygame.K_LCTRL]:
                    if vrem_k == 10000:
                        vrem_k = 1
                        #
                        for i in balls:
                            i.speed[0] /= 10000
                            i.speed[1] /= 10000
                    else:
                        vrem_k *= 10
                        #
                        for i in balls:
                            i.speed[0] *= 10
                            i.speed[1] *= 10
                    text_vrem_k = font.render('Время: x' + str(vrem_k), True, 'green')
                else:
                    k = k * 0.85

                    w_x = jump_x - xx * k
                    w_y = jump_y - yy * k
            if event.button == 5 and not set_stop:
                if keys[pygame.K_LCTRL]:
                    if vrem_k == 1:
                        vrem_k = 100000
                        #
                        for i in balls:
                            i.speed[0] *= 100000
                            i.speed[1] *= 100000
                    else:
                        vrem_k //= 10
                        #
                        for i in balls:
                            i.speed[0] /= 10
                            i.speed[1] /= 10
                    text_vrem_k = font.render('Время: x' + str(vrem_k), True, 'green')
                else:
                    k = k / 0.85
                    w_x = jump_x - xx * k
                    w_y = jump_y - yy * k
            if event.button == 3 and not set_stop:
                balls.append(Ball(jump_x, jump_y, r, m, color))

        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0] == True:
                w_x -= event.rel[0] * k
                w_y -= event.rel[1] * k
        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0] == True:
                w_x -= event.rel[0] * k
                w_y -= event.rel[1] * k
    if not stop:
        if vrem_k == 100000:
            vrem_k //= 1
            for _ in range(1):
                collisions = []
                for i in range(len(balls)):
                    for j in range(i + 1, len(balls)):
                        dx = balls[j].real_x - balls[i].real_x
                        dy = balls[j].real_y - balls[i].real_y
                        d = (dx ** 2 + dy ** 2) ** 0.5
                        ff = G * balls[i].m * balls[j].m / d ** 2

                        balls[i].f[0] += dx * ff / d
                        balls[i].f[1] += dy * ff / d

                        balls[j].f[0] -= dx * ff / d
                        balls[j].f[1] -= dy * ff / d

                        if balls[i].real_r > d - balls[j].real_r:
                            collisions.append((i, j))

                for i in collisions:
                    t1 = balls[i[0]]
                    t2 = balls[i[1]]
                    if t1.status and t2.status:
                        t1.status = False
                        t2.status = False
                        if t1.real_r > t2.real_r:
                            c = t1.colour
                        else:
                            c = t2.colour

                        t = Ball((t1.real_x * t1.m + t2.real_x * t2.m) / (t1.m + t2.m),
                                 (t1.real_y * t1.m + t2.real_y * t2.m) / (t1.m + t2.m),
                                 (t1.real_r ** 3 + t2.real_r ** 3) ** (1 / 3),
                                 t1.m + t2.m,
                                 c)
                        t.speed[0] = (t1.m * t1.speed[0] + t2.m * t2.speed[0]) / (t1.m + t2.m)
                        t.speed[1] = (t1.m * t1.speed[1] + t2.m * t2.speed[1]) / (t1.m + t2.m)
                        balls.append(t)

                tt = []
                for ball in balls:
                    if ball.status:
                        tt.append(ball)
                balls = tt
                for ball in balls:
                    ball.update()
                    ball.f = [0, 0]
            vrem_k *= 1
        else:
            collisions = []
            for i in range(len(balls)):
                for j in range(i + 1, len(balls)):
                    dx = balls[j].real_x - balls[i].real_x
                    dy = balls[j].real_y - balls[i].real_y
                    d = (dx ** 2 + dy ** 2) ** 0.5
                    if d == 0:
                        d = 1
                    ff = G * balls[i].m * balls[j].m / d ** 2

                    balls[i].f[0] += dx * ff / d
                    balls[i].f[1] += dy * ff / d

                    balls[j].f[0] -= dx * ff / d
                    balls[j].f[1] -= dy * ff / d

                    if balls[i].real_r > d - balls[j].real_r:
                        collisions.append((i, j))

            for i in collisions:
                t1 = balls[i[0]]
                t2 = balls[i[1]]
                if t1.status and t2.status:
                    t1.status = False
                    t2.status = False
                    if t1.real_r > t2.real_r:
                        c = t1.colour
                    else:
                        c = t2.colour

                    t = Ball((t1.real_x * t1.m + t2.real_x * t2.m) / (t1.m + t2.m),
                             (t1.real_y * t1.m + t2.real_y * t2.m) / (t1.m + t2.m),
                             (t1.real_r ** 3 + t2.real_r ** 3) ** (1 / 3),
                             t1.m + t2.m,
                             c)
                    t.speed[0] = (t1.m * t1.speed[0] + t2.m * t2.speed[0]) / (t1.m + t2.m)
                    t.speed[1] = (t1.m * t1.speed[1] + t2.m * t2.speed[1]) / (t1.m + t2.m)
                    balls.append(t)

            tt = []
            for ball in balls:
                if ball.status:
                    tt.append(ball)
            balls = tt
            for ball in balls:
                ball.update()
                ball.f = [0, 0]
    screen.fill('black')
    if set_stop:
        render_options(screen, font, FPS, m, r, color=color)
        if error:
            message(f'Неверный формат файла!', screen, w_n, h_n)

    else:
        for ball in balls:
            ball.draw()
        screen.blit(text_FPS, (10, 10))
        screen.blit(text_vrem_k, (10, 50))
        if not set_stop:
            text_test = font.render(' '.join([str(i) for i in balls[0].speed]), True, 'green')
            screen.blit(text_FPS, (10, 10))
            screen.blit(text_vrem_k, (10, 50))
        if stop:
            screen.blit(text_pause, (w_n / 2 - 50, 10))
            screen.blit(text_FPS, (10, 10))
            screen.blit(text_vrem_k, (10, 50))
    screen.blit(setup, (w_n - 60, 0))
    pygame.display.update()

    pygame.display.update()
pygame.quit()
