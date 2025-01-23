import pygame as pg
from sys import exit
from fighter import Fighter

pg.mixer.init()
pg.init()

# Размеры окна
W = 736 * 2
H = 414 * 2

redw = pg.image.load("graphics/red_wins.png")
greenw = pg.image.load("graphics/green_wins.png")

def drawwinred():
    screen.blit(redw, (0,0))
def drawwgreen():
    screen.blit(greenw, (0,0))

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
cube1 = Fighter(1, 100, H-160)
cube2 = Fighter(2, W-150, H-160)

pg.display.set_caption("Game!")

def drawHealthBar(x, y, health):
    ratio = health/100
    pg.draw.rect(screen, "White", (x-5, y-5, 610, 40))
    pg.draw.rect(screen, "Red", (x,y, 600 , 30))
    pg.draw.rect(screen, "Yellow", (x,y, 600 * ratio, 30))


def drawKD(x, y, kd):
    ratio = kd * 6
    pg.draw.rect(screen, "White", (x, y, 310, 15))
    pg.draw.rect(screen, "Red", (x, y, ratio, 15))


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    screen.blit(bg, (0,0))
    cube1.draw(screen, "Green")
    cube2.draw(screen, "Red")
    
    drawHealthBar(80, 50, cube1.health)
    drawHealthBar(800, 50, cube2.health)

    drawKD(80, 100, cube1.kd) 
    drawKD(800, 100, cube2.kd)


    cube1.move(screen, W, H, cube2)
    cube2.move(screen, W, H, cube1)

    if cube1.health == 0:
        drawwinred()
    elif cube2.health == 0:
        drawwgreen()

    pg.display.update()
    clock.tick(60)