import pygame as pg
from sys import exit
import time

pg.init()

# Размеры окна
W = 736 * 2
H = 414 * 2

# Частота кадров
clock = pg.time.Clock()
screen = pg.display.set_mode((W, H))
bg = pg.image.load("/Users/dulatulynurasyl/VSCODE/Pygame/Game-CC/CC-game/graphics/background1.jpeg")
bg = pg.transform.scale(bg, (W, H))

# Параметры кубов
cube1 = pg.Surface((50, 100))
cube1.fill("green")
cube2 = pg.Surface((50, 100))
cube2.fill("red")

# Здоровье
HP1 = 100
HP2 = 100
HP_BAR_LENGTH = 200

# Координаты кубов
cubex1 = 100
cubey1 = H - 200
velocity_y1 = 0 
is_jumping1 = False

cubex2 = W - 150
cubey2 = H - 200
velocity_y2 = 0
is_jumping2 = False

# Гравитация
GRAVITY = 1

pg.display.set_caption("Game!")

# Эффект урона
damage_effect_opacity = 0
damage_effect_surface = pg.Surface((W, H), pg.SRCALPHA)
damage_effect_surface.fill((255, 0, 0, 128))  # Полупрозрачный красный

# Время выстрелов
last_shot_time1 = 0
last_shot_time2 = 0
SHOOT_COOLDOWN = 5  # Кулдаун в секундах

# Линия выстрела
line1 = None
line2 = None

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    screen.blit(bg, (0, 0))

    # Управление игроком 1
    keys = pg.key.get_pressed()
    if keys[pg.K_a] and cubex1 > 0:  # Движение влево
        cubex1 -= 5
    if keys[pg.K_d] and cubex1 < W - 50:  # Движение вправо
        cubex1 += 5
    if keys[pg.K_w] and not is_jumping1:  # Прыжок
        is_jumping1 = True
        velocity_y1 = -15
    if keys[pg.K_f] and time.time() - last_shot_time1 >= SHOOT_COOLDOWN:  # Стрельба
        line1 = (cubex1 + 50, cubey1 + 50)
        last_shot_time1 = time.time()

    # Управление игроком 2
    if keys[pg.K_LEFT] and cubex2 > 0:  # Движение влево
        cubex2 -= 5
    if keys[pg.K_RIGHT] and cubex2 < W - 50:  # Движение вправо
        cubex2 += 5
    if keys[pg.K_UP] and not is_jumping2:  # Прыжок
        is_jumping2 = True
        velocity_y2 = -15
    if keys[pg.K_RSHIFT] and time.time() - last_shot_time2 >= SHOOT_COOLDOWN:  # Стрельба
        line2 = (cubex2, cubey2 + 50)
        last_shot_time2 = time.time()

    # Гравитация и прыжки для игрока 1
    if is_jumping1:
        cubey1 += velocity_y1
        velocity_y1 += GRAVITY
        if cubey1 >= H - 200:
            cubey1 = H - 200
            is_jumping1 = False

    # Гравитация и прыжки для игрока 2
    if is_jumping2:
        cubey2 += velocity_y2
        velocity_y2 += GRAVITY
        if cubey2 >= H - 200:
            cubey2 = H - 200
            is_jumping2 = False

    # Обновление линии выстрела игрока 1
    if line1:
        x, y = line1
        x += 10
        if x > W:
            line1 = None
        elif abs(x - cubex2) < 50 and abs(y - cubey2) < 100:
            HP2 -= 5
            damage_effect_opacity = 255
            line1 = None
        else:
            pg.draw.line(screen, "green", (x, y), (x + 20, y), 5)
            line1 = (x, y)

    # Обновление линии выстрела игрока 2
    if line2:
        x, y = line2
        x -= 10
        if x < 0:
            line2 = None
        elif abs(x - cubex1) < 50 and abs(y - cubey1) < 100:
            HP1 -= 5
            damage_effect_opacity = 255
            line2 = None
        else:
            pg.draw.line(screen, "red", (x, y), (x - 20, y), 5)
            line2 = (x, y)

    # Полоска здоровья
    pg.draw.rect(screen, "green", (50, 50, HP1 * 2, 20))
    pg.draw.rect(screen, "red", (W - 250, 50, HP2 * 2, 20))

    # Отрисовка кубов
    screen.blit(cube1, (cubex1, cubey1))
    screen.blit(cube2, (cubex2, cubey2))

    # Отрисовка эффекта урона
    if damage_effect_opacity > 0:
        damage_effect_surface.fill((255, 0, 0, damage_effect_opacity))  # Красный с текущей прозрачностью
        screen.blit(damage_effect_surface, (0, 0))  # Накладываем поверх экрана
        damage_effect_opacity = max(0, damage_effect_opacity - 5)  # Постепенное уменьшение прозрачности

    pg.display.update()
    clock.tick(60)
