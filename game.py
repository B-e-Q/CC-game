import pygame as pg
from sys import exit
pg.mixer.init()

pg.init()

# Размеры окна
W = 736 * 2
H = 414 * 2

redw = pg.image.load("graphics/red_wins.png")
greenw = pg.image.load("graphics/green_wins.png")
#music
pg.mixer.music.load("sound/main_theme.mp3")
pg.mixer.music.set_volume(0.05)
pg.mixer.music.play(-1)
redw = pg.transform.scale(redw, (W, H))
greenw = pg.transform.scale(greenw, (W, H))

# Частота кадров
clock = pg.time.Clock()
screen = pg.display.set_mode((W, H))
bg = pg.image.load("graphics/background1.jpeg")
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
gunx1 = 130
guny1 = H-150
velocity_y1 = 0 
is_jumping1 = False
is_dead1 = False
ult1 = 2

cubex2 = W - 150
cubey2 = H - 200
velocity_y2 = 0
is_jumping2 = False
is_dead2 = False
ult2 = 2

# Гравитация
GRAVITY = 1

pg.display.set_caption("Game!")

# Эффект урона
damage_effect_opacity = 0
damage_effect_surface = pg.Surface((W, H), pg.SRCALPHA)
damage_effect_surface.fill((255, 0, 0, 128))  # Полупрозрачный красный

# Время выстрелов
kd1 = 0
kd2 = 0

# Линия выстрела
line1 = None
line2 = None

count = 0
#dead body
deadcube1 = pg.Surface((100, 50))
deadcube1.fill("green")
deadcube2 = pg.Surface((100, 50))
deadcube2.fill("red")

#gun
gun = pg.image.load("graphics/gun.jpg")
gunright = pg.transform.scale(gun, (50, 17))
gunleft = pg.transform.flip(gunright, 50, 0)


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    screen.blit(bg, (0, 0))
    keys = pg.key.get_pressed()

    # Управление игроком 1
    if not is_dead1:
        if keys[pg.K_a] and cubex1 > 0:  # Движение влево
            cubex1 -= 5
            gunx1 -= 5
        if keys[pg.K_d] and cubex1 < W - 50:  # Движение вправо
            cubex1 += 5
            gunx1 += 5
        if keys[pg.K_w] and not is_jumping1:  # Прыжок
            is_jumping1 = True
            velocity_y1 = -15
        if keys[pg.K_f]:  # Стрельба
            if kd1 >= 100:
                line1 = (cubex1 + 50, cubey1 + 50)
                kd1 = 0
            else:
                kd1+=1



    if kd1 > 0:
        kd1 -=0.25
    
    


    # Управление игроком 2
    if not is_dead2:
        if keys[pg.K_LEFT] and cubex2 > 0:  # Движение влево
            cubex2 -= 5
        if keys[pg.K_RIGHT] and cubex2 < W - 50:  # Движение вправо
            cubex2 += 5
        if keys[pg.K_UP] and not is_jumping2:  # Прыжок
            is_jumping2 = True
            velocity_y2 = -15
        if keys[pg.K_RSHIFT]:  # Стрельба
            if kd2 >= 100:
                line2 = (cubex2 - 50, cubey2 + 50)
                kd2  = 0
            else:
                kd2+=1

    if kd2 > 0:
        kd2 -= 0.25
    # Гравитация и прыжки для игрока 1
    if is_jumping1:
        guny1 += velocity_y1
        cubey1 += velocity_y1
        velocity_y1 += GRAVITY
        if cubey1 >= H - 200 and guny1 >= H - 150:
            cubey1 = H - 200
            guny1 = H - 150
            is_jumping1 = False

    # Гравитация и прыжки для игрока 2
    if is_jumping2:
        cubey2 += velocity_y2
        velocity_y2 += GRAVITY
        if cubey2 >= H - 200:
            cubey2 = H - 200
            is_jumping2 = False

    # Обновление линии выстрела игрока 1
    if line1 and not is_dead1:
        x, y = line1
        x += 10
        if x > W:
            line1 = None
        elif abs(x - cubex2) < 50 and abs(y - cubey2) < 100:
            HP2 -= 100
            damage_effect_opacity = 255
            line1 = None
            if HP2 == 0:
                is_dead2 = True
        else:
            pg.draw.rect(screen, "green", (x, y, 20, 10))
            line1 = (x, y)

    # Обновление линии выстрела игрока 2
    if line2 and not is_dead2:
        x, y = line2
        x -= 10
        if x < 0:
            line2 = None
        elif abs(x - cubex1) < 50 and abs(y - cubey1) < 100:
            HP1 -= 100
            damage_effect_opacity = 255
            line2 = None
            if HP1 == 0:
                is_dead1 = True
        else:
            pg.draw.rect(screen, "red", (x, y, 20, 10))
            line2 = (x, y)

    # Полоска здоровья
    pg.draw.rect(screen, "green", (50, 50, HP1 * 2, 20))
    pg.draw.rect(screen, "red", (W - 250, 50, HP2 * 2, 20))

    #kd toltyru
    pg.draw.rect(screen, "green", (50, 100, ult1 * kd1, 10))
    pg.draw.rect(screen, "red", (W - 250, 100, ult2 * kd2, 10))

    # Отрисовка кубов
    if is_dead1 or is_dead2:
        count+=1
        if count >= 180:
            if is_dead1:
                screen.blit(redw, (0, 0))
            else:
                screen.blit(greenw, (0, 0))
        else:
            if is_dead1:
                screen.blit(cube2, (cubex2, cubey2))
                screen.blit(deadcube1, (cubex1, cubey1+50))
            else:
                screen.blit(cube1, (cubex1, cubey1))
                screen.blit(gunright, (gunx1,guny1))
                screen.blit(deadcube2, (cubex2, cubey2+50))

    else:
        screen.blit(cube1, (cubex1, cubey1))
        screen.blit(cube2, (cubex2, cubey2))
        screen.blit(gunright, (gunx1,guny1))
        
        
    

    if keys[pg.K_r] and (is_dead1 or is_dead2):
        HP1 = 100
        HP2 = 100
        is_dead1 = False
        is_dead2 = False
        gunx1 = 130
        guny1 = H-150
        cubex1 = 100
        cubey1 = H - 200
        cubex2 = W - 150
        cubey2 = H - 200
        screen.blit(cube1, (cubex1, cubey1))
        screen.blit(cube2, (cubex2, cubey2))



    # Отрисовка эффекта урона
    if damage_effect_opacity > 0:
        damage_effect_surface.fill((255, 0, 0, damage_effect_opacity))  # Красный с текущей прозрачностью
        screen.blit(damage_effect_surface, (0, 0))  # Накладываем поверх экрана
        damage_effect_opacity = max(0, damage_effect_opacity - 5)  # Постепенное уменьшение прозрачности



    pg.display.update()
    clock.tick(60)