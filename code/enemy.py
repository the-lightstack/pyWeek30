import pygame, math

class Enemy(object):
    def __init__(self, var, x, y, width=32, height=48):
        self.rect = pygame.Rect(x,y,width,height)
        self.range = 1050
        self.var = var
        self.img = pygame.image.load('./images/enemy.png')
    
    def draw(self):
        self.var.screen.blit(self.img, self.rect[:2])
    
    def update(self, player):
        x1, y1 = self.rect[:2]
        x2, y2 = player.rect[:-2]
        if math.sqrt((x1-x2)**2 + (y1-y2)**2) < self.range:
            if player.rect.x > self.rect.x and self.rect.x < self.var.SCREEN_SIZE[0]:
                self.rect.x += 1
            elif player.rect.x < self.rect.x and self.rect.x > 0:
                self.rect.x -= 1
            
            if player.rect.y > self.rect.y and self.rect.y < self.var.SCREEN_SIZE[1]:
                self.rect.y += 1
            elif player.rect.y < self.rect.y and self.rect.y > 0:
                self.rect.y -= 1
        
        self.draw()