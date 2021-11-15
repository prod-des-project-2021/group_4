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
    packet.priority = Packet.Priority.ACK_REQUIRED
    packet.seq = 1
    packet.type = Packet.Type.ACK

    packet.setPayload(bytes("assssdasdasdassss this can be anything", "utf-8"))

    endp = packet.encode()
    packet2 = Packet()
    packet2.decode(endp)

    packet2.printDebug()

    pygame.init()
    screen = pygame.display.set_mode((800,600))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(packet2.encode(), ("127.0.0.1", 5555))
    running = True

    obj = Square()

    while(running):
        packet2.seq = int(obj.x)

        screen.fill(pygame.Color("black"))
        obj.update()
        obj.draw(screen)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == '__main__':
    main()
