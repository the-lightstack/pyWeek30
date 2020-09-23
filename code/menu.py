import pygame, time

class Button:
    def __init__(self, x,y, width, height):
        self.rect = pygame.Rect(x,y, width, height)
    
    def isClicked(self, pos):
        x, y , w, h= self.rect
        print(pos)
        if x <= pos[0] and y <= pos[1] and x+w >= pos[0] and y+h >= pos[1]:
            print("clicked")
            return True
        return False
    
    def draw(self, var, opacity=0):
        pygame.draw.rect(var.screen, (abs(215-opacity),abs(175-opacity),abs(175-opacity)), self.rect)
    
    def action(self, var):
        pass

class Play(Button):
    def action(self, var):
        var.game_running = True
        var.main_menu = False
        for opacity in range(0, 255, 5):
            old_clip=pygame.display.get_surface().get_clip()
            self.draw(var, opacity)
            pygame.display.flip()

class Quit(Button):
    def action(self, var):
        var.exit_game = True
        for opacity in range(0, 255, 5):
            old_clip=pygame.display.get_surface().get_clip()
            self.draw(var, opacity)
            pygame.display.flip()

class Options(Button):
    def action(self, var):
        for opacity in range(0, 255, 5):
            old_clip=pygame.display.get_surface().get_clip()
            self.draw(var, opacity)
            pygame.display.flip()

# class Title(Button):
#     def action(self, var):
#         for opacity in range(0, 255, 5):
#             old_clip=pygame.display.get_surface().get_clip()
#             self.draw(var, opacity)
#             pygame.display.flip()

class MainMenu:
    def __init__(self, var):
        self.var = var
        self.img = pygame.image.load('./images/menu2.png')
        self.objects = []
        self.initialize()
    
    def initialize(self):
        self.objects.append(Play(465, 395, 260, 65))
        self.objects.append(Options(465, 490, 260, 65))
        self.objects.append(Quit(465,585, 260,65))
    
    def draw(self):
        self.var.screen.blit(self.img, (0,0,*self.var.SCREEN_SIZE))