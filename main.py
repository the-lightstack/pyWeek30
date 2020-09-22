import pygame
from code.player import Player
from code.obstacle import Obstacle
from code.map import Map
from code.enemy import Enemy
from code.monk_with_torch import Torch_Monk 
pygame.init()


def main():
    #class for all the variables so you have easy access across multiple files
    class Var:
        def __init__(self):
            self.SCREEN_SIZE=(1200,720)
            self.screen=pygame.display.set_mode(self.SCREEN_SIZE)
            pygame.display.set_caption("Cast A Torch")

            self.game_running=True
            self.player=None
            self.clock=pygame.time.Clock()
            self.FPS=30
            
            self.boxes_size=(32,32)
            self.camera_scrolling=pygame.Vector2(100,0)

            #game stuff
            self.frame_counter=0
            
            self.obstacles=[]
            self.map=Map(self)

            self.dead_monk=Torch_Monk(9,14,self)
            self.screen_night_overlay=pygame.image.load("./images/screen_dark_overlay.png").convert_alpha()
            self.screen_night_overlay=pygame.transform.scale(self.screen_night_overlay,self.SCREEN_SIZE)
        def update_camera(self):
            self.camera_scrolling.x-=(self.camera_scrolling.x-(self.player.rect.x-self.SCREEN_SIZE[0]/2))/10
            self.camera_scrolling.y-=(self.camera_scrolling.y-(self.player.rect.y-self.SCREEN_SIZE[1]/2))/10

    var=Var()
    var.player=Player(100,400,32,48,var)
    #setting up camera on player location
    var.camera_scrolling.x=-400
    var.camera_scrolling.y=0
    #test enemy
    en=Enemy(var,100,100)

    while var.game_running:
        var.clock.tick(var.FPS)
        var.frame_counter+=1
        #event loop
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                var.game_running=False
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_w:
                    var.player.moving_up=True
                    var.player.last_moving_direction="su"
                if event.key==pygame.K_a:
                    var.player.moving_left=True
                    var.player.last_moving_direction="sl"
                if event.key==pygame.K_s:
                    var.player.moving_down=True
                    var.player.last_moving_direction="sd"
                if event.key==pygame.K_d:
                    var.player.moving_right=True
                    var.player.last_moving_direction="sr"
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_w:
                    var.player.moving_up=False
                if event.key==pygame.K_a:
                    var.player.moving_left=False
                if event.key==pygame.K_s:
                    var.player.moving_down=False
                if event.key==pygame.K_d:
                    var.player.moving_right=False

        var.screen.fill((0,0,0))
        var.map.update()
        for i in var.obstacles:
            i.update()
        var.dead_monk.update()
        var.player.update()
        
        
        #will later be for all enemys
        en.update()
        

        var.screen.blit(var.screen_night_overlay,(0,0))
        pygame.display.flip()
        var.update_camera()





if __name__=="__main__":
    main()