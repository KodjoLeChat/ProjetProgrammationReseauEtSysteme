""" Menu screen"""
import queue
from Vue.menu_button import *
from Vue.menu_settings import *
from Vue.input import *
from file_reader import reader_bmp_map
import pygame as pg
import sys
import pickle
import os
import multiprocessing
import logging
import subprocess  # Make sure to import subprocess at the beginning of your file

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def join_server(ip_port, username, password):
        # Logic to connect to the server
        # Example: connect_to_server(ip_port, username, password)
        logging.info(f"Joining server with IP:PORT={ip_port}, Username={username}, Password={password}")
        # Implement the actual server joining logic here

class Menu():
    GRAY = (169, 169, 169)
    def __init__(self, screen, controleur):
        self.controleur = controleur
        self.displayed = True
        self.screen = screen
        self.font = pg.font.SysFont('Constantia', 75)
        self.font2 = pg.font.SysFont('Constantia', 50)
        self.current = "Main"
        self.background = pg.transform.scale(background_of_menu, screen.get_size())
        self.mid_width = (self.screen.get_width() // 2) - (WIDTH_BUTTON // 2)
        self.mid_height = (self.screen.get_height() // 2) - (1.5 * HEIGHT_BUTTON)
        self.start = False
        self.load = False
        self.save = False
        self.pause = False
        #  next lines is for song
        try:
            pg.mixer.music.load(music_menu)
            pg.mixer.music.play(-1)
            self.volume = pg.mixer.music.get_volume()
        except pg.error as e:
            print(f"An error occurred: {e}")
            # Handle the error or fail gracefully

    def display_main(self):
        if self.displayed:

            # buttons
            self.Start_new_career = Button_Menu(self.screen, self.mid_width, self.mid_height - GAP, 'Start new career')
            self.Load_Saved_Game = Button_Menu(self.screen, self.mid_width, self.mid_height, 'Load Saved Game')
            self.Join_Game = Button_Menu(self.screen, self.mid_width, self.mid_height + GAP, 'Join Game')
            self.Options         = Button_Menu(self.screen, self.mid_width, self.mid_height + (2 * GAP), 'Options')
            self.Creators        = Button_Menu(self.screen, self.mid_width, self.mid_height + (3 * GAP), 'Creators')
            self.Exit            = Button_Menu(self.screen, self.mid_width, self.mid_height + (4 * GAP), 'Exit')
            
    def events(self, event):
        if self.Start_new_career.check_button(event):
            self.Start_new_career.current_col = self.Start_new_career.button_col
            self.controleur.create_new_game()
            self.controleur.metier.init_board(reader_bmp_map(1, self.controleur))
            self.controleur.ihm.init_sprite()
            self.controleur.play()

        if self.Load_Saved_Game.check_button(event):
            if os.path.exists("save.sav"):
                self.controleur.metier = pickle.load(open("save.sav", 'rb'))
                # fixe la taille du plateau de jeu
                self.controleur.grid_height  = len(self.controleur.metier.monde.board)
                self.controleur.grid_width = len(self.controleur.metier.monde.board[0])

                self.controleur.ihm.init_sprite()
                try:
                    subprocess.Popen(["./sender"])
                except Exception as e:
                    print(f"Failed to execute sender: {e}")
                self.controleur.play()
        
        if self.Join_Game.check_button(event):
            self.current = "Join Game"
            self.display_settings_join()
            run = False

        if self.Exit.check_button(event):
            run = False
            sys.exit()

        if self.Options.check_button(event):
            self.current = "Options"
            self.display_settings()
            run = False

        if self.Creators.check_button(event):
            self.current = "Creators"
            self.display_creators()
            run = False
        
        if event.type == pg.QUIT:
            run = False
            sys.exit()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.font.render(" Romulus Online ", True, BLUE_SKY),
                         (self.mid_width - 120, self.mid_height - (2.5 * GAP)))

        self.Start_new_career.draw()
        self.Load_Saved_Game.draw()
        self.Join_Game.draw()
        self.Creators.draw()
        self.Options.draw()
        self.Exit.draw()
        pg.display.flip()

    def display_settings(self):
        if self.displayed:

            pg.display.set_caption(' Romulus Online ')

            # buttons
            Exit        = Button_Menu(self.screen, self.mid_width, self.mid_height + (5*GAP), 'Exit')
            Volume_up   = Button_Menu(self.screen, self.mid_width + (3.5 * GAP), self.mid_height + GAP, '+ Volume Up')
            Volume_down = Button_Menu(self.screen, self.mid_width - (3*GAP), self.mid_height + GAP, '- Volume Down')
            Return      = Button_Menu(self.screen, self.mid_width, self.mid_height - GAP * 2, 'Return')

            run = True
            while run:
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.font.render("Settings", True, RED,(249, 231, 159)), (self.mid_width +30, self.mid_height - GAP*3.25))

                for event in pg.event.get():
                    if Volume_down.check_button(event):
                        if self.volume > 0.0:
                            self.volume -= 0.1
                            pg.mixer.music.set_volume(self.volume)

                    if Volume_up.check_button(event):
                        if self.volume < 1.0:
                            self.volume += 0.1
                            pg.mixer.music.set_volume(self.volume)

                    if Return.check_button(event):
                        run = False
                        self.current = "Main"
                        self.display_main()

                    if Exit.check_button(event):
                        run = False
                        sys.exit()

                    if event.type == pg.QUIT:
                        run = False
                        pg.quit()

                Exit.draw()
                Volume_up.draw()
                Volume_down.draw()
                Return.draw()
                pg.display.flip()

    def display_settings_join(self):
        if self.displayed:
            pg.display.set_caption(' Romulus Online ')
            print("test")
            # Input buttons
            ip_port_input = InputButton(self.screen, self.mid_width, self.mid_height + (5*2), 'IP', '')
            port_input = InputButton(self.screen, self.mid_width, self.mid_height + (8*20), 'PORT', '')
            password_input = InputButton(self.screen, self.mid_width, self.mid_height + (11*30), 'Username', '')

            # Other buttons
            Return = Button_Menu(self.screen, self.mid_width, self.mid_height - GAP, 'Return')
            Join = Button_Menu(self.screen, self.mid_width, self.mid_height - GAP * 2, 'Join')

            run = True
            while run:
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.font.render("Settings", True, RED, (249, 231, 159)), (self.mid_width + 30, self.mid_height - GAP*3.25))

                for event in pg.event.get():
                    if ip_port_input.check_button(event):
                        # Handle IP:PORT input
                        ip_port = ip_port_input.input_text
                        # You may want to parse and store the IP:PORT somewhere

                    if port_input.check_button(event):
                        # Handle username input
                        username = port_input.input_text
                        # You may want to store the username somewhere

                    if password_input.check_button(event):
                        # Handle password input
                        password = password_input.input_text
                        # You may want to store the password somewhere (consider security implications)
           
                    if Return.check_button(event):
                        run = False
                        self.current = "Main"
                        self.display_main()
                        
                    if Join.check_button(event):
                        ip = ip_port_input.input_text
                        port = port_input.input_text
                        password = password_input.input_text
                        print(f"Joining server with IP={ip}, PORT={port}, Password={password}")
                        with open('config.txt', 'w') as config_file:
                            config_file.write(f"{ip} {port}\n")                        
                        # Execute the receiver program
                        try:
                            subprocess.run(["./receiver"])
                        except Exception as e:
                            print(f"Failed to execute receiver: {e}")
                            
                        if os.path.exists("onlineWorld.sav") and os.path.getsize("onlineWorld.sav") > 0:
                            with open("onlineWorld.sav", 'rb') as file:
                                self.controleur.metier = pickle.load(file)                            # fixe la taille du plateau de jeu
                            self.controleur.grid_height  = len(self.controleur.metier.monde.board)
                            self.controleur.grid_width = len(self.controleur.metier.monde.board[0])

                            self.controleur.ihm.init_sprite()
                            self.controleur.is_Joining=True
                            self.controleur.play()
                        else:
                            print("onlineWorld.sav is empty or does not exist")
                                
                        run = False
                        self.current = "Main"
                        self.display_main()


                ip_port_input.draw()
                port_input.draw()
                password_input.draw()
                Return.draw()
                Join.draw()
                pg.display.flip()


        
    def display_creators(self):
        if self.displayed:

            #pg.display.set_caption(' keaserV ')
            Return = Button_Menu(self.screen, self.mid_width, self.mid_height - GAP * 2, 'Return')

            run = True
            while run:
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.font.render("Awa", True, GREEN_DARK ,(255, 255, 255)),
                                (self.mid_width*0.95, self.mid_height - 40))
                self.screen.blit(self.font.render("Rayane", True, GREEN_DARK,(255, 255, 255)),
                                (self.mid_width * 0.95, self.mid_height + 35))
                self.screen.blit(self.font.render("Philémon", True, GREEN_DARK,(255, 255, 255)),
                                (self.mid_width * 0.95, self.mid_height + (GAP+35)))
                self.screen.blit(self.font.render("Ayet", True, GREEN_DARK,(255, 255, 255)),
                                (self.mid_width * 0.95, self.mid_height + GAP * 2 +35))
                self.screen.blit(self.font.render("Pérès", True, GREEN_DARK,(255, 255, 255)),
                                (self.mid_width * 0.95, self.mid_height + GAP * 3 + 35))
                Return.draw()
                for event in pg.event.get():
                    if Return.check_button(event):
                        run = False
                        self.current = "Main"
                        self.display_main()

                    if event.type == pg.QUIT:
                        run = False
                        sys.exit()


                pg.display.update()