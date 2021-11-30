import pygame

class DestroyEnemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,6):
            img = pygame.image.load(f"img/wut ({num}).jpg")
            img = pygame.transform.scale(img,(50,50))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
    
    def update(self):
        animationSpeed = 4
        self.counter += 1

        if self.counter >= animationSpeed and self.index < len(self.images) -1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images) - 1 and self.counter >= animationSpeed:
            self.kill()

    