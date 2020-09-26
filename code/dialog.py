import pygame, time

class Dialog():
    def __init__(self, x, y , w, h, *dialog):
        self.rect = pygame.Rect(x, y, w, h)
        self.dialog = dialog
        self.font = pygame.font.SysFont('Times New Roman', 20)
    
    def draw(self, var):
        pygame.draw.rect(var.screen, (150, 10, 130), self.rect)
        for d in self.dialog:
            text = self.font.render(d, True, (255,255,255))
            var.screen.blit(text, self.rect[:2])

            