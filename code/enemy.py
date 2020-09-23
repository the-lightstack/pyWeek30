import pygame, math, random

class Enemy(object):
    def __init__(self, var, x, y, width=32, height=48):
        self.rect = pygame.Rect(x,y,width,height)
        self.inipos = ('x' if random.choice([0,1]) else 'y', *self.rect[:2])
        if self.inipos[0] == 'x':
            self.range = (x-100, x+100, 150) # horizontal , vertical and radii range
        else:
            self.range = (y-100, y+100, 150)
        self.dir = 1
        self.var = var
        self.player = var.player
        self.img = pygame.image.load('./images/boss.png')
    
    def draw(self):
        self.var.screen.blit(self.img, (self.rect.x-self.var.camera_scrolling.x,self.rect.y-self.var.camera_scrolling.y))
    
    def update(self):
        if self.check_collision():
            self.draw()
            return True
        x1, y1 = self.rect[:2]
        x2, y2 = self.player.rect[:-2]
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
    
    def check_collision(self):
        if self.rect.colliderect(self.player.rect):
            return True