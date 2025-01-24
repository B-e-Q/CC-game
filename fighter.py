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
        self.bullet = None
        self.hit = True
        self.shotkd = 0
<<<<<<< HEAD
=======
        self.dir = 1

        self.sam_idle = []
        for i in range(1, 16):
            path = f"/Users/dulatulynurasyl/VSCODE/Pygame/graphics/sam_idle/sam_idle{i}.png"
            frame = pg.image.load(path).convert_alpha()
            self.sam_idle.append(frame)

        self.current_frame = 0     
        self.frame_counter = 0       
        self.frame_delay = 5        

        self.sam_run = []
        for i in range(1, 17):
            path = f"/Users/dulatulynurasyl/VSCODE/Pygame/graphics/sam_run/sam_run{i}.png"
            frame = pg.image.load(path).convert_alpha()
            self.sam_run.append(frame)

        self.sam_jump = []
        for i in range(1, 10): 
            path = f"/Users/dulatulynurasyl/VSCODE/Pygame/graphics/sam_jump/sam_jump{i}.png"
            frame = pg.image.load(path).convert_alpha()
            self.sam_jump.append(frame)

        self.current_animation = "idle"
>>>>>>> patch 1.5
        


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
<<<<<<< HEAD
            if key[pg.K_d]:
                dx = SPEED
=======
                self.current_animation = "run"
            if key[pg.K_d]:
                dx = SPEED
                self.current_animation = "run"

            if not(key[pg.K_a] or key[pg.K_d]) and not(self.jump):
                self.current_animation = "idle" #returning to idle
>>>>>>> patch 1.5

            #attacking
            if key[pg.K_r] and not self.attacking:
                self.attack(surface, target)

            #jump
            if key[pg.K_w] and not self.jump:
                self.vel_y = -20
                self.jump = True
<<<<<<< HEAD
=======
                self.current_animation = "jump"
            
            if self.jump:
                self.current_animation = "idle"
>>>>>>> patch 1.5
            
            #gravity
            self.vel_y += GRAVITY
            dy += self.vel_y

            #shot
            if key[pg.K_f] and self.hit:
                self.bullet = (self.rect.centerx + 30 * (-1)** self.flip, self.rect.centery)
                self.shotkd = 0
            
            



        elif self.player == 2 and not self.dead:
            #movement
            if key[pg.K_LEFT]:
                dx = -SPEED
<<<<<<< HEAD
            if key[pg.K_RIGHT]:
                dx = SPEED
=======
                self.current_animation = "run"
            if key[pg.K_RIGHT]:
                dx = SPEED
                self.current_animation = "run"
            if not(key[pg.K_a] or key[pg.K_d]) and not(self.jump):
                self.current_animation = "idle" #returning to idle
>>>>>>> patch 1.5

            #attacking
            if key[pg.K_RSHIFT] and not self.attacking:
                self.attack(surface, target)

            #jump
<<<<<<< HEAD
            if key[pg.K_UP] and not self.jump:
                self.vel_y = -20
                self.jump = True
=======
            if key[pg.K_w] and not self.jump:
                self.vel_y = -20
                self.jump = True
                self.current_animation = "jump"
            
            if self.jump:
                self.current_animation = "idle"
>>>>>>> patch 1.5
            
            #gravity
            self.vel_y += GRAVITY
            dy += self.vel_y

            if key[pg.K_l] and self.hit and self.shotkd == 10:
                self.bullet = (self.rect.centerx + 30 * (-1)** self.flip, self.rect.centery)
                self.shotkd = 0


        if self.attacking:
            self.kd+=1
            if self.kd == 50:
                self.attacking = False
                self.kd = 0
        


        if self.hit:
            self.shotkd +1
        

        self.too_close(target, surface)
        
        self.shoot(surface, "Yellow", w, target)
        
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
        self.dead_rect = pg.Rect((self.rect.x-50,self.rect.y+50, 100, 50))
        


    def attack(self, surface, target):
        self.attacking = True
        attacking_rect = pg.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 10
        pg.draw.rect(surface, "Blue", attacking_rect)
    

    def too_close(self, target, surface):
        close_rect = pg.Rect(self.rect.centerx - (10 * self.rect.width * self.flip), self.rect.y - 60, 10 * self.rect.width, self.rect.height + 60)
        if close_rect.colliderect(target.rect):
            self.hit = False
        else:
            self.hit = True


    def shoot(self, surface, color, w, target):
        if self.bullet:
            x, y = self.bullet
            x += 10 * (-1)**self.flip
            bullet = pg.Rect(x , y, 10, 5)
            self.hit = False
            if x > w or x < 0:
                self.bullet = None
            elif bullet.colliderect(target.rect):
                target.health -= 10
                self.bullet = None
                self.hit = True
            else:
                pg.draw.rect(surface, color, bullet)
                self.bullet = (x, y)
    
    def draw(self, surface, color):
<<<<<<< HEAD
        if self.dead:
            pg.draw.rect(surface, color, self.dead_rect)
        else:
            pg.draw.rect(surface, color, self.rect)
=======
        if self.current_animation == "idle":
            frame = self.sam_idle[self.current_frame]
        elif self.current_animation == "run":
            frame = self.sam_run[self.current_frame]
        elif self.current_animation == "jump":
            frame = self.sam_jump[self.current_frame]

        # Если dir == -1, кадр зеркально отображается
        
        frame = pg.transform.flip(frame, self.flip, False)

        surface.blit(frame, (self.rect.x - 190, self.rect.y - 120))  # Смещение анимации

        # Логика переключения кадров
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(
                self.sam_idle if self.current_animation == "idle"
                else self.sam_run if self.current_animation == "run"
                else self.sam_jump
            )
            self.frame_counter = 0
>>>>>>> patch 1.5
