# pretty crappy effects
# should be redone

import pygame

class Explosion:
    def __init__(self, x, y, images = list(), big = False ):

        self.images = list()
        for image in images:
            if(not big):
                img = pygame.transform.scale(image,(50,50))
                self.images.append(img)
            else:
                img = pygame.transform.scale(image,(150,150))
                self.images.append(img)

        self.lifetime = 30
        self.x = x
        self.y = y
        self.active = True
        self.ticks = len(self.images)-1
        self.ticker = 0
        self.cimg = 0

    def draw(self, screen):
        dimensions = self.images[self.cimg].get_rect()
        screen.blit(self.images[self.cimg], (int(self.x-dimensions.width/2), int(self.y-dimensions.height/2)))

    def update(self):
        if(self.ticker < self.lifetime):
            self.ticker += 1
            if(self.ticker % (self.lifetime/self.ticks) == 0):
                self.cimg += 1
        else:
            self.active = False
