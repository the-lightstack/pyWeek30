import pygame
pygame.init()
from code.obstacle import Obstacle
class Map:
    def __init__(self,var):
        self.current_map_path="./maps/map1.txt"
        self.current_map=None
        self.load_map()#Current map gets assigned here
        self.var=var
        self.indices={  0:(pygame.image.load("./images/floor_sprite_test.png"),False,False,None),#img_path,Collision(obstacle),has_animation,anim_duration_min_max
                        1:("./images/temp_wall.png",True,False,[1,10]),
                        2:("./images/bush_animation_sprites.png",True,True,(5,15)),
                        3:(self.get_sprite_sheet((32,32),"./images/beach_water_sprites.png")[0],False,False,None),#beach_left_one
                        4:(self.get_sprite_sheet((32,32),"./images/beach_water_sprites.png")[1],False,False,None),#beach_left_two
                        5:(self.get_sprite_sheet((32,32),"./images/beach_water_sprites.png")[2],False,False,None),#beach_corner_down_right
                        6:(self.get_sprite_sheet((32,32),"./images/beach_water_sprites.png")[3],False,False,None),#beach_corner_up_left
                        7:(self.get_sprite_sheet((32,32),"./images/beach_water_sprites.png")[4],False,False,None),#full_beach
                        8:(self.get_sprite_sheet((32,32),"./images/beach_water_sprites.png")[5],False,False,None),#tiny_beach_part_up_left
                        9:(self.get_sprite_sheet((32,32),"./images/beach_water_sprites.png")[6],False,False,None),#full water tile
                        10:(self.get_sprite_sheet((32,32),"./images/beach_water_sprites.png")[7],False,False,None),#halfwater, half sand
                        11:(self.get_sprite_sheet((32,32),"./images/beach_water_sprites.png")[8],False,False,None),#swimming, platform
                        }

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

    def get_sprite_sheet(self,size,file,pos=(0,0)):
        import pygame#file is path_to_file
        #Initial Values
        len_sprt_x,len_sprt_y = size #sprite size
        
        sprt_rect_x,sprt_rect_y = pos #where to find first sprite on sheet
        sheet = pygame.image.load(file).convert_alpha() #Load the sheet
        sheet_rect = sheet.get_rect()
        
        sprites = []
        
        image_size=(32,32)
    
        #print("row")
        for i in range(0,sheet_rect.width,size[0]):#columns
            #print("column")    
            sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y)) #find sprite you want
            sprite = sheet.subsurface(sheet.get_clip()) #grab the sprite you want
            sprites.append(sprite)
            sprt_rect_x += len_sprt_x
        sprt_rect_y += len_sprt_y
        sprt_rect_x = 0

        sprites=[pygame.transform.scale(i,(image_size[0],image_size[1])) for i in sprites]
        return sprites