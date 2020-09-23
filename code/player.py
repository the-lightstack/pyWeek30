import pygame
pygame.init()

class Player:
    def __init__(self,x,y,w,h,var):
        self.rect=pygame.Rect(x,y,w,h)
        self.hitbox=pygame.Rect(x,y,w,h)
        self.var=var
        self.health = 100
        self.moving_left=False
        self.moving_up=False
        self.moving_right=False
        self.moving_down=False

        self.img=pygame.image.load("./images/player_test.png")

        #general game attributes
        self.moving_speed=7
        self.movement_velocity=pygame.Vector2(0,0)

    #this updates everything and calls all the other functions
    def update(self):
        self.update_movement_velocity()
        self.update_pos()
        self.show()
    def show(self):
        self.var.screen.blit(self.img,(self.rect.x-self.var.camera_scrolling.x,self.rect.y-self.var.camera_scrolling.y))

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
       

        collisions=self.check_obstacle_collision()

        for i in collisions:
            if self.movement_velocity.x>0:#moving right
                self.rect.right=i.rect.left
            if self.movement_velocity.x<0:#moving left
                self.rect.left=i.rect.right
        
        self.rect.y+=self.movement_velocity.y
        collisions=self.check_obstacle_collision()
        for i in collisions:
           
            if self.movement_velocity.y>0:
                self.rect.bottom=i.rect.top
            if self.movement_velocity.y<0:
                self.rect.top=i.rect.bottom

    def check_obstacle_collision(self):
            collide_list=[]
            for obs in self.var.obstacles:
                if self.rect.colliderect(obs.rect):
                    collide_list.append(obs)
                    
            return collide_list
