import pygame as pg

from .adding_engeneer import AddingEngeneer

from .bouton_hud import Button_HUD
from .adding_building import Adding_Building
from .clear import Clear
from .addingRoad import Adding_Road
import threading
import json


# permet de gerer les HUD du haut et de la droite
class HUD:
    def __init__(self, screen, carriere, netstat):
        self.screen   = screen
        self.carriere = carriere
        self.longueur = self.screen.get_width() 
        self.hauteur = self.screen.get_height()
        self.action = None
        self.netstat = netstat
        #dimension image
        REFERENCE_SIZE_X = 1920
        REFERENCE_SIZE_Y = 1080
        self.count2 = 0 # for test
        # ecart entre chaque action de l'hud de droite 
        HORIZONTAL_GAP = self.longueur*0.032
        VERTICAL_GAP   = self.hauteur *0.0415

        #chargement de l'image
        self.hud_right = pg.image.load("./assets/hud/hud_right.png").convert_alpha()
        size_hud_right = (self.hud_right.get_width()*self.longueur/REFERENCE_SIZE_X, self.hud_right.get_height()*self.hauteur/REFERENCE_SIZE_Y)
        self.hud_right = pg.transform.scale(self.hud_right, size_hud_right)

        self.hud_top = pg.image.load("./assets/hud/hud_top.png").convert_alpha()
        size_hud_top = (self.hud_top.get_width()*self.longueur/REFERENCE_SIZE_X, self.hud_top.get_height()*self.hauteur/REFERENCE_SIZE_Y)
        self.hud_top =  pg.transform.scale(self.hud_top, size_hud_top)

        # double boucle, pour pouvoir rajouter de future action
        # permet de gérer ensuite les evenements
        actions = ["build", "clear", "road", "", "", "", "", "", "", "engeneer", "attack", ""]
        self.button_hud_right = {}
        for i in range(4):
            for j in range(3):
                if actions[i*3+j] != "":
                    self.button_hud_right[actions[i*3+j]] = Button_HUD(self.screen,
                                                                   self.screen.get_width()*0.905+j*HORIZONTAL_GAP,
                                                                   self.screen.get_height()*0.348+i*VERTICAL_GAP ,
                                                                   actions[i*3+j])





    # traite les evenements
    def events(self, event):
        pos = pg.mouse.get_pos()

        # si nous avons une action en cours alors nous faisons les evenements de cette action
        # tout est au moins basic_action
        if self.action is not None:
            self.action.events(event)
            if self.action.is_progress == False:
                self.carriere.reload_board()
                self.action = None
        
        # s'il y a colision avec l'un des boutons alors on initialise une action si elle n'existe pas 
        for button in self.button_hud_right:
            if self.button_hud_right[button].rect.collidepoint(pos):
                # affichage
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    self.button_hud_right[button].who_is_visible = "image_click"
                    #interaction 
                elif event.type == pg.MOUSEBUTTONUP and event.button == 1 and self.button_hud_right[button].who_is_visible == "image_click":
                    match button:
                        # si nous voulons rajouter des actions, cela devient donc très simple
                        case "build":
                            if self.action == None: 
                                self.action = Adding_Building(self.carriere, "assets/upscale_house/Housng1a_00045.png",self.netstat)
                                method = "Adding_Building"
                                params = {
                                    "image_path": "assets/upscale_house/Housng1a_00045.png",

                                }

                                message = {
                                    "method": method,
                                    "params": params
                                }                                
                                self.netstat.send(message)
                            if not self.action.is_progress:
                                self.action.is_progress = True
                                image = pg.image.load("assets/upscale_land/Land2a_00001.png")
                                self.action.initialiser(image)
                        case "clear":
                            if self.action == None: self.action = Clear(self.carriere, "assets/upscale_land/red_image.png")

                            if not self.action.is_progress:
                                self.action.is_progress = True
                                image = pg.image.load("assets/upscale_land/red_image.png")
                                self.action.initialiser(image)
                        case "road":
                            if self.action == None: self.action = Adding_Road(self.carriere)

                            if not self.action.is_progress:
                                self.action.is_progress = True
                                image = pg.image.load("assets/upscale_road/Land2a_00094.png")
                                self.action.initialiser(image)
                        case "engeneer":

                            if self.action == None:
                                self.action = AddingEngeneer(self.carriere)
                                self.action.is_progress = True
                                image = pg.image.load("assets/upscale_land/Land2a_00001.png")
                                self.action.initialiser(image)
                                method = "Adding_Building"
                                params = {
                                    "image_path": "assets/upscale_house/Housng1a_00045.png",


                                }
                                message = {
                                    "method": method,
                                    "params": params
                                }
                                self.netstat.send(message)
                        case "stats":
                            if self.action == None: self.action = AddingEngeneer(self.carriere)
                            if not self.action.is_progress:
                                self.action.is_progress = True
                                image = pg.image.load("assets/upscale_land/Land2a_00001.png")
                                self.action.initialiser(image)
                elif self.button_hud_right[button].who_is_visible != "image_click":
                    self.button_hud_right[button].who_is_visible = "image_hover"

            else:
                self.button_hud_right[button].who_is_visible = ""
        
        if self.count2 == 0:  # pour test, à supprimer
            self.netstat.received_data_ADDING_BUILDING.append({"method": "Adding_Building", "params": {"image_path": "assets/upscale_house/Housng1a_00045.png"}})
            self.netstat.received_data.append({"method": "treat_event", "grid_pos": [20, 13], "last_grid": [20, 13], "SelectionneurZone": [116, 60], "pos": [1417, 509], "Ressources": "{\"food\": 0, \"water\": 0, \"dinars\": 4000, \"population\": 0, \"username\": \"player2\"}"})

            self.netstat.received_data_WALKER.append({"method": "walker_creation", "params": {"depart": [20, 39], "destination": [20, 13]}})
            self.netstat.received_data.append({"method": "treat_event_bis"})
            self.count2+=1

        # Check if there is any data received
        #net_event = self.netstat.start_receiving_thread()
        if self.netstat.received_data_WALKER:
            # Look at the first item in the list without removing it
            #action_data = self.netstat.received_data[0]
            action_data = self.netstat.received_data_WALKER[0]

            if action_data.get("method") == "walker_creation":
                # Pop the first item from the list as it's a 'walker_creation' action
                print("avant creation du walker : AAAAAAAAAAAAAAAAA" + str(self.netstat.received_data_WALKER))
                action_data = self.netstat.received_data_WALKER.pop(0)
                print("après création du walker: AAAAAAAAAAAAAAAAA" + str(self.netstat.received_data_WALKER))
                print("action date walker : " ,action_data)

                self.execute_action(action_data)

        if self.netstat.received_data_ADDING_BUILDING:
            # Look at the first item in the list without removing it
            action_data = self.netstat.received_data_ADDING_BUILDING[0]

            if action_data.get("method") == "Adding_Building":
                # Pop the first item from the list as it's an 'Adding_Building' action
                print("avant: AAAAAAAAAAAAAAAAA" + str(self.netstat.received_data_ADDING_BUILDING))
                action_data = self.netstat.received_data_ADDING_BUILDING.pop(0)
                print("après: AAAAAAAAAAAAAAAAA" + str(self.netstat.received_data_ADDING_BUILDING))

                self.execute_action(action_data)
                #print(action_data)
            else:
                # Handle other methods or leave the item in the list
                pass  # Replace with your handling logic for other methods


    def execute_action(self, action_data):
        print("TESTTTTTTTTTTTTTTTTTTTTT RAYANE")
        if "method" in action_data and "params" in action_data:
            method = action_data["method"]
            params = action_data["params"]
            
            match method:
                case "Adding_Building":
                    # Handle 'build' action
                    print("constructing building")

                    if self.action is None:
                        # Create the action and start the waiting thread
                        self.action = Adding_Building(self.carriere, "assets/upscale_house/Housng1a_00045.png", self.netstat)
                        threading.Thread(target=self.wait_for_treat_event, daemon=True).start()
                        # Gestion de l'arrivée du migrant

                case "walker_creation":
                    # Traitement pour le départ du walker
                    print("Creating walker")
                    if self.action is None:
                        self.action = Adding_Building(self.carriere, "assets/upscale_house/Housng1a_00045.png",
                                                      self.netstat)
                        threading.Thread(target=self.wait_for_treat_event, daemon=True).start()

                        # Envoyer l'information pour le départ du walker
                        #self.netstat.received_data({"method":"walker_creation", "params": {"depart": [20, 39], "destination": [20, 13]} })

                        self.carriere.controleur.walker_creation((20, 39), (20, 13))

                case "AddingEngeneer":
                    # Handle 'clear' action
                    print("constructing engeneer")

                    if self.action is None:
                        # Create the action and start the waiting thread
                        self.action = Adding_Building(self.carriere, "assets/upscale_house/Housng1a_00045.png", self.netstat)
                        threading.Thread(target=self.wait_for_treat_event, daemon=True).start()
    def wait_for_treat_event(self):
        while True:
            # Use a thread lock if needed to safely access self.netstat.received_data
            for i in range(len(self.netstat.received_data)):
                print("BRAVOOO ! ")
                action_data = self.netstat.received_data[i]
                if action_data.get("method") == "treat_event":
                    if action_data.get("grid_pos"):
                        grid = action_data.get("grid_pos")
                        ressources_json = action_data.get("Ressources")
                        ressources = json.loads(ressources_json)  # Parse the JSON string
                        print(ressources)
                        test = action_data.get("SelectionneurZone")
                        test2 = action_data.get("pos")
                        self.action.test = test
                        self.action.test2 = test2
                        self.action.original_surface = test
                        print("coordonnees du walker : ", grid, test)
                        self.carriere.controleur.walker_creation(grid, test)

                        print("PARFAIT ! ")


                        if grid and ressources:
                            # Call the treat_event_local method with the extracted data
                            self.action.treat_event_local(grid, ressources,action_data.get("method") )
                            # Remove the processed item from received_data
                            del self.netstat.received_data[i]
                            return  # Exit the loop and thread after processing
                    if action_data.get("method") == "treat_event_enge":
                        print("LETS GOO")



            # Optionally, add a small delay here to prevent high CPU usage


    # affiche les images et les boutons suite aux evenements
    def draw(self):
        if self.action is not None: self.action.draw()

        self.screen.blit(self.hud_right, (self.longueur*0.895, self.hauteur*0.0235))
        self.screen.blit(self.hud_top, (0, 0))

        for button in self.button_hud_right:
            self.button_hud_right[button].draw()