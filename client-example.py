import pygame
import math
from pygame.math import Vector2

ZERO_X = 1920/2
ZERO_Y = 1080/2

class Player:
    def __init__(self, sprite):
        self.sprite = sprite

        # rewritten movement with vectors
        self.position = Vector2(150.0, 150.0)
        self.UP = Vector2(0, 1)
        self.direction = Vector2(0, 1)
        self.velocity = Vector2(0, 0)
        self.acceleration = 0.25

        self.angle = 0.0
        self.rotatedSprite = None
        self.rotate() # initialize the rotated sprite

        self.max_velocity = 7.0

    def draw(self, screen):
        screen.blit(self.rotatedSprite, (int(self.position.x-self.dimensions.width/2), int(self.position.y-self.dimensions.height/2)))
        pygame.draw.line(screen, (255,255,255), (ZERO_X, 0), (ZERO_X, ZERO_Y*2))
        pygame.draw.line(screen, (255,255,255), (0, ZERO_Y), (ZERO_X*2, ZERO_Y))
        pygame.draw.line(screen, (255,0,0), (ZERO_X, ZERO_Y), (ZERO_X+self.direction.x*50, ZERO_Y+self.direction.y*50))
        pygame.draw.line(screen, (0,255,0), (ZERO_X, ZERO_Y), (ZERO_X+self.velocity.x*20, ZERO_Y+self.velocity.y*20))


    def rotate(self):
        self.direction = Vector2(self.UP)
        self.direction.rotate_ip(-self.angle)

        self.rotatedSprite = pygame.transform.rotate(self.sprite, int(self.angle)-90)
        self.dimensions = self.rotatedSprite.get_rect()

    def setAngle(self,angle):
        self.angle = radToDec(angle)

    def update(self, accelerating):
        if(accelerating):
            # limiting the velocity
            # guess it's little hacky but whatever
            tempVelocity = Vector2(self.velocity)
            tempVelocity += self.direction * self.acceleration

            # if incrementing velocity doesn't exceed max, allow it
            if(tempVelocity.length() < self.max_velocity):
                self.velocity += self.direction * self.acceleration

        else:
            if(self.velocity.length() > 0):
                # braking vector
                braking = Vector2(0.15, 0.15)
                rotation_angle = braking.angle_to(self.velocity)
                braking.rotate_ip(rotation_angle)
                self.velocity -= braking

        self.position += self.velocity
        self.rotate()


def radToDec(rad):
    return (rad*180/math.pi)

def decToRad(dec):
    return (dec/180*math.pi)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1024,768), pygame.RESIZABLE, vsync=1)
    clock = pygame.time.Clock()

    running = True

    # resources
    playerImg = pygame.image.load('res/player.png')
    player = Player(playerImg)

    # mouse boolean
    mouseDown = False

    while(running):

        # get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_angle = math.atan2(mouse_x - player.position.x, mouse_y - player.position.y)
        player.setAngle(player_angle)

        # draw stuff
        screen.fill(pygame.Color("black"))
        player.draw(screen)

        # update stuff
        player.update(mouseDown)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouseDown = False

        clock.tick(60)
        pygame.display.flip()
