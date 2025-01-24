import pygame as pg

class Fighter():
    def __init__(self, player, x, y):
        self.player = player
        self.flip = False
        self.animation_list = self.load_images()
        self.action = 0 #0:idle , 1:run , 2:jump , 3:fireball , 4:attack , 5:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pg.time.get_ticks()
        self.rect = pg.Rect((x,y, 50, 160))
        self.dead = False
        self.vel_y = 0
        self.jump = False
        self.health = 100
        self.attacking = False
        self.bullet = None
        self.hit = True
        self.shotkd = 0
        self.kd = 0
        self.running = False
        self.current_fireball_frame = 0  
        self.fireball_frame_counter = 0  
        self.fireball_frame_delay = 3

        
    def load_images(self):
        sam_idle = []
        for i in range(1, 16):
            path = f"graphics/sam_idle/sam_idle{i}.png"
            frame = pg.image.load(path).convert_alpha()
            sam_idle.append(frame)
        sam_run = []
        for i in range(1, 17):
            path = f"graphics/sam_run/sam_run{i}.png"
            frame = pg.image.load(path).convert_alpha()
            sam_run.append(frame)
        sam_jump = []
        for i in range(1, 10): 
            path = f"graphics/sam_jump/sam_jump{i}.png"
            frame = pg.image.load(path).convert_alpha()
            sam_jump.append(frame)
        fireball = []  
        for i in range(1, 6):  
            path = f"graphics/projectile/fireball{i}.png"
            frame = pg.image.load(path).convert_alpha()
            frame = pg.transform.scale(frame, (50, 50))
            fireball.append(frame)
        attack = []  
        for i in range(1, 7):  
            path = f"graphics/sam_attack/sam_attack{i}.png"
            frame = pg.image.load(path).convert_alpha()
            attack.append(frame)
        death = []  
        for i in range(1, 17):  
            path = f"graphics/sam_death/sam_death{i}.png"
            frame = pg.image.load(path).convert_alpha()
            death.append(frame)
        
        animation_list = [sam_idle, sam_run, sam_jump, fireball, attack, death]
        return animation_list

            


    def move(self, surface, w, h, target):
        SPEED = 5
        GRAVITY = 1
        dx = 0
        dy = 0
        self.running = False
        
        key = pg.key.get_pressed()

        if target.health <= 0:
            target.health = 0
            target.dead = True
        

        #First player
        if self.player == 1 and not self.dead and not self.attacking:
            #movement
            if key[pg.K_a]:
                dx = -SPEED
                self.running = True
            if key[pg.K_d]:
                dx = SPEED
                self.running = True
                self.current_animation = "run"
            #attacking
            if key[pg.K_r] and not self.jump:
                self.attack(surface, target)

            #jump
            if key[pg.K_w] and not self.jump:
                self.vel_y = -20
                self.jump = True
            
            #gravity
            self.vel_y += GRAVITY
            dy += self.vel_y

            #shot
            if key[pg.K_f] and self.hit:
                self.bullet = (self.rect.centerx + 30 * (-1)** self.flip, self.rect.centery)
                self.shotkd = 0
            
            


        #second player
        elif self.player == 2 and not self.dead and not self.attacking:
            #movement
            if key[pg.K_LEFT]:
                dx = -SPEED
                self.running = True

            if key[pg.K_RIGHT]:
                dx = SPEED
                self.running = True

            #attacking
            if key[pg.K_RSHIFT] and not self.jump:
                self.attack(surface, target)

            #jump
            if key[pg.K_UP] and not self.jump:
                self.vel_y = -20
                self.jump = True


            #gravity
            self.vel_y += GRAVITY
            dy += self.vel_y

            if key[pg.K_l] and self.hit:
                self.bullet = (self.rect.centerx + 30 * (-1)** self.flip, self.rect.centery)
                self.shotkd = 0
        


        if self.hit:
            self.shotkd += 1
        

        self.too_close(target, surface)
        
        self.shoot(surface, w, target)
        
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
        
        if self.kd > 0:
            self.kd -= 1

        self.rect.x += dx
        self.rect.y += dy
       
        

    def update(self):
        animation_cooldown = 100
        #check action
        if self.dead:
            animation_cooldown = 200
            self.update_action(5)
        elif self.attacking:
            self.update_action(4)
        elif self.jump:
            self.update_action(2)
            animation_cooldown = 50
        elif self.running:
            self.update_action(1)
        else:
            self.update_action(0)

        self.image = self.animation_list[self.action][self.frame_index]
        if pg.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pg.time.get_ticks()
        
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            if self.action == 4:
                self.attacking = False
                self.kd = 50
        

    def attack(self, surface, target):
        if self.kd == 0:
            self.attacking = True
            attacking_rect = pg.Rect(self.rect.centerx - (4 * self.rect.width * self.flip), self.rect.y, 4 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
        

    def too_close(self, target, surface):
        close_rect = pg.Rect(self.rect.centerx - (10 * self.rect.width * self.flip), self.rect.y - 60, 10 * self.rect.width, self.rect.height + 60)
        if close_rect.colliderect(target.rect):
            self.hit = False
        else:
            self.hit = True


    def shoot(self, surface, w, target):
        if self.bullet:
            # Получаем текущие координаты патрона
            x, y = self.bullet
            x += 15 * (-1) ** self.flip
            bullet = pg.Rect(x, y, 10, 5)

            # Обработка столкновений и выхода за пределы экрана
            self.hit = False
            if x > w or x < 0:  # Патрон вышел за пределы экрана
                self.bullet = None
            elif bullet.colliderect(target.rect):  # Патрон попал в цель
                target.health -= 10
                self.bullet = None
                self.hit = True
            else:

                # Отображение анимации патрона
                fireball_frame = self.animation_list[3][self.current_fireball_frame]  # Получаем текущий кадр
                fireball_frame = pg.transform.flip(fireball_frame, self.flip, False)
                surface.blit(fireball_frame, (x - 30, y - 30))  # Отображаем кадр патрона

                # Переключение кадров
                self.fireball_frame_counter += 1
                if self.fireball_frame_counter >= self.fireball_frame_delay:
                    self.current_fireball_frame = (self.current_fireball_frame + 1) % len(self.animation_list[3])
                    self.fireball_frame_counter = 0

                # Сохраняем обновленные координаты патрона
                self.bullet = (x, y)

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pg.time.get_ticks()
    
    def draw(self, surface, color):
        img = pg.transform.flip(self.image, self.flip , False)

        if self.dead:
            surface.blit(img, (self.rect.x - 190, self.rect.y-85))
        else:
            surface.blit(img, (self.rect.x - 190, self.rect.y-60))
        
        
        