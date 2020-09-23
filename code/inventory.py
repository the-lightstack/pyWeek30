import pygame
from code.menu import Button

pygame.init()

class Inventory:
    def __init__(self, var, x, y, width, height):
        self.var = var
        self.rect = pygame.Rect(x, y, width, height)
        self.slots = ['health', 'stealth', 'boost']
        self.active = None
        self.items = {
            'health' : {
                'button': Button(x+5, y, 50, 50),
                'empty': False,
                'sprites': [pygame.image.load('./images/items/healthempty1.png'), pygame.image.load('./images/items/healthfull1.png')]
            },
            'stealth' : {
                'button': Button(x+60, y, 50, 50),
                'empty': False,
                'sprites': [pygame.image.load('./images/items/stealthempty1.png'), pygame.image.load('./images/items/stealthfull1.png')]
            },
            'boost' : {
                'button': Button(x+115, y, 50, 50),
                'empty': False,
                'sprites': [pygame.image.load('./images/items/boostempty1.png'), pygame.image.load('./images/items/boostfull1.png')]
            },
        }
    
    def draw(self):
        pygame.draw.rect(self.var.screen, (50, 30, 10), self.rect)
        for item in self.slots:
            if self.items[item].get('empty'):
                self.var.screen.blit(self.items[item].get('sprites')[0], self.items[item].get('button').rect[:2])
            else:
                self.var.screen.blit(self.items[item].get('sprites')[1], self.items[item].get('button').rect[:2])
    
    def isClicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for item in self.slots:
                if self.items[item].get('button').isClicked(pos):
                    print(f'{item} is clicked.')
                    self.active = item
    
    def use_item(self, event):
        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[pygame.K_e]:
                if self.active:
                    print(f'{self.active} is used')
                    self.items.get(self.active)['empty'] = True
                    self.active = None
    