import pygame as pg
from sys import exit

pg.init()

# Размеры окна
W = 736 * 2
H = 414 * 2

# Частота кадров
clock = pg.time.Clock()
screen = pg.display.set_mode((W, H))
bg = pg.image.load("Game-CC/CC-game/graphics/background1.jpeg")
bg = pg.transform.scale(bg, (W, H))

# Параметры кубо
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

arrows1 = []
arrows2 = []
arrow_speed = 7

kd1 = True
kd2 = True

pg.display.set_caption("Game!")

pg.display.set_caption("Game!")

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
    if keys[pg.K_f]:  # Стрельба
        arrows1.append({"x": cubex1 + 50, "y": cubey1 + 50, "vx": 7, "vy": -5})

    # Управление игроком 2
    if keys[pg.K_LEFT] and cubex2 > 0:  # Движение влево
        cubex2 -= 5
    if keys[pg.K_RIGHT] and cubex2 < W - 50:  # Движение вправо
        cubex2 += 5
    if keys[pg.K_UP] and not is_jumping2:  # Прыжок
        is_jumping2 = True
        velocity_y2 = -15
    if keys[pg.K_RSHIFT] & kd1:  # Стрельба
        arrows2.append({"x": cubex2, "y": cubey2 + 50, "vx": -7, "vy": -5})
        kd1 = False

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

 # Обновление стрел игрока 1
    for arrow in arrows1[:]:
        arrow["x"] += arrow["vx"]
        arrow["y"] += arrow["vy"]
        arrow["vy"] += GRAVITY * 0.2  # Гравитация на стрелы
        if arrow["x"] > W or arrow["y"] > H:
            arrows1.remove(arrow)
        elif abs(arrow["x"] - cubex2) < 50 and abs(arrow["y"] - cubey2) < 100:
            HP2 -= 5
            arrows1.remove(arrow)

    # Обновление стрел игрока 2
    for arrow in arrows2[:]:
        arrow["x"] += arrow["vx"]
        arrow["y"] += arrow["vy"]
        arrow["vy"] += GRAVITY * 0.2  # Гравитация на стрелы
        if arrow["x"] < 0 or arrow["y"] > H:
            arrows2.remove(arrow)
        elif abs(arrow["x"] - cubex1) < 50 and abs(arrow["y"] - cubey1) < 100:
            HP1 -= 5
            arrows2.remove(arrow)

    # Атаки
    if keys[pg.K_SPACE]:  # Атака игрока 1
        if abs(cubex1 - cubex2) < 60 and abs(cubey1 - cubey2) < 100:
            HP2 -= 1

    if keys[pg.K_RETURN]:  # Атака игрока 2
        if abs(cubex2 - cubex1) < 60 and abs(cubey2 - cubey1) < 100:
            HP1 -= 1

    # Полоска здоровья
    pg.draw.rect(screen, "green", (50, 50, HP1 * 2, 20))
    pg.draw.rect(screen, "red", (W - 250, 50, HP2 * 2, 20))

    # Отрисовка кубов
    screen.blit(cube1, (cubex1, cubey1))
    screen.blit(cube2, (cubex2, cubey2))

    for arrow in arrows1:
        pg.draw.circle(screen, "green", (int(arrow["x"]), int(arrow["y"])), 5)
    for arrow in arrows2:
        pg.draw.circle(screen, "red", (int(arrow["x"]), int(arrow["y"])), 5)

    pg.display.update()
    clock.tick(60)
