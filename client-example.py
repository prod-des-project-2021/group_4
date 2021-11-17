import pygame
import math

class Player:
    def __init__(self, sprite):
        self.sprite = sprite
        self.x = 150.0
        self.y = 150.0

        self.xv = 0.0
        self.yv = 0.0

        self.angle = 0.0
        self.rotatedSprite = None
        self.rotate() # initialize the rotated sprite

        self.velocity = 0.0
        self.max_velocity = 6.0
        self.velocity_increment = 0.25
        self.velocity_decrement_x = 0.05
        self.velocity_decrement_y = 0.05

    def draw(self, screen):
        screen.blit(self.rotatedSprite, (int(self.x-self.dimensions.width/2), int(self.y-self.dimensions.height/2)))

    def rotate(self):
        self.rotatedSprite = pygame.transform.rotate(self.sprite, int(self.angle)-90)
        self.dimensions = self.rotatedSprite.get_rect()

    def setAngle(self,angle):
        self.angle = radToDec(angle)

    def update(self, accelerating):
        if(accelerating):
            self.xv = self.xv + math.sin(decToRad(self.angle)) * self.velocity_increment
            self.yv = self.yv + math.cos(decToRad(self.angle)) * self.velocity_increment
            

            print("xv: "+str(self.xv)+" yv: "+str(self.yv))

            self.velocity_decrement_x = abs(self.xv / 75)
            self.velocity_decrement_y = abs(self.yv / 75)

        else:
            if(self.xv > 0):
                self.xv = self.xv - self.velocity_decrement_x
            if(self.xv < 0):
                self.xv = self.xv + self.velocity_decrement_x

            if(self.yv > 0):
                self.yv = self.yv - self.velocity_decrement_y
            if(self.yv < 0):
                self.yv = self.yv + self.velocity_decrement_y

            # zero the velocity
            if(self.xv < self.velocity_decrement_x and self.xv > -self.velocity_decrement_x):
                self.xv = 0

            if(self.yv < self.velocity_decrement_y and self.yv > -self.velocity_decrement_y):
                self.yv = 0

        self.x = self.x + self.xv
        self.y = self.y + self.yv
        self.rotate()


def radToDec(rad):
    return (rad*180/math.pi)

def decToRad(dec):
    return (dec/180*math.pi)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1024,768))
    clock = pygame.time.Clock()

    running = True

    # resources
    playerImg = pygame.image.load('res/player.png')
    player = Player(playerImg)

    # mouse boolean
    mouseDown = False

    while(running):
        clock.tick(60)
        # get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_angle = math.atan2(mouse_x - player.x, mouse_y - player.y)
        player.setAngle(player_angle)

        # draw stuff
        screen.fill(pygame.Color("black"))
        player.draw(screen)

        # update stuff
        player.update(mouseDown)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouseDown = False
