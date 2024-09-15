# https://github.com/russs123/pygame_tutorials/blob/main/Button/button.py

import pygame
import time

# button class
class Button:
    #position is a tuple (x, y), scale is a tuple (width, height)

   
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()
        #print(pos)

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                #print("CLICKED")
                #time.sleep(0.5)
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action




