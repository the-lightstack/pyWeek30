import pygame
pygame.init()

class Torch_Monk:
    def __init__(self,x,y,var):
        self.rect=pygame.Rect(x*var.boxes_size[0],y*var.boxes_size[1],64,32)
        self.image_with_torch=pygame.image.load("./images/dead_monk_torch.png").convert_alpha()
        self.image_without_torch=pygame.image.load("./images/dead_monk_no_torch.png")
        
        self.hitbox=pygame.Rect(self.rect.x+10,self.rect.y+10,self.rect.w-20,self.rect.h-20)
        self.var=var

        self.collected=False
    
    def update(self):
        
        self.show()
        self.check_collected()
    def show(self):
        if not self.collected:
            self.var.screen.blit(self.image_with_torch,(self.rect.x-self.var.camera_scrolling.x,self.rect.y-self.var.camera_scrolling.y))
        else:
            self.var.screen.blit(self.image_without_torch,(self.rect.x-self.var.camera_scrolling.x,self.rect.y-self.var.camera_scrolling.y))
            
    def check_collected(self):
        if self.hitbox.colliderect(self.var.player) and self.collected==False:
            self.collected=True
            self.var.player.available_knives+=1
            
