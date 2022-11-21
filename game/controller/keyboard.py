import pygame

class keyboard:

    def __init__(self,game):
        self.game = game
        self.pressed = {}
        self.test = 1
        self.wantToSave = False
        self.wantToLoad = False
        self.wantToPause = False
        self.wantToZoom = False

    def notify(self):
        for event in pygame.event.get():
            if self.game.get_state():
                self.key_down_playing(event)


    def key_down_playing(self,event):
        """
        Gère les évenements pendant le jeu
        """
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            self.quit_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.pressed[pygame.MOUSEBUTTONDOWN] = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.pressed[pygame.MOUSEBUTTONDOWN] = False

        elif event.type == pygame.MOUSEMOTION:
            self.pressed[pygame.MOUSEMOTION] = True
        elif event.type != pygame.MOUSEMOTION:
            self.pressed[pygame.MOUSEMOTION] = False


        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    print("ok Tu veux zoomer mais marhe pas")
                    self.wantToZoom = True
        elif event.type == pygame.KEYUP:
            self.pressed[event.key] = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.test >= 1:
                   print("ok tu changes le tps")
                   self.test += 1
                if self.test < 1:
                    print("ok tu changes le tps")
                    self.test += 0.1
            elif event.key == pygame.K_DOWN:
                if self.test > 0:
                    print("ok tu changes le tps")
                    if self.test > 1:
                       self.test -= 1
                    if self.test <= 1:
                       self.test -= 0.1
            '''get KEY S EVENT AND TURN TRUE WANTTOSAVE'''
            if event.key == pygame.K_s:
                print("ok tu veux save")
                self.wantToSave = True
            if event.key == pygame.K_l:
                print("ok tu veux load")
                self.wantToLoad = True
            if event.key == pygame.K_p:
                if self.wantToPause == False:
                    print("ok tu veux pause")
                    self.wantToPause = True
                elif self.wantToPause == True:
                    print("Ok je résume le jeu")
                    self.wantToPause = False
                    
    def key_down_menu(self):
        pass

    def get_keyboard_input(self):
        return self.pressed

    def quit_game(self):
        self.game.set_playing(False)
        self.game.set_state(False)
