import pygame
from random import randint

def rotate_flip(img):
    img = pygame.transform.rotozoom(img,0,2)
    img = pygame.transform.flip(img,True,False)
    return img

class Runner(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        frame1 = pygame.image.load("visuals\\mario run\\mariorun1.png").convert_alpha()
        frame1 = rotate_flip(frame1)

        frame2 = pygame.image.load("visuals\\mario run\\mariorun2.png").convert_alpha()
        frame2 = rotate_flip(frame2)

        frame3 = pygame.image.load("visuals\\mario run\\mariorun3.png").convert_alpha()
        frame3 = rotate_flip(frame3)

        self.frames = [frame1,frame2,frame3,frame2]
        self.frame_index = 0

        self.runner_jump = pygame.image.load("visuals\\mario run\\mariojump.png").convert_alpha()
        self.runner_jump = rotate_flip(self.runner_jump)

        self.runner_crouch = pygame.image.load("visuals\\mario run\\mariocrouch.png").convert_alpha()
        self.runner_crouch = rotate_flip(self.runner_crouch)
        self.crouch = False

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom = (208,330))

        self.gravity = 0
        self.scrolling = True

    def runner_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.crouch = True

        elif keys[pygame.K_SPACE] and self.rect.bottom >= 330:
            self.gravity = -15
        else:
            self.crouch = False
            
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.bottom >= 330:
            self.rect.bottom = 330

    def curr_frame(self):
        if self.rect.bottom < 330:
            self.image = self.runner_jump
            self.scrolling = True

        elif self.crouch:
            self.image = self.runner_crouch
            self.rect = self.image.get_rect(midbottom = (200,330))
            self.scrolling = False

        else:
            self.frame_index += 0.25
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            
            self.image = self.frames[int(self.frame_index)]
            self.rect = self.image.get_rect(midbottom = (208,330))
            self.scrolling = True

    def update(self):
        self.runner_input()
        self.apply_gravity()
        self.curr_frame()
        
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        shell_frame1 = pygame.image.load("visuals\\obstacles\\shell1.png")
        shell_frame1 = pygame.transform.scale2x(shell_frame1)

        shell_frame2= pygame.image.load("visuals\\obstacles\\shell2.png")
        shell_frame2 = pygame.transform.scale2x(shell_frame2)

        shell_frame3 = pygame.image.load("visuals\\obstacles\\shell3.png")
        shell_frame3 = pygame.transform.scale2x(shell_frame3)

        shell_frame4 = pygame.image.load("visuals\\obstacles\\shell4.png")
        shell_frame4 = pygame.transform.scale2x(shell_frame4)

        bullet_frame = pygame.image.load("visuals\\obstacles\\bullet.png")
        bullet_frame = pygame.transform.scale2x(bullet_frame)

        if type == "shell":
            self.frames = [shell_frame1,shell_frame2,shell_frame3,shell_frame4]
            y_pos = 330

        if type == "bullet":
            self.frames = [bullet_frame]
            y_pos = randint(250,290)
        
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom = (randint(1000,1200),y_pos))

    def curr_frame(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self):
        self.curr_frame()
        self.rect.x -= 6
        if self.rect.x < -100:
            self.kill()