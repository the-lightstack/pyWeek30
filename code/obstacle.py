import pygame
pygame.init()
import random
#so we can add like walls,bushes,rivers or houses
class Obstacle:#x and y will be multiplicated by 32 are like row and column
    def __init__(self,x,y,var,img_path,has_animation,anim_dur_min_max,width=32,height=32):#animation is gonna be true or false
        self.rect=pygame.Rect(x*var.boxes_size[0],y*var.boxes_size[1],width,height)
        self.var=var
        self.img_path=img_path
        self.has_animation=has_animation
        self.anim_dur_min_max=anim_dur_min_max#animation duration min and max can be same, else random int between both
        
        self.animation_duration=random.randint(self.anim_dur_min_max[0],self.anim_dur_min_max[1])
        
        self.sprites=[]
        if self.has_animation:
            self.sprites=self.get_sprite_sheet((32,32),self.img_path)
        else:
            self.sprites.append(pygame.image.load(self.img_path))


    def update(self):
        self.show()

    def show(self):
        if self.has_animation:
            current_image=self.sprites[(((self.var.frame_counter)//self.animation_duration)-1)%len(self.sprites)]
            self.var.screen.blit(current_image,((self.rect.x)-self.var.camera_scrolling.x,(self.rect.y)-self.var.camera_scrolling.y))
        else:
            self.var.screen.blit(self.sprites[0],((self.rect.x)-self.var.camera_scrolling.x,(self.rect.y)-self.var.camera_scrolling.y))
            
       
    
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
