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
            - 'simulation': coeur du programme pour lancer la simulation

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

        if len(self.robot.q)==3:
            self.draw_controls()
        self.draw_info()

        if pos_target is not None:
            pygame.draw.circle(self.window, (255,0,0), self.convertToPygame(pos_target), 8)

        message=""
        if self.connected:
            message = "(robot connecté)"

        pygame.display.set_caption(f"Simulation {message} du robot nR plan")

        pygame.display.flip()
        
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

    def jointSpaceControl(self):
        """
        Commande en espace articulaire
        """
        keys = pygame.key.get_pressed()
        if not self.connected:
            if keys[pygame.K_a]:
                self.robot.q[0] += 1
            if keys[pygame.K_q]:
                self.robot.q[0] -= 1
            if keys[pygame.K_z]:
                self.robot.q[1] += 1
            if keys[pygame.K_s]:
                self.robot.q[1] -= 1
            if keys[pygame.K_e]:
                self.robot.q[2] += 1
            if keys[pygame.K_d]:
                self.robot.q[2] -= 1

        else:
            

            if keys[pygame.K_a]:
                self.motors.motors[0].set_position(int(self.motors.deg_to_pos(self.robot.q[0]))+10)
            if keys[pygame.K_q]:
                self.motors.motors[0].set_position(int(self.motors.deg_to_pos(self.robot.q[0]))-10)
            if keys[pygame.K_z]:
                self.motors.motors[1].set_position(int(self.motors.deg_to_pos(self.robot.q[1]))+10)
            if keys[pygame.K_s]:
                self.motors.motors[1].set_position(int(self.motors.deg_to_pos(self.robot.q[1]))-10)
            if keys[pygame.K_e]:
                self.motors.motors[2].set_position(int(self.motors.deg_to_pos(self.robot.q[2]))+10)
            if keys[pygame.K_d]:
                self.motors.motors[2].set_position(int(self.motors.deg_to_pos(self.robot.q[2]))-10)
    
    def cartesianControl(self):
        """
        Commande en espace opérationnel
        """
        keys = pygame.key.get_pressed()
        newEffPos=[self.robot.pos[-1][0],self.robot.pos[-1][1]]

        if keys[pygame.K_UP]:
            newEffPos[1]+=0.005
        if keys[pygame.K_DOWN]:
            newEffPos[1]-=0.005
        if keys[pygame.K_RIGHT]:
            newEffPos[0]+=0.005
        if keys[pygame.K_LEFT]:
            newEffPos[0]-=0.005   
        
        angle = 0 # angle de l'effecteur pour calculé le MGI, on mets l'angle courrant du 3eme moteur
        self.robot.q = self.robot.MGI(newEffPos,angle)[0]
        # print(f"MGI q : {self.robot.q}")
        if self.connected:
            for i in range(3):
                self.motors.setMotor(self.robot.q[i], i)

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
                    if pos_target is not None:
                        q_final = self.robot.MGI(pos_target)
                        for i in range(3):
                            error = q_final[i] - self.q[i]
                            max_delta = vitesse_deg_par_s * dt
                            if abs(error) <= max_delta:
                                self.robot.q[i]=q_final[i]
                            else:
                                dx= self.robot.q[i] + max_delta * (1 if error > 0 else -1)
                                # print(i)
                                self.motors.setMotor(dx,i)

                elif mode== "'manipulate":
                    pass
                
                else:
                    if len(self.robot.q)==3:

                        if mode == "posTarget":
                            # Déplacement vers q_target si elle est définie
                            if q_target is not None:
                                for i in range(3):
                                    error = q_target[i] - self.q[i]
                                    max_delta = vitesse_deg_par_s * dt
                                    if abs(error) <= max_delta:
                                        self.robot.q[i] = q_target[i]
                                    else:
                                        dx= self.robot.q[i] + max_delta * (1 if error > 0 else -1)
                                        # print(i)
                                        self.motors.setMotor(dx,i)
                    
                        elif mode == "posTarget2":
                            # Déplacement vers q_target si elle est définie
                            if q_target is not None:
                                for i in range(3):
                                    self.motors.motors[i].set_velocity(30)
                                    self.motors.setMotor(q_target[i],i)

                        elif mode == "jointControl":
                            self.jointSpaceControl()

                        elif mode=="cartesianControl":
                            self.cartesianControl()
                    else:
                        raise ValueError("Mode disponible seulement pour robot 3R")
                    
                for i in range(len(self.robot.q)):
                    self.motors.motors[i].torque_disable()

            else:
                raise "Robot non connecté"
            
            self.robot.MGD()
            self.plotRobot()

        pygame.display.quit()   # ferme la fenêtre
        pygame.quit()  
    
    def simulateVirtualRobot(self,mode, q_target, pos_target, vitesse_deg_par_s):
        """
        Simulation continue du robot. 
        vitesse_deg_par_s : vitesse angulaire de déplacement en degrés/seconde.
        état : non connecté
        mode = q_atrget, pos_target
        """
        import math
        clock = pygame.time.Clock()
        running = True
       

        self.robot.MGD() # Intialise les positions
        while running:
            dt = clock.tick(self.FPS) / 1000.0  # durée en secondes entre les frames

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
      
                    running = False

        
        
            if mode == "qTarget":
                # Déplacement vers q_target si elle est définie
                if q_target is not None:
                    for i in range(len(q_target)):
                        error = q_target[i] - self.robot.q[i]
                        max_delta = vitesse_deg_par_s * dt
                        if abs(error) <= max_delta:
                            self.robot.q[i]=q_target[i]
                        else:
                            self.robot.q[i] += max_delta * (1 if error > 0 else -1)
                                    
            else:
                if len(self.robot.q)==3:
                    if mode=="posTarget":
                        if pos_target is not None:
                            q_final = self.robot.MGI(pos_target)
                            for i in range(3):
                                error = q_final[i] - self.robot.q[i]
                                max_delta = vitesse_deg_par_s * dt
                                if abs(error) <= max_delta:
                                    self.robot.q[i]=q_final[i]
                                else:
                                    self.robot.q[i] += max_delta * (1 if error > 0 else -1)                   
                        
                    elif mode == "jointControl":
                        self.jointSpaceControl()

                    elif mode=="cartesianControl":
                        self.cartesianControl()


                    elif mode =="circle":
                        center = (0.05, 0.05)  # en mètres
                        radius = 0.03
                        self.draw_circle_path_with_effector(center=center, radius=radius)

                        
                else:
                    raise ValueError("Mode disponible seulement pour robot 3R") 

            self.robot.MGD()
            self.plotRobot()

        pygame.display.quit()   # ferme la fenêtre
        pygame.quit()  


    def draw_circle_path_with_effector(self, center, radius, num_points=100, vitesse_deg_par_s=30):
        """
        Fait dessiner un cercle à l'effecteur autour d'un centre donné.
        
        Paramètres :
            - center : tuple (x, y) du centre du cercle (en mètres)
            - radius : rayon du cercle (en mètres)
            - num_points : nombre de points à tracer sur le cercle
            - vitesse_deg_par_s : vitesse de déplacement angulaire des articulations
        """
        import math
        clock = pygame.time.Clock()
        points = [
            (
                center[0] + radius * math.cos(2 * math.pi * i / num_points),
                center[1] + radius * math.sin(2 * math.pi * i / num_points)
            )
            for i in range(num_points)
        ]

        for target_pos in points:
            dt = clock.tick(self.FPS) / 1000.0

            try:
                q_sol = self.robot.MGI(target_pos)[0]
            except:
                print(f"MGI échoué pour le point {target_pos}")
                continue

            for i in range(len(self.robot.q)):
                error = q_sol[i] - self.robot.q[i]
                max_delta = vitesse_deg_par_s * dt
                if abs(error) <= max_delta:
                    self.robot.q[i] = q_sol[i]
                else:
                    self.robot.q[i] += max_delta * (1 if error > 0 else -1)

            if self.connected:
                for i in range(len(self.robot.q)):
                    self.motors.setMotor(self.robot.q[i], i)

            self.robot.MGD()
            self.plotRobot(pos_target=target_pos)


    def run(self,mode, q_target=None, pos_target=None, vitesse_deg_par_s=30):
        
        if self.connected:
            self.simulateRealRobot(mode, q_target, pos_target, vitesse_deg_par_s)
        else:
            self.simulateVirtualRobot(mode, q_target, pos_target, vitesse_deg_par_s)