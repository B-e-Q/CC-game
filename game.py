import pygame as pg
from sys import exit
import random

pg.init()

clock = pg.time.Clock()
screen = pg.display.set_mode((736, 414))
bg = pg.image.load("graphics/background.jpeg")

cube = pg.Surface((50,100))
cube.fill("green")

cubex = 100
cubey = 300

pg.display.set_caption("Game!")

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    screen.blit(bg, (0,0))
    screen.blit(cube, (cubex,cubey))

    keys = pg.key.get_pressed()

    # if keys[pg.K_w] and cubey >= 0:
    #     if keys[pg.K_w] and keys[pg.K_a] and cubex >= 0:
    #         cubey -= 2
    #         cubex -= 2
    #     if keys[pg.K_w] and keys[pg.K_d] and cubex <= 686:
    #         cubey -= 2
    #         cubex += 2
    #     else:
    #         cubey -= 2
    # elif keys[pg.K_s] and cubey <= 314:
    #     if keys[pg.K_s] and keys[pg.K_a] and cubex >= 0:
    #         cubey += 2
    #         cubex -= 2
    #     if keys[pg.K_s] and keys[pg.K_d] and cubex <= 686:
    #         cubey += 2
    #         cubex += 2
    #     else:
    #         cubey += 2
    if keys[pg.K_a] and cubex >= 0:
        cubex -= 2
    elif keys[pg.K_d] and cubex <= 686:
        cubex += 2
    
    pg.display.update()
    clock.tick(60)
    