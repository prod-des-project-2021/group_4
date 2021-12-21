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
        self.bigfont = pygame.font.SysFont('Arial', 80)
        self.clock = pygame.time.Clock()
        self.running = True
        self.tickrate = 120
        self.background = pygame.image.load("space.jpg")
        self.background = pygame.transform.scale(self.background, (1600,900))
        pygame.mixer.music.load('sfx/music_menu.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.25)
        self.clicksound = pygame.mixer.Sound("sfx/laser.ogg")
        self.clicksound.set_volume(0.05)
        
    def start(self):
        while(self.running):
            
            self.screen.fill(pygame.Color("black"))
            self.screen.blit(self.background,(0,0))
            mouseX, mouseY = pygame.mouse.get_pos()
            mouseclick = False

            textsurface = self.bigfont.render('Space Shooter', False, (pygame.Color("gold")))
            textrect = textsurface.get_rect()
            textrect.center = (800,200)
            self.screen.blit(textsurface,(textrect))

            textsurface1 = self.bigfont.render('Main Menu', False, (pygame.Color("gold")))
            textrect1 = textsurface1.get_rect()
            textrect1.center = (800,275)
            self.screen.blit(textsurface1,(textrect1))
            
            startGameText = 'Join Game'
            gamesurface = self.myfont.render(startGameText,True,(pygame.Color("gold")))
            startGameButton = gamesurface.get_rect()
            startGameButton.center = (800,450)
            startGameButton.w = gamesurface.get_width() + 20
            pygame.draw.rect(self.screen,(pygame.Color("darkgoldenrod")),startGameButton,5)
            self.screen.blit(gamesurface, (startGameButton.x + 10, startGameButton.y))

            creditsText = 'Credits'
            creditssurface = self.myfont.render(creditsText,True,(pygame.Color("gold")))
            creditsButton = creditssurface.get_rect()
            creditsButton.center = (800,550)
            creditsButton.w = creditssurface.get_width() + 20
            pygame.draw.rect(self.screen,(pygame.Color("darkgoldenrod")),creditsButton,5)
            self.screen.blit(creditssurface, (creditsButton.x + 10, creditsButton.y))

            optionsText = 'Options'
            optionssurface = self.myfont.render(optionsText,True,(pygame.Color("gold")))
            optionsButton = optionssurface.get_rect()
            optionsButton.center = (800,650)
            optionsButton.w = optionssurface.get_width() + 20
            pygame.draw.rect(self.screen,(pygame.Color("darkgoldenrod")),optionsButton,5)
            self.screen.blit(optionssurface,(optionsButton.x + 10, optionsButton.y))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouseclick = True

            if startGameButton.collidepoint((mouseX,mouseY)):
                if mouseclick:
                    self.clicksound.play()
                    self.enterInfo()
                
            if creditsButton.collidepoint((mouseX, mouseY)):
                if mouseclick:
                    self.clicksound.play()
                    self.credits()
            
            if optionsButton.collidepoint((mouseX,mouseY)):
                if mouseclick:
                    self.clicksound.play()
                    self.options()
          
            pygame.display.update()
            self.clock.tick(self.tickrate)
            pygame.display.flip()

    def enterInfo(self):
    
        userIgnRect = pygame.Rect(200,200,140,60)
        userIgnText = ''
        infoIgnText = 'In Game Name'
        infoIpText = 'IP Address'
        serverIPRect = pygame.Rect(200,300,140,60)
        serverIPText = '135.181.97.38'
        selectedClr  = pygame.Color("gold")
        notSelectedClr = pygame.Color("darkgoldenrod")
        color = notSelectedClr
        color1 = notSelectedClr
        textBoxActive = False
        textBoxActive2 = False
       
        while (self.running):
            self.screen.fill(pygame.Color("black"))
            self.screen.blit(self.background,(0,0))

            mouseX, mouseY = pygame.mouse.get_pos()
            mouseclick = False

            titlesurface = self.bigfont.render('Type your name and start playing', False,(pygame.Color("gold")))
            titlerect = titlesurface.get_rect()
            titlerect.center = (800,100)
            self.screen.blit(titlesurface,(titlerect))

            infoignsurface = self.myfont.render(infoIgnText,True,(pygame.Color("gold")))
            infoignrect = infoignsurface.get_rect()
            infoignrect.center = (800,300)
            self.screen.blit(infoignsurface,(infoignrect))

            infoipsurface = self.myfont.render(infoIpText,True,(pygame.Color("gold")))
            infoiprect = infoipsurface.get_rect()
            infoiprect.center = (800,475)
            self.screen.blit(infoipsurface,(infoiprect))

            gametext = 'Start Game'
            gamesurface = self.bigfont.render(gametext,True,(pygame.Color("gold")))
            gameButton = gamesurface.get_rect()
            gameButton.center = (800,750)
            gameButton.w = gamesurface.get_width() + 20
            pygame.draw.rect(self.screen,(pygame.Color("darkgoldenrod")),gameButton,5)
            self.screen.blit(gamesurface,(gameButton.x + 10, gameButton.y))

            menuButton = pygame.Rect(50,800,350,60)
            menuText = 'Back to Menu'
            pygame.draw.rect(self.screen,(pygame.Color("darkgoldenrod")),menuButton,5)
            menusurface = self.myfont.render(menuText,True,(pygame.Color("gold")))
            self.screen.blit(menusurface,(menuButton.x + 25, menuButton.y - 5))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouseclick = True

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if userIgnRect.collidepoint(event.pos):
                        textBoxActive = True
                    else:
                        textBoxActive = False
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
                if mouseclick:
                    self.clicksound.play()
                    pygame.mixer.music.fadeout(1000)
                    
                    if len(userIgnText) <= 0:
                        userIgnText = 'Anonym'
                        self.stateMachine.goto("game", args = (userIgnText, serverIPText))
                        
                    else:
                        self.stateMachine.goto("game", args = (userIgnText, serverIPText))

            if menuButton.collidepoint((mouseX,mouseY)):
                if mouseclick:
                    self.clicksound.play()
                    self.start()

            if textBoxActive:
                color = selectedClr
            else:
                color = notSelectedClr

            if textBoxActive2:
                color1 = selectedClr
            else:
                color1 = notSelectedClr

            ignSurface = self.myfont.render(userIgnText,True,(pygame.Color("gold")))
            ipsurface = self.myfont.render(serverIPText,True,(pygame.Color("gold")))
            serverIPRect.center = (800,550)
            userIgnRect.center = (800,375)
            serverIPRect.w = max(175,ipsurface.get_width() + 20)
            userIgnRect.w = max(175,ignSurface.get_width() + 20)
            pygame.draw.rect(self.screen,color,userIgnRect,5)
            pygame.draw.rect(self.screen,color1,serverIPRect,5)
            self.screen.blit(ignSurface, (userIgnRect.x + 10, userIgnRect.y - 5))
            self.screen.blit(ipsurface, (serverIPRect.x + 10, serverIPRect.y - 5))

            pygame.display.update()
            self.clock.tick(self.tickrate)
            pygame.display.flip()

    def credits(self):
        while(self.running):
            self.screen.fill(pygame.Color("black"))
            self.screen.blit(self.background,(0,0))

            mouseX, mouseY = pygame.mouse.get_pos()
            
            menuButton = pygame.Rect(50,800,350,60)
            menuText = 'Back to Menu'
            pygame.draw.rect(self.screen,(pygame.Color("darkgoldenrod")),menuButton,5)
            menusurface = self.myfont.render(menuText,True,(pygame.Color("gold")))
            self.screen.blit(menusurface,(menuButton.x + 25, menuButton.y - 5))
            
            titlesurface = self.myfont.render('Game Created By', False, (pygame.Color("gold")))
            textrect = titlesurface.get_rect()
            textrect.center = (800,200)
            self.screen.blit(titlesurface,(textrect))

            namesurface = self.myfont.render('Juho Taskila', False, (pygame.Color("gold")))
            textrect = namesurface.get_rect()
            textrect.center = (800,300)
            self.screen.blit(namesurface,(textrect))

            namesurface2 = self.myfont.render('Peetu Puumala', False, (pygame.Color("gold")))
            textrect = namesurface2.get_rect()
            textrect.center = (800,400)
            self.screen.blit(namesurface2,(textrect))

            namesurface3 = self.myfont.render('Ville Prittinen', False, (pygame.Color("gold")))
            textrect = namesurface3.get_rect()
            textrect.center = (800,500)
            self.screen.blit(namesurface3,(textrect))

            namesurface4 = self.myfont.render('Jukka Mäenpää', False, (pygame.Color("gold")))
            textrect = namesurface4.get_rect()
            textrect.center = (800,600)
            self.screen.blit(namesurface4,(textrect))

            mouseclick = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouseclick = True

            if menuButton.collidepoint((mouseX,mouseY)):
                if mouseclick:
                    self.clicksound.play()
                    self.start()

            pygame.display.update()
            self.clock.tick(self.tickrate)
            pygame.display.flip()

    def options(self):
        while(self.running):
            self.screen.fill(pygame.Color("black"))
            self.screen.blit(self.background,(0,0))

            mouseX, mouseY = pygame.mouse.get_pos()
            
            menuButton = pygame.Rect(50,800,350,60)
            menuText = 'Back to Menu'
            pygame.draw.rect(self.screen,(pygame.Color("darkgoldenrod")),menuButton,5)
            menusurface = self.myfont.render(menuText,True,(pygame.Color("gold")))
            self.screen.blit(menusurface,(menuButton.x + 25, menuButton.y - 5))

            muteText = 'Mute Music'
            mutemusicsurface = self.myfont.render(muteText,True,(pygame.Color("gold")))
            muteButton = mutemusicsurface.get_rect()
            muteButton.center = (800,200)
            muteButton.w = mutemusicsurface.get_width() + 20
            pygame.draw.rect(self.screen,(pygame.Color("darkslategray4")),muteButton)
            self.screen.blit(mutemusicsurface,(muteButton.x + 10, muteButton.y))

            volupText = '>'
            volupsurface = self.myfont.render(volupText,True,(pygame.Color("darkslategray4")))
            volupButton = volupsurface.get_rect()
            volupButton.center = (970,200)
            volupButton.w = volupsurface.get_width() + 20
            pygame.draw.rect(self.screen,(pygame.Color("gold")),volupButton)
            self.screen.blit(volupsurface,(volupButton.x + 10, volupButton.y))

            voldownText = '<'
            voldownsurface = self.myfont.render(voldownText,True,(pygame.Color("darkslategray4")))
            voldownButton = voldownsurface.get_rect()
            voldownButton.center = (630,200)
            voldownButton.w = voldownsurface.get_width() + 20
            pygame.draw.rect(self.screen,(pygame.Color("gold")),voldownButton)
            self.screen.blit(voldownsurface,(voldownButton.x + 10, voldownButton.y))

            volumesurface = self.myfont.render('Music Volume',True,(pygame.Color("gold")))
            volumerect = volumesurface.get_rect()
            volumerect.center = (800,100)
            self.screen.blit(volumesurface,(volumerect))

            sfxsurface = self.myfont.render('SFX Volume',True,(pygame.Color("gold")))
            sfxrect = sfxsurface.get_rect()
            sfxrect.center = (800,325)
            self.screen.blit(sfxsurface,(sfxrect))

            mutesfxText = 'Mute SFX'
            mutesfxsurface = self.myfont.render(mutesfxText,True,(pygame.Color("gold")))
            mutesfxButton = mutesfxsurface.get_rect()
            mutesfxButton.center = (800,425)
            mutesfxButton.w = mutesfxsurface.get_width() + 20
            pygame.draw.rect(self.screen,(pygame.Color("darkslategray4")),mutesfxButton)
            self.screen.blit(mutesfxsurface,(mutesfxButton.x + 10, mutesfxButton.y))

            sfxupText = '>'
            sfxupsurface = self.myfont.render(sfxupText,True,(pygame.Color("darkslategray4")))
            sfxupButton = volupsurface.get_rect()
            sfxupButton.center = (955,425)
            sfxupButton.w = sfxupsurface.get_width() + 20
            pygame.draw.rect(self.screen,(pygame.Color("gold")),sfxupButton)
            self.screen.blit(sfxupsurface,(sfxupButton.x + 10, sfxupButton.y))

            sfxdownText = '<'
            sfxdownsurface = self.myfont.render(sfxdownText,True,(pygame.Color("darkslategray4")))
            sfxdownButton = voldownsurface.get_rect()
            sfxdownButton.center = (645,425)
            sfxdownButton.w = sfxdownsurface.get_width() + 20
            pygame.draw.rect(self.screen,(pygame.Color("gold")),sfxdownButton)
            self.screen.blit(sfxdownsurface,(sfxdownButton.x + 10, sfxdownButton.y))

            mouseclick = False
            for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.running = False
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouseclick = True
            if voldownButton.collidepoint((mouseX,mouseY)):
                if mouseclick:
                    self.clicksound.play()
                    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.05)
                    if pygame.mixer.music.get_volume() <= 0.05:
                        pygame.mixer.music.set_volume(0)
            if volupButton.collidepoint((mouseX,mouseY)):
                if mouseclick:
                    self.clicksound.play()
                    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.05)
            if muteButton.collidepoint((mouseX,mouseY)):
                if mouseclick:
                  self.clicksound.play()
                  pygame.mixer.music.set_volume(0)
            if menuButton.collidepoint((mouseX,mouseY)):
                if mouseclick:
                    self.clicksound.play()
                    self.start()

            pygame.display.update()
            self.clock.tick(self.tickrate)
            pygame.display.flip()
            

