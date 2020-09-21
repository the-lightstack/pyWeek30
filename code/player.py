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
        images_width=32
        self.animation_sprites={"wr":self.get_sprite_sheet([images_width,48],"./images/character_walking_right_sprite_sheet.png"),"wd":self.get_sprite_sheet([images_width,48],"./images/character_walking_down_sprite_sheet.png"),"wl":self.get_sprite_sheet([images_width,48],"./images/character_walking_left_sprite_sheet.png"),"wu":self.get_sprite_sheet([images_width,48],"./images/character_walking_up_sprite_sheet.png"),"sr":self.get_sprite_sheet((images_width,48),"./images/player_idle_poses.png")[3],"sl":self.get_sprite_sheet((images_width,48),"./images/player_idle_poses.png")[2],"su":self.get_sprite_sheet((images_width,48),"./images/player_idle_poses.png")[0],"sd":self.get_sprite_sheet((images_width,48),"./images/player_idle_poses.png")[1]}
        self.walking_animation_duration=3
        #general game attributes
        self.last_moving_direction="su"

        self.moving_speed=6
        self.movement_velocity=pygame.Vector2(0,0)

        self.torch_collected=False
        self.light_beam=None
    #this updates everything and calls all the other functions
    #def draw_test_light_beam(self):
        #pygame.draw.aalines(self.screen,)
    def update(self):
        self.update_movement_velocity()
        self.update_pos()
        self.show()
    def show(self):
        #self.var.screen.blit(self.img,(self.rect.x-self.var.camera_scrolling.x,self.rect.y-self.var.camera_scrolling.y))
        if self.movement_velocity.x==0 and self.movement_velocity.y==0:
            self.var.screen.blit(self.animation_sprites[self.last_moving_direction],(self.rect.x-self.var.camera_scrolling.x,self.rect.y-self.var.camera_scrolling.y))
        else:#this part is temporary 
            #self.var.screen.blit(self.img,(self.rect.x-self.var.camera_scrolling.x,self.rect.y-self.var.camera_scrolling.y))
            if self.movement_velocity.y<0 and self.movement_velocity.x>=0:
                #up image
                current_image=self.animation_sprites["wu"][(((self.var.frame_counter)//self.walking_animation_duration))%len(self.animation_sprites["wu"])]
            elif self.movement_velocity.x>0 and self.movement_velocity.y>=0:
                #right image
                current_image=self.animation_sprites["wr"][(((self.var.frame_counter)//self.walking_animation_duration))%len(self.animation_sprites["wr"])]
            elif self.movement_velocity.y>0 and self.movement_velocity.x<=0:
                #down image
                current_image=self.animation_sprites["wd"][(((self.var.frame_counter)//self.walking_animation_duration)-1)%len(self.animation_sprites["wd"])]
            elif self.movement_velocity.x<0 and self.movement_velocity.y<=0:
                #left image
                current_image=self.animation_sprites["wl"][(((self.var.frame_counter)//self.walking_animation_duration)-1)%len(self.animation_sprites["wl"])]
            self.var.screen.blit(current_image,(self.rect.x-self.var.camera_scrolling.x,self.rect.y-self.var.camera_scrolling.y))
            
                


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


    def get_sprite_sheet(self,size,file,pos=(0,0)):
        import pygame#file is path_to_file
        #Initial Values
        pos=(0,0)
        len_sprt_x,len_sprt_y = size #sprite size
        
        sprt_rect_x,sprt_rect_y = pos #where to find first sprite on sheet
        sheet = pygame.image.load(file).convert_alpha() #Load the sheet
        sheet_rect = sheet.get_rect()
        
        sprites = []
        
        image_size=size
        print("sheet rect w:",sheet_rect.w)
        #print("row")
        for i in range(0,sheet_rect.width,size[0]):#columns
            #print("column")
            print("i:",i)    
            sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y)) #find sprite you want
            sprite = sheet.subsurface(sheet.get_clip()) #grab the sprite you want
            sprites.append(sprite)
            sprt_rect_x += len_sprt_x
        sprt_rect_y += len_sprt_y
        sprt_rect_x = 0

        #sprites=[pygame.transform.scale(i,(image_size[0],image_size[1])) for i in sprites]
        #print("sprites:",sprites)
        return sprites
