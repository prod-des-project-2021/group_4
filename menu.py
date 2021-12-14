from statemachine import State
import pygame
import sys
from pygame.locals import *
class Menu(State):
    def __init__(self, stateMachine):
        super().__init__(stateMachine)

    def initialize(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((1600,900))
        pygame.display.set_caption("MAIN MENU")
        self.myfont = pygame.font.SysFont('Arial', 60)
        self.clock = pygame.time.Clock()
        self.running = True
        self.tickrate = 120
        self.background = pygame.image.load("space.jpg")
        self.background = pygame.transform.scale(self.background, (1600,900))

    def start(self):
        while(self.running):
            
            self.screen.fill(pygame.Color("black"))
            self.screen.blit(self.background,(0,0))
            textsurface = self.myfont.render('Space Shooter', False, (pygame.Color("darkgoldenrod")))
            self.screen.blit(textsurface,(700,150))
            textsurface1 = self.myfont.render('Main Menu', False, (pygame.Color("darkgoldenrod")))
            self.screen.blit(textsurface1,(750,200))
            
            mouseX, mouseY = pygame.mouse.get_pos()
            startGameText = 'Join Game'
            creditsText = 'Credits'
            startGameButton = pygame.Rect(700,300,275,60)
            creditsButton = pygame.Rect(750,375,200,60)
            pygame.draw.rect(self.screen,(pygame.Color("darkgoldenrod")),startGameButton,5)
            pygame.draw.rect(self.screen,(pygame.Color("deepskyblue")),creditsButton,5)
            gamesurface = self.myfont.render(startGameText,True,(pygame.Color("gold")))
            creditssurface = self.myfont.render(creditsText,True,(pygame.Color("gold")))
            self.screen.blit(gamesurface, (startGameButton.x + 10, startGameButton.y - 5))
            self.screen.blit(creditssurface, (creditsButton.x + 20, creditsButton.y - 5))
            

            if startGameButton.collidepoint((mouseX,mouseY)):
                if click:
                    self.enterInfo()
                
            if creditsButton.collidepoint((mouseX, mouseY)):
                if click:
                    self.credits()

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
          
            pygame.display.update()
            self.clock.tick(self.tickrate)
            pygame.display.flip()

    def enterInfo(self):
    
        userIgnRect = pygame.Rect(200,200,140,60)
        userIgnText = ''
        serverIPRect = pygame.Rect(200,300,140,60)
        serverIPText = '135.181.97.38'
        selectedClr  = pygame.Color("gold")
        notSelectedClr = pygame.Color("darkgoldenrod")
        color = notSelectedClr
        textBoxActive = False
        textBoxActive2 = False

        while (self.running):
            self.screen.fill(pygame.Color("black"))
            self.screen.blit(self.background,(0,0))

            textsurface = self.myfont.render('Type your ign and server IP', False,(pygame.Color("darkgoldenrod")))
            self.screen.blit(textsurface,(700,150))

            

            gameButton = pygame.Rect(700,300,300,60)
            gametext = 'Start Game'
            pygame.draw.rect(self.screen,(pygame.Color("darkgoldenrod")),gameButton,5)
            gamesurface = self.myfont.render(gametext,True,(pygame.Color("gold3")))
            self.screen.blit(gamesurface,(gameButton.x + 25, gameButton.y - 5))

            menuButton = pygame.Rect(50,700,300,60)
            menuText = 'Back to Menu'
            pygame.draw.rect(self.screen,(pygame.Color("darkgoldenrod")),menuButton,5)
            menusurface = self.myfont.render(menuText,True,(pygame.Color("gold3")))
            self.screen.blit(menusurface,(menuButton.x + 25, menuButton.y - 5))

            mouseX, mouseY = pygame.mouse.get_pos()
            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if userIgnRect.collidepoint(event.pos):
                        textBoxActive = True
                    else:
                        textBoxActive = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if serverIPRect.collidepoint(event.pos):
                        textBoxActive2 = True
                    else:
                        textBoxActive2 = False

                if event.type == pygame.KEYDOWN:
                    if textBoxActive == True:
                        if event.key == pygame.K_BACKSPACE:
                            userIgnText = userIgnText[:-1]
                        else:
                            if len(userIgnText) < 8:
                                userIgnText += event.unicode
                    if textBoxActive2 == True:
                        if event.key == pygame.K_BACKSPACE:
                            serverIPText = serverIPText[:-1]
                        else:
                            if len(serverIPText) < 20:
                                serverIPText += event.unicode

            if gameButton.collidepoint((mouseX,mouseY)):
                if click:
                    self.stateMachine.goto("game", args = (userIgnText, serverIPText))
            
            if textBoxActive:
                color = selectedClr
            else:
                color = notSelectedClr
            if textBoxActive2:
                color = selectedClr
            else:
                color = notSelectedClr

            pygame.draw.rect(self.screen,color, userIgnRect,5)
            pygame.draw.rect(self.screen,color, serverIPRect,5)
            ignSurface = self.myfont.render(userIgnText,True,(pygame.Color("darkgoldenrod")))
            ipsurface = self.myfont.render(serverIPText,True,(pygame.Color("darkgoldenrod")))
            self.screen.blit(ignSurface, (userIgnRect.x + 5, userIgnRect.y - 5))
            self.screen.blit(ipsurface, (serverIPRect.x + 5, serverIPRect.y - 5))
            serverIPRect.w = max(175,ipsurface.get_width() + 10)
            userIgnRect.w = max(175,ignSurface.get_width() + 10)
            pygame.display.update()
            self.clock.tick(self.tickrate)
            pygame.display.flip()

    def credits(self):
        pass
