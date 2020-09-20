import pygame
from code.player import Player
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
    var=Var()
    var.player=Player(100,100,32,48,var)


    while var.game_running:
        var.clock.tick(var.FPS)
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

        var.screen.fill((0,0,0))
        var.player.update()



        pygame.display.flip()






if __name__=="__main__":
    main()