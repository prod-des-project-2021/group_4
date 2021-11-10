import socket
import pygame

from networking import Packet

class Square:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.w = 50
        self.h = 50
        self.xv = 0.4
        self.yv = 0.4

    def update(self):
        self.x = self.x + self.xv
        self.y = self.y + self.yv

        if self.x < 0 or self.x > 800 - self.w:
            self.xv =- self.xv

        if self.y < 0 or self.y > 600 - self.h:
            self.yv =- self.yv

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color("red"), (self.x, self.y, self.w, self.h))

def main():
    packet = Packet()
    packet.priority = 1
    packet.seq = 0
    packet.payload = 1593953959

    print(packet.encode())

    pygame.init()
    screen = pygame.display.set_mode((800,600))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b'test', ("127.0.0.1", 5555))
    running = True

    obj = Square()

    while(running):
        screen.fill(pygame.Color("black"))
        obj.update()
        obj.draw(screen)

        sock.sendto(bytes(int(obj.x)), ("127.0.0.1", 5555))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == '__main__':
    main()
