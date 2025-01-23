import pygame as pg

class Fighter():
    def __init__(self, player, x, y):
        self.player = player
        self.flip = False
        self.rect = pg.Rect((x,y, 50, 100))
        self.dead = False
        self.vel_y = 0
        self.jump = False
        self.health = 100
        self.attacking = False
        self.kd = 0
    

    def move(self, surface, w, h, target):
        SPEED = 5
        GRAVITY = 1
        dx = 0
        dy = 0
        
        key = pg.key.get_pressed()

        if target.health <= 0:
            target.health = 0
            target.dead = True


        
        if self.player == 1 and not self.dead:
            #movement
            if key[pg.K_a]:
                dx = -SPEED
            if key[pg.K_d]:
                dx = SPEED

            #attacking
            if key[pg.K_r] and not self.attacking:
                self.attack(surface, target)

            #jump
            if key[pg.K_w] and not self.jump:
                self.vel_y = -20
                self.jump = True
            
            #gravity
            self.vel_y += GRAVITY
            dy += self.vel_y
        elif self.player == 2 and not self.dead:
            #movement
            if key[pg.K_LEFT]:
                dx = -SPEED
            if key[pg.K_RIGHT]:
                dx = SPEED

            #attacking
            if key[pg.K_RSHIFT] and not self.attacking:
                self.attack(surface, target)

            #jump
            if key[pg.K_UP] and not self.jump:
                self.vel_y = -20
                self.jump = True
            
            #gravity
            self.vel_y += GRAVITY
            dy += self.vel_y


        if self.attacking:
            self.kd+=1
            if self.kd == 50:
                self.attacking = False
                self.kd = 0
        
        
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > w:
            dx = w - self.rect.right
        if self.rect.bottom + dy > h - 60:
            self.vel_y = 0
            self.jump = False
            dy = h - 60 - self.rect.bottom

        
        if self.rect.centerx < target.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        self.rect.x += dx
        self.rect.y += dy
        


    def attack(self, surface, target):
        self.attacking = True
        attacking_rect = pg.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 10
        pg.draw.rect(surface, "Blue", attacking_rect)
    
    def draw(self, surface, color):
        pg.draw.rect(surface, color, self.rect)
