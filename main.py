import pygame, random
from code.player import Player
from code.enemy import Enemy
from code.obstacle import Obstacle
from code.map import Map
from code.menu import MainMenu

pygame.init()

def main():
    #class for all the variables so you have easy access across multiple files
    class Var:
        def __init__(self):
            self.SCREEN_SIZE=(1200,720)
            self.screen=pygame.display.set_mode(self.SCREEN_SIZE)
            pygame.display.set_caption("Cast A Torch")

            self.game_running=False
            self.exit_game = False
            self.main_menu = True
            self.player=None
            self.clock=pygame.time.Clock()
            self.FPS=30
            
            self.boxes_size=(32,32)
            self.camera_scrolling=pygame.Vector2(100,0)

            #game stuff
            self.frame_counter=0
            
            self.obstacles=[]
            self.map=Map(self)
        
        def update_camera(self):
            self.camera_scrolling.x-=(self.camera_scrolling.x-(self.player.rect.x-self.SCREEN_SIZE[0]/2))/10
            self.camera_scrolling.y-=(self.camera_scrolling.y-(self.player.rect.y-self.SCREEN_SIZE[1]/2))/10

    var=Var()
    var.player=Player(100,100,32,48,var)
    Enemies = [Enemy(var, random.choice(range(200, 1000)), random.choice(range(200, 600))) for _ in range(10)]
    menu = MainMenu(var)

    while True:
        var.clock.tick(var.FPS)
        var.frame_counter+=1

        # if the quit is pressed, game exits
        if var.exit_game:
            pygame.quit()
            quit()

        # for main menu
        if var.main_menu:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    var.game_running=False
                    pygame.quit()

            if pygame.mouse.get_pressed() == (1,0,0):
                pos = pygame.mouse.get_pos()
                for obj in menu.objects:
                    if obj.isClicked(pos):
                        obj.action(var)
                        break

            menu.draw()

        # game's running
        if var.game_running:
            #event loop
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    var.game_running=False
                    pygame.quit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_w:
                        var.player.moving_up=True
                    if event.key==pygame.K_a:
                        var.player.moving_left=True
                    if event.key==pygame.K_s:
                        var.player.moving_down=True
                    if event.key==pygame.K_d:
                        var.player.moving_right=True
                if event.type==pygame.KEYUP:
                    if event.key==pygame.K_w:
                        var.player.moving_up=False
                    if event.key==pygame.K_a:
                        var.player.moving_left=False
                    if event.key==pygame.K_s:
                        var.player.moving_down=False
                    if event.key==pygame.K_d:
                        var.player.moving_right=False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        var.game_running = False
                        var.main_menu = True

            var.screen.fill((0,0,0))
            var.map.update()
            var.player.update()
            for enemy in Enemies:
                enemy.update()
            
            for i in var.obstacles:
                i.update()

        pygame.display.flip()
        var.update_camera()



if __name__=="__main__":
    main()