import pygame, random
from code.player import Player
from code.enemy import Enemy
from code.obstacle import Obstacle
from code.map import Map
from code.menu import MainMenu
from code.enemy import Enemy
from code.monk_with_torch import Torch_Monk 
from code.inventory import Inventory

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
            self.game_over = False
            self.player=None
            self.clock=pygame.time.Clock()
            self.FPS=30
            
            self.boxes_size=(32,32)
            self.camera_scrolling=pygame.Vector2(100,0)

            #game stuff
            self.frame_counter=0
            self.level_counter=0
            self.obstacles=[]
            self.map=Map(self)

            self.dead_monk=Torch_Monk(9,14,self)
            self.screen_night_overlay=pygame.image.load("./images/screen_dark_overlay.png").convert_alpha()
            self.screen_night_overlay=pygame.transform.scale(self.screen_night_overlay,self.SCREEN_SIZE)
            self.Enemies = [Enemy(self, random.choice(range(200, 1500)), random.choice(range(200, 1500))) for _ in range(100)]

            self.goal_img=pygame.image.load("./images/end_goal.png")
            self.goal_rect=pygame.Rect(1390,1470,32,32)
            
        def update_camera(self):
            self.camera_scrolling.x-=(self.camera_scrolling.x-(self.player.rect.x-self.SCREEN_SIZE[0]/2))/10
            self.camera_scrolling.y-=(self.camera_scrolling.y-(self.player.rect.y-self.SCREEN_SIZE[1]/2))/10

        def set_player_move_bools(self,event):
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_w:
                    self.player.moving_up=True
                    self.player.last_moving_direction="su"
                if event.key==pygame.K_a:
                    self.player.moving_left=True
                    self.player.last_moving_direction="sl"
                if event.key==pygame.K_s:
                    self.player.moving_down=True
                    self.player.last_moving_direction="sd"
                if event.key==pygame.K_d:
                    self.player.moving_right=True
                    self.player.last_moving_direction="sr"
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_w:
                    self.player.moving_up=False
                if event.key==pygame.K_a:
                    self.player.moving_left=False
                if event.key==pygame.K_s:
                    self.player.moving_down=False
                if event.key==pygame.K_d:
                    self.player.moving_right=False


    var=Var()
    var.player=Player(100,400,32,48,var)
    #setting up camera on player location
    var.camera_scrolling.x=-400
    var.camera_scrolling.y=0
    
    menu = MainMenu(var)
    var.inventory = Inventory(var, 20, 600, 230, 110)

    while True:
        var.clock.tick(var.FPS)
        

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
            #print("fps:",var.clock.get_fps())
           
            var.frame_counter+=1
            #event loop
            var.screen.fill((0,100,200))
            var.map.update()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    var.game_running=False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        var.game_running = False
                        var.main_menu = True
                var.set_player_move_bools(event)
                var.player.update_knives_scroll(event)
                var.player.check_interactable_area(event)
                var.inventory.isClicked(event)
                var.inventory.use_item(event)

            for i in var.obstacles:
                i.update()
            var.dead_monk.update()
            #blitting goal
            var.screen.blit(var.goal_img,(var.goal_rect.x-var.camera_scrolling.x,var.goal_rect.y-var.camera_scrolling.y))
            #checking for goal player collision
            if var.player.rect.colliderect(var.goal_rect):
                var.main_menu=True
                var.game_running=False
                var.player.rect.x+=100
            var.player.update()
            enemy_len = len(var.Enemies)
            for enemy in var.Enemies:
                enemy.update()
            
            
            var.inventory.draw()
        
        if var.game_over:
            print("Game over")
            var.game_over = False
            main()


        pygame.display.flip()
        var.update_camera()



if __name__=="__main__":
    main()