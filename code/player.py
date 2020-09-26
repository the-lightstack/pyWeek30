import pygame
from random import random#give bullets a bit of randomness
import random
from pygame import Vector2
import math
import pygame

pygame.init()

class Player:
    def __init__(self,x,y,w,h,var):
        self.rect=pygame.Rect(x,y,w,h)
        self.hitbox=pygame.Rect(x,y,w,h)
        self.var=var
        self.health = HealthBar(1000, 10, 100, 20, self.var)
        self.health_counter = 4
        self.moving_left=False
        self.moving_up=False
        self.moving_right=False
        self.moving_down=False

        self.stealth = False
        self.stealth_counter = 100

        self.img=pygame.image.load("./images/player_test.png")
        images_width=32
        self.animation_sprites={"wr":self.get_sprite_sheet([images_width,48],"./images/character_walking_right_sprite_sheet.png"),"wd":self.get_sprite_sheet([images_width,48],"./images/character_walking_down_sprite_sheet.png"),"wl":self.get_sprite_sheet([images_width,48],"./images/character_walking_left_sprite_sheet.png"),"wu":self.get_sprite_sheet([images_width,48],"./images/character_walking_up_sprite_sheet.png"),"sr":self.get_sprite_sheet((images_width,48),"./images/player_idle_poses.png")[3],"sl":self.get_sprite_sheet((images_width,48),"./images/player_idle_poses.png")[2],"su":self.get_sprite_sheet((images_width,48),"./images/player_idle_poses.png")[0],"sd":self.get_sprite_sheet((images_width,48),"./images/player_idle_poses.png")[1]}
        self.walking_animation_duration=3
        #general game attributes
        self.last_moving_direction="su"

        self.moving_speed=10
        self.boost_counter = 15
        self.movement_velocity=pygame.Vector2(0,0)

        
       
        self.available_knives=0
        self.may_throw_knife=True
        self.knives=[]
    #this updates everything and calls all the other functions
    def update_knives_scroll(self,event):
        for i in self.knives:
            i.check_mouse_wheel_scroll(event)

    def check_health(self):
        if self.health.value < 0:
            self.var.game_running = False
            self.var.game_over = True

    def update(self):
        self.check_health()
        self.update_movement_velocity()
        self.update_pos()
        self.shoot()
        self.show()
        for i in self.knives:
            i.update()

        #if self.torch_collected:
            #self.draw_test_light_beam()
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
        
        self.health.draw()
            
     
    def shoot(self):
        
        mouse_pos=Vector2(pygame.mouse.get_pos()[0]+self.var.camera_scrolling[0],pygame.mouse.get_pos()[1]+self.var.camera_scrolling[1])
        playerPos=Vector2(self.rect.x+self.rect.w/2,self.rect.y+self.rect.h/2)
        difference =Vector2(mouse_pos-playerPos)

        #rotation_z=math.atan2(difference.y,difference.x)
       
        self.angle=360-(180 / math.pi) * -math.atan2(difference.y, difference.x)
   
        
        if pygame.mouse.get_pressed()[0] and self.available_knives>0 and self.may_throw_knife:
            angle=math.radians(self.angle)
            bulletVel=Vector2(math.cos(angle),math.sin(angle))
            
            self.knives.append(Knife(self.rect.x+self.rect.w/2,self.rect.y+self.rect.h/2,bulletVel,self.var))
            self.available_knives-=1

    def update_movement_velocity(self):
        self.movement_velocity.x=0
        self.movement_velocity.y=0

        if self.moving_left:
            self.movement_velocity.x-=1
        if self.moving_right:
            self.movement_velocity.x+=1
        if self.moving_up:
            self.movement_velocity.y-=1
        if self.moving_down:
            self.movement_velocity.y+=1
        try:
            self.movement_velocity=self.movement_velocity.normalize()
        except:
            pass
        self.movement_velocity.x=self.movement_velocity.x*self.moving_speed
        self.movement_velocity.y=self.movement_velocity.y*self.moving_speed

        if self.moving_speed != 10:
            self.boost_counter -= 1
            if self.boost_counter < 0:
                self.boost_counter = 10
                self.moving_speed -= 1
                

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
            
            for fountain in self.var.map.fountains:
                if self.rect.colliderect(fountain.rect):
                    collide_list.append(fountain)

            return collide_list
    
    def check_interactable_area(self, event):
        for fountain in self.var.map.fountains:
            if self.rect.colliderect(fountain.interactable_area):
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_z]:
                        fountain.refill()

    

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
        #print("sheet rect w:",sheet_rect.w)
        #print("row")
        for i in range(0,sheet_rect.width,size[0]):#columns
            #print("column")
            #print("i:",i)    
            sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y)) #find sprite you want
            sprite = sheet.subsurface(sheet.get_clip()) #grab the sprite you want
            sprites.append(sprite)
            sprt_rect_x += len_sprt_x
        sprt_rect_y += len_sprt_y
        sprt_rect_x = 0

        #sprites=[pygame.transform.scale(i,(image_size[0],image_size[1])) for i in sprites]
        #print("sprites:",sprites)
        return sprites
    
    def decrease_health(self):
        self.health_counter -= 1
        if self.health_counter < 0:
            self.health.value -= 1
            self.health_counter = 4


class HealthBar():
    def __init__(self, x, y, width, height, var):
        self.rect = pygame.Rect(x, y, width, height)
        self.var = var
        self.value = 100
        self.bar = pygame.image.load('./images/healthbar.png')
    
    def draw(self):
        self.var.screen.blit(self.bar, self.rect[:2])
        pygame.draw.rect(self.var.screen, (30,180,60), (self.rect.x+20, self.rect.y+45, (self.rect.w+60)*self.value//100, self.rect.h-10))


    
   

class Knife:
    def __init__(self,x,y,vel,var):#have to make it so knives die after time or if they hit player or maybe object or out of bounds
        
        self.vel=vel
        self.time_limit=1
        self.w=15
        self.h=30
        self.rect=pygame.Rect(x,y,self.w,self.h)
        self.hitbox_rect=pygame.Rect(self.rect.x-10,self.rect.y-10,self.rect.w+20,self.rect.h+20)
        self.color=(92, 40, 136)
        self.speed=16
        self.max_speed=12
        self.speed_steps=1.5

        self.image_flying=pygame.transform.scale(self.get_sprite_sheet((10,20),"./images/knife_sprite_sheet.png")[0],(self.rect.w,self.rect.h))
        self.image_collectable=pygame.transform.scale(self.get_sprite_sheet((10,20),"./images/knife_sprite_sheet.png")[1],(self.rect.w,self.rect.h))

        self.changed_direction=False
        self.flying=True
        self.var=var
        self.angle=360-self.var.player.angle-90
        
    def show(self):
       #this is temporaryly
        #pygame.draw.rect(self.var.screen,self.color,(self.rect.x-self.var.camera_scrolling[0],self.rect.y-self.var.camera_scrolling[1],self.w,self.w))
        temp_angle=self.angle
        if self.speed<0:
            temp_angle*=2

        if self.flying==True:
            temp_image=pygame.transform.rotate(self.image_flying,temp_angle)
        else:
            temp_image=pygame.transform.rotate(self.image_collectable,temp_angle)
        if self.speed<0:
            temp_image=pygame.transform.flip(temp_image,False,True)
            
        self.var.screen.blit(temp_image,(self.rect.x-self.var.camera_scrolling.x,self.rect.y-self.var.camera_scrolling.y))
    def update_pos(self):
        if self.flying==True:
            self.rect.x+=int(self.vel.x*self.speed)
            self.rect.y+=int(self.vel.y*self.speed)
            #currently checks if bullet is supposed to die
        
        
        #self.vel+=self.vel/200
       
        
    def check_colliding(self):
       for i in self.var.obstacles:
           if i.rect.colliderect(self.rect):
               self.flying=False

    def update(self):
        self.update_pos()
        self.check_colliding()
        self.show()
        self.check_player_collecting()
        #self.check_mouse_wheel_scroll()
        self.hitbox_rect[:2]=self.rect[:2]
    
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
        
        for i in range(0,sheet_rect.width,size[0]):#columns
            #print("column")
             
            sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y)) #find sprite you want
            sprite = sheet.subsurface(sheet.get_clip()) #grab the sprite you want
            sprites.append(sprite)
            sprt_rect_x += len_sprt_x
        sprt_rect_y += len_sprt_y
        sprt_rect_x = 0

        #sprites=[pygame.transform.scale(i,(image_size[0],image_size[1])) for i in sprites]
        #print("sprites:",sprites)
        return sprites

    def check_player_collecting(self):
        if self.flying==False:
            if self.var.player.rect.colliderect(self.rect):
                self.var.player.available_knives+=1
                self.var.player.knives.remove(self)
    def check_mouse_wheel_scroll(self,event):
        '''
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==4:
                if self.speed+self.speed_steps<self.max_speed:
                    self.speed+=self.speed_steps
            elif event.button==5:
                if self.speed-self.speed_steps>self.max_speed*-1:
                    self.speed-=self.speed_steps
        '''
        if event.type==pygame.MOUSEBUTTONDOWN and not self.changed_direction:
            if event.button==1:
                self.speed*=-1
                self.changed_direction=True
        #Picking up knife out of the air
        '''if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                if self.hitbox_rect.colliderect(self.var.player.rect) :
                    self.var.player.available_knives+=1
                    self.var.player.knives.remove(self)'''
        keys=pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE]:
            
            if self.hitbox_rect.colliderect(self.var.player.rect):
                self.var.player.available_knives+=1
                self.var.player.knives.remove(self)
    

        