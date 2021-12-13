import pygame

class TextObject:
    def __init__(self, text, font, color):
        self.text = text

        self.font = pygame.font.SysFont(font, 15)
        self.color = color
        self.textSurface = self.font.render(self.text, False, self.color)

        self.x = 0
        self.y = 0

    def draw(self, screen):
        screen.blit(self.textSurface, (self.x, self.y))

    def updateText(self, text):
        # update the text only when it's actually changing
        if(self.text != text):
            self.text = text
            self.textSurface = self.font.render(self.text, False, self.color)

    def setPosition(self, x, y):
        self.x = x
        self.y = y
