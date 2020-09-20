import pygame
pygame.init()

class Player:
    def __init__(self,x,y,w,h,var):
        self.rect=pygame.Rect(x,y,w,h)
        self.hitbox=pygame.Rect(x,y,w,h)
        self.var=var
        
        self.moving_left=False
        self.moving_up=False
        self.moving_right=False
        self.moving_down=False

        self.img=pygame.image.load("./images/player_test.png")

        #general game attributes
        self.moving_speed=6
        self.movement_velocity=pygame.Vector2(0,0)

    #this updates everything and calls all the other functions
    def update(self):
        self.update_movement_velocity()
        self.update_pos()
        self.show()
    def show(self):
        self.var.screen.blit(self.img,(self.rect.x,self.rect.y))

    def update_movement_velocity(self):
        self.movement_velocity.x=0
        self.movement_velocity.y=0

        if self.moving_left:
            self.movement_velocity.x-=1*self.moving_speed
        if self.moving_right:
            self.movement_velocity.x+=1*self.moving_speed
        if self.moving_up:
            self.movement_velocity.y-=1*self.moving_speed
        if self.moving_down:
            self.movement_velocity.y+=1*self.moving_speed

    def update_pos(self):
        self.rect.x+=self.movement_velocity.x
        self.rect.y+=self.movement_velocity.y
    
