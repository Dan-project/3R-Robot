"""
File: robot3r.py
Author: Dan Calamia and some codes provided by Sylvain Argentieri
Date: 06/2025
Description: Simulation of 3R plan robot.
"""

# Importation pygame pour la simualtion
import pygame
# Importation matplotlib
import matplotlib.pyplot as plt
from motor import *

class Univers:
    """
    Classe Univers:
    Création d'un univers pour la simulation d'un robot nR plan.
    Le control du robot via les touches est valables que pour les robots 3R, à modifier si besoin.

        Paramètres:
            - robot (instance de Robot)
            - nMotors (nombre de moteurs à initialiser, ici toujours 3)
            - portName (nom du port usb à renseigner dans le main)

        Fonctions:
            - 'convertToPygame' : convertit les coordonnées pour l'affichage Pygame (centrage + redimensionnement)
            - 'plotRobot': plot le robot à n articulations, et la cible target si elle existe
            - 'draw_text', 'draw_controls', 'draw_info' : écris le text sur la fenètre Pygame
            - 'jointSpaceControl' : controler les paramètres articulaires
            - 'cartesianControl': controler l'effecteur
            - 'run': coeur du programme pour lancer la simulation

    """ 
    def __init__(self,robot,connected=False,portName=None):
        
        # État du robot
        self.connected=connected

        # Création d'un robot
        self.robot=robot

        if self.connected:
            # try:
            self.motors= Motor(self.robot,len(self.robot.q),portName)
            # except:
            #     print("Initialisation des moteurs échoués")

        # Initialisation Pygame
        pygame.init()
        self.width, self.height = 700, 700
        self.scale = self.width / 0.5 # 0.5/0.5 mètre
        self.window = pygame.display.set_mode((self.width, self.height))
        self.FPS = 60

    # PLOT
    def convertToPygame(self, pos):
        x = ((pos[0]) * self.scale) + self.width//2
        y =  self.height//2-(( pos[1]) * self.scale)
        return int(x), int(y)

    def plotRobot(self,pos_target=None):
        # Couleurs 
        bg = (245, 245, 245)
        joint_color = (255, 50, 50)
        link_color = (40, 90, 200)
        effector_color = (0, 150, 0)

        self.window.fill(bg) 

        # Liste des points ( positions de chaques articulations )
        points = self.robot.pos
        
        # Tracer les segments
        for i in range(len(points)-1):
            pygame.draw.line(self.window, link_color,
                            self.convertToPygame(points[i]),
                            self.convertToPygame(points[i+1]),
                            width=4)

        # Tracer les articulations
        for i, point in enumerate(points):
            color = effector_color if i == len(points)-1 else joint_color
            pygame.draw.circle(self.window, color, self.convertToPygame(point), 6)
            if i==len(points)-1:
                self.draw_text(f"eff", self.convertToPygame(point), size=14)
            else:
                self.draw_text(f"q{i+1}", self.convertToPygame(point), size=14)


        if pos_target is not None:
            pygame.draw.circle(self.window, (255,0,0), self.convertToPygame(pos_target), 8)

        message=""
        if self.connected:
            message = "(robot connecté)"

        pygame.display.set_caption(f"Simulation {message} du robot nR plan")

        pygame.display.flip()

   # DRAW INFO WINDOW     
    def draw_text(self, text, pos, size=16, color=(0, 0, 0)):
        font = pygame.font.SysFont("Arial", size)
        label = font.render(text, True, color)
        self.window.blit(label, pos)

    def draw_controls(self):
        control1 = [
            "Commandes articulaires :",
            "A / Q : + / - Articulation 1",
            "Z / S : + / - Articulation 2",
            "E / D : + / - Articulation 3"
        ]
        control2 = [
            "Commandes opérationnelles :",
            "Arrow (UP, DOWN, LEFT, RIGHT)",
        
        ]

        for i, line in enumerate(control1):
            self.draw_text(line, pos=(10, 100 + i * 22), size=16)
        for i, line in enumerate(control2):
            self.draw_text(line, pos=(10, 190 + i * 22), size=16)
 
    def draw_info(self):

        info=[f"États des articulations: "]
        for i in range(len(self.robot.q)):
            info.append(f"q{i} : x={self.robot.pos[i][0]*100:.2f} cm, y={self.robot.pos[i][1]*100:.2f} cm, q1 : {self.robot.q[i]:.2f}°")

        for i, line in enumerate(info):
            self.draw_text(line, pos=(10,10+22*i), size=16)

    # SIMULATION
    def simulateVirtualRobot(self,mode, q_target, pos_target, vitesse_deg_par_s):
        running = True
        self.robot.MGD() # Intialise les positions
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                                    

            if mode=="interpolationArti":
                # -------- À COMPLÉTER AU TP1 --------
                pass

            elif mode=="interpolationOpe":
                # -------- À COMPLÉTER AU TP1 --------
                pass              



            self.robot.MGD()
            self.plotRobot()

        pygame.display.quit()   # ferme la fenêtre
        pygame.quit()  
  
    def simulateRealRobot(self,mode, q_target, pos_target, vitesse_deg_par_s):
        """
        Simulation continue du robot. 
        vitesse_deg_par_s : vitesse angulaire de déplacement en degrés/seconde.
        état : connecté 
        mode = q_atrget, pos_target
        """
        clock = pygame.time.Clock()
        running = True
        self.robot.MGD() # Intialise les positions

        while running:
            dt = clock.tick(self.FPS) / 1000.0  # durée en secondes entre les frames
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            if self.connected:

                self.motors.updateMotors()

                if mode=="qTarget":
                     # -------- À COMPLÉTER AU TP2 --------
                    pass


                elif mode == "posTarget":
                     # -------- À COMPLÉTER AU TP2 --------
                    pass
                    
            # mets à jour les positions 
            self.robot.MGD()
            # affiche le robot
            self.plotRobot()

        # déasctive le couple moteur
        for i in range(len(self.robot.q)):
                self.motors.motors[i].torque_disable()

        pygame.display.quit()   # ferme la fenêtre
        pygame.quit()  
    
    def run(self,mode, q_target=None, pos_target=None, vitesse_deg_par_s=30):
        if self.connected:
            self.simulateRealRobot(mode, q_target, pos_target, vitesse_deg_par_s)
        else:
            self.simulateVirtualRobot(mode, q_target, pos_target, vitesse_deg_par_s)