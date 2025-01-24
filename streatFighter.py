import pygame as pg
from sys import exit
from fighter import Fighter
from fighter2 import Fighter2


pg.mixer.init()
pg.init()

#colors
GREEN = (36, 144, 0)
BLACKR = (50, 0, 0 )
BLACKR2 = (81, 0, 0 )

# Размеры окна
W = 736 * 2
H = 414 * 2

#ui
ui = pg.image.load("graphics/ui_hp_bar.png")
ui = pg.transform.scale(ui, (W, H))


redw = pg.image.load("graphics/red_wins.png")
greenw = pg.image.load("graphics/green_wins.png")

def drawwinred():
    screen.blit(redw, (0,0))
def drawwgreen():
    screen.blit(greenw, (0,0))

#music
pg.mixer.music.load("sound/main_theme.mp3")
pg.mixer.music.set_volume(0 )
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
cube2 = Fighter2(2, W-150, H-160)

redwin = 0
greenwin = 0

resetgreen = Fighter(1, 100, H-160)
resetred = Fighter2(2, W-150, H-160)

rounds = [
    pg.transform.scale(pg.image.load("graphics/1.png"), (W, H)),
    pg.transform.scale(pg.image.load("graphics/2.png"), (W, H)),
    pg.transform.scale(pg.image.load("graphics/3.png"), (W, H))
]
round_delay = 1
current_round = 1
alpha = 255
pg.display.set_caption("Game!")

def drawHealthBar(x, y, health):

    ratio = health/100
    pg.draw.rect(screen, BLACKR2, (x-5, y-5, 610, 40))
    pg.draw.rect(screen, BLACKR, (x,y, 600 , 30))
    pg.draw.rect(screen, GREEN, (x,y, 600 * ratio, 30))


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
    screen.blit(ui, (0,0))

    cube1.update()
    cube2.update()

    cube1.draw(screen, "Green")
    cube2.draw(screen, "Red")
    

    drawHealthBar(80, 50, cube1.health)
    drawHealthBar(800, 50, cube2.health)

    drawKD(80, 100, cube1.kd) 
    drawKD(800, 100, cube2.kd)


    cube1.move(screen, W, H, cube2)
    cube2.move(screen, W, H, cube1)

    if cube1.dead and redwin >= 2:
        drawwinred()
    elif cube2.dead and greenwin >= 2:
        drawwgreen()
    else:
        if current_round <= 3:
            rounds[current_round-1].set_alpha(alpha)
            screen.blit(rounds[current_round-1], (0, 0))
            if alpha >= 0:
                alpha-=1
        if (cube1.dead or cube2.dead) and current_round < 3:
            if round_delay == 180:
                current_round += 1
                if cube1.dead:
                    redwin += 1
                if cube2.dead:
                    greenwin += 1
                cube1 = resetgreen
                cube2 = resetred
                alpha = 255
                print(cube1, greenwin, redwin)
                round_delay = 1
            round_delay+=1

    
    

    pg.display.update()
    clock.tick(60)