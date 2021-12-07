import pygame 

class GameMonitor:
    def __init__(self, players): 
        self.players = players
        #self.rockets = rockets
        #self.bullets = bullets
        pygame.init()
        widthWindow = 1920
        heightWindow = 1080
        tickrate = 120
        self.screen = pygame.display.set_mode((widthWindow, heightWindow))
        pygame.display.set_caption("Tracking monitor")
        self.font = pygame.font.SysFont('Arial', 45) 
        self.screen = pygame.display.set_mode((widthWindow,heightWindow), pygame.RESIZABLE, vsync=1)
        clock = pygame.time.Clock()
        
        running = True
        while (running):
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(tickrate)
            pygame.display.flip()
        pygame.quit()

    def draw(self):
        self.screen.fill(pygame.Color("black"))
        for player in self.players:
            position = pygame.Rect(int(player.position.x), int(player.position.y), 64,64)
            pygame.draw.rect(self.screen, (255,0,0),position)
            self.screen.blit(self.font.render(str(player.health),True,(0,255,0)),(int(player.position.x), int(player.position.y)))
            
        #for bullet in self.bullets:
            #position = pygame.Rect(int(bullet.position.x),int(bullet.position.y),8,8)
            #pygame.draw.rect(self.screen,(0,0,255),position)

        #for rocket in self.rockets:
            #position = pygame.Rect(int(rocket.position.x),int(rocket.position.y),12,12)
            #pygame.draw.rect(self.screen,(0,255,0),position)
    
    
    
        
        
            

    