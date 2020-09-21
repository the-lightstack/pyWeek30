import pygame
pygame.init()
from code.obstacle import Obstacle
class Map:
    def __init__(self,var):
        self.current_map_path="./maps/map1.txt"
        self.current_map=None
        self.load_map()#Current map gets assigned here
        self.var=var
        self.indices={0:(pygame.image.load("./images/floor_sprite_test.png"),False,False,None),1:("./images/temp_wall.png",True,False,[1,10]),2:("./images/bush_animation_sprites.png",True,True,(5,15))}#img_path,Collision(obstacle),has_animation,anim_duration_min_max
        #when it aint a obstacle the image should be 
        self.init_obstacles()
    def update(self):
        self.show()
    def load_map(self):
        with open(self.current_map_path,"r") as file:
            self.current_map=file.read()
        self.current_map=eval(self.current_map)
        
    
    def show(self):
        
        y=0
        for layer in self.current_map:
            x=0
            for number in layer:                                                  # all the obstacles should actually only be loaded once, but all the drawing stuff is supposed to 
    
                
                if number==2:#draw grass under bush
                    self.var.screen.blit(self.indices[0][0],((x*self.var.boxes_size[0])-self.var.camera_scrolling.x,(y*self.var.boxes_size[1])-self.var.camera_scrolling.y))
                    
                
                if self.indices[number][1]==False:#Its not interacting with its surounding
                    self.var.screen.blit(self.indices[number][0],((x*self.var.boxes_size[0])-self.var.camera_scrolling.x,(y*self.var.boxes_size[1])-self.var.camera_scrolling.y))
                x+=1
            
            y+=1
    def init_obstacles(self):
        y=0
        for layer in self.current_map:
            x=0
            for number in layer:                                                  # all the obstacles should actually only be loaded once, but all the drawing stuff is supposed to 
    
                
                
                if self.indices[number][1]==True:#means it is an obstacle
                    self.var.obstacles.append(Obstacle(x,y,self.var,self.indices[number][0],self.indices[number][2],self.indices[number][3]))
                
                x+=1
            
            y+=1