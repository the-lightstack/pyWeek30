import pygame, math, random

class Enemy(object):
    def __init__(self, var, x, y, width=32, height=48):
        self.rect = pygame.Rect(x,y,width,height)
        self.inipos = ('x' if random.choice([0,1]) else 'y', *self.rect[:2])

        self.flying_imgs=[pygame.image.load("./images/bug.png"),pygame.image.load("./images/bug1.png"),pygame.image.load("./images/bug2.png"),pygame.image.load("./images/bug3.png"),pygame.image.load("./images/bug4.png")]
        self.attacking_imgs=[pygame.image.load("./images/bug.png"),pygame.image.load("./images/bug-attack.png"),pygame.image.load("./images/bug-attack1.png"),pygame.image.load("./images/bug-attack2.png"),pygame.image.load("./images/bug-attack3.png")]
        self.flying_animation_duration=random.randint(2,5)
        self.attacking=False
        self.dead=False
        self.animation_start_frame=1000000000000000000000000
        self.started_animtion=False
        self.death_animation_duration=20
        self.particles=[]

        if self.inipos[0] == 'x':
            self.range = (x-100, x+100, 150) # horizontal , vertical and radii range
        else:
            self.range = (y-100, y+100, 150)

        self.dir = 1
        self.var = var
        
        self.img = pygame.image.load('./images/boss.png')
    
    def draw(self):
        #self.var.screen.blit(self.img, (self.rect.x-self.var.camera_scrolling.x,self.rect.y-self.var.camera_scrolling.y))
        if not self.attacking:
            current_image=self.flying_imgs[(((self.var.frame_counter)//self.flying_animation_duration))%len(self.flying_imgs)]
        else:
            current_image=self.attacking_imgs[(((self.var.frame_counter)//self.flying_animation_duration))%len(self.flying_imgs)]
        self.var.screen.blit(current_image,(self.rect.x-self.var.camera_scrolling.x,self.rect.y-self.var.camera_scrolling.y))
    
    def update(self):
        if self.dead==True:
           self.death_animation()
        if self.check_collision():
            self.draw()
            return True
        if self.dead==False:
            x1, y1 = self.rect[:2]
            x2, y2 = self.var.player.rect[:-2]
            if math.sqrt((x1-x2)**2 + (y1-y2)**2) < self.range[2]:
                # print('Following player')
                if x2 > x1 and x1 < self.var.SCREEN_SIZE[0]:
                    self.rect.x += 1
                elif x2 < x1 and x1 > 0:
                    self.rect.x -= 1
                
                if y2 > y1 and y1 < self.var.SCREEN_SIZE[1]:
                    self.rect.y += 1
                elif y2 < y1 and y1 > 0:
                    self.rect.y -= 1
            
            elif self.inipos[0] == 'x' and y1 == self.inipos[2]:
                # print('Moving left and right')
                if x1 == self.range[0]:
                    self.dir = -1
                elif x1 == self.range[1]:
                    self.dir = 1
                self.rect.x -= self.dir

            elif self.inipos[0] == 'y' and x1 == self.inipos[1]:
                # print('Moving up and down')
                if y1 == self.range[0]:
                    self.dir = -1
                elif y1 == self.range[1]:
                    self.dir = 1
                self.rect.y -= self.dir

            else:
                # print('Returning back to initial position')
                if x1 > self.inipos[1]:
                    self.rect.x -= 1
                elif x1 <  self.inipos[1]:
                    self.rect.x += 1

                if y1 > self.inipos[2]:
                    self.rect.y -= 1
                elif y1 < self.inipos[2]:
                    self.rect.y += 1

            self.draw()
        self.check_self_dead()

    def check_collision(self):
        if self.rect.colliderect(self.var.player.rect):
            if self.var.player.stealth:
                if self.var.player.stealth_counter < 0:
                    self.var.player.stealth_counter = 100
                    self.var.player.stealth = False
                    print("Stealth mode finished.")
                else:
                    self.var.player.stealth_counter -= 1
                return False
            if self.var.player.moving_speed == 10:
                self.attacking = True
                self.var.player.decrease_health()
            return True
        else:
            self.attacking = False
            

    def death_animation(self):
        print("frame-couner:",self.var.frame_counter)
        if self.dead==True and self.started_animtion==False:#This should trigger only on the first time
            self.animation_start_frame=self.var.frame_counter
            self.init_death_particles()
            self.started_animtion=True
        else:   
            
            print("diff",self.var.frame_counter-self.animation_start_frame)
            print("max:",self.death_animation_duration)
            if self.var.frame_counter-self.animation_start_frame<self.death_animation_duration:#not run out of time
                for i in self.particles:
                    i.update()
                #self.animation_start_frame=self.var.frame_counter
            else:
                self.particles=[]
            
                self.var.Enemies.remove(self)
                
    def check_self_dead(self):
        for i in self.var.player.knives:
            if self.rect.colliderect(i.rect):
                #self.var.Enemies.remove(self)
                self.dead=True
    def init_death_particles(self):
        particle_amount=40
        
        for _ in range(particle_amount):
            self.particles.append(Particle(self.rect.x,self.rect.y,self.var))

class Particle:
    def __init__(self,x,y,var):
        
        self.pos=pygame.Vector2(x,y)
        self.var=var
        self.velocity=pygame.Vector2(random.random()*6-3,random.random()*6-3)
        self.w=random.randint(2,6)
        #color one (191,31,55),(236,81,45)
        self.color=(random.randint(190,240),random.randint(30,80),random.randint(45,55))

    def update(self):
        self.update_pos()
        self.show()
    def update_pos(self):
        self.pos+=self.velocity
    def show(self):
        pygame.draw.rect(self.var.screen,self.color,(self.pos.x-self.var.camera_scrolling.x,self.pos.y-self.var.camera_scrolling.y,self.w,self.w))