import pygame
from code.menu import Button

pygame.init()

class Inventory:
    def __init__(self, var, x, y, width, height):
        self.var = var
        self.rect = pygame.Rect(x, y, width, height)
        self.slots = [Health(x+5, y, 50, 50), Stealth(x+60, y, 50, 50), Boost(x+115, y, 50, 50)]
        self.active = None
        
    
    def draw(self):
        pygame.draw.rect(self.var.screen, (50, 30, 10), self.rect)
        for item in self.slots:
            item.draw(self.var)
            
    
    def isClicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for item in self.slots:
                if item.isClicked(pos):
                    self.active = item
    
    def use_item(self, event):
        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[pygame.K_e]:
                if self.active:
                    self.active.use(self.var.player)
                    self.active = None

class Health(Button):
    empty = False
    sprites = [pygame.image.load('./images/items/healthempty1.png'), pygame.image.load('./images/items/healthfull1.png')]
    magic = 'health'

    def use(self, player):
        player.health.value += 20
        if player.health.value > 100:
            player.health.value = 100
        self.empty = True
    
    def draw(self, var):
        if self.empty:
            var.screen.blit(self.sprites[0], self.rect[:2])
        else:
            var.screen.blit(self.sprites[1], self.rect[:2])


class Boost(Button):
    empty = False
    sprites = [pygame.image.load('./images/items/boostempty1.png'), pygame.image.load('./images/items/boostfull1.png')]
    magic = 'boost'

    def use(self, player):
        player.moving_speed = 20
        self.empty = True
    
    def draw(self, var):
        if self.empty:
            var.screen.blit(self.sprites[0], self.rect[:2])
        else:
            var.screen.blit(self.sprites[1], self.rect[:2])

class Stealth(Button):
    empty = False
    sprites = [pygame.image.load('./images/items/stealthempty1.png'), pygame.image.load('./images/items/stealthfull1.png')]
    magic = 'stealth'

    def use(self, player):
        print("Entering stealth mode")
        player.stealth = True
        self.empty = True
    
    def draw(self, var):
        if self.empty:
            var.screen.blit(self.sprites[0], self.rect[:2])
        else:
            var.screen.blit(self.sprites[1], self.rect[:2])

    