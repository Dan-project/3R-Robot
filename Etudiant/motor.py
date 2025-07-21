# Importation dynamixel-controller
from dynio import *  
from robot import *

class Motor:
    """
    Classe Motor:
        Paramètres:
            - robot (instance de Robot)
            - nMotors (nombre de moteurs à initialiser, ici toujours 3)
            - portName (nom du port usb à renseigner dans le main)
            - self.motors -> listes des moteurs ax12 initialisés

        Fonctions à implémenter: 
            - fonctions de conversions degrès à postions et positions à degrès ('pos_to_deg' et 'deg_to_pos')
            - fonction d'actualisations depuis les moteurs pour mettre à jour les paramètres articulaires depuis les moteurs ('updateMotors'). Utile pour connaitre les postions intiales.
            - fonction  d'actualisations d'un moteur depuis un angle (prends en paramètre un angle et l'ID moteur 1,2 ou 3).

        Fonctions de la bibliothèque à utiliser: ( exemple avec motor = dxl_io.new_ax12(1), ID = 1 )
            - motor.set_position(x) avec x étant un entier et appertant à [0,1023]
            - motor.get_position() retourne un la position du moteur, valeur entre  [0,1023]
        
        À NOTER : les paramètres articulaires q de la classe Robot sont utilisés en degrès. De plus, les moteurs ax12 sont exploitables en degrès entre [0,300]°.

    """  
    def __init__(self,robot,nMotors,portName):
        # nombres de moteurs : 3
        self.nMotors=nMotors
        
        try:
            # Initialisaion du port usb
            self.portname= portName 
            # Initialisation des moteurs
            dxl_io = dxl.DynamixelIO(self.portname, baud_rate=1000000) #baud_rate --> vitesse de communication

        except:
            raise NameError("Port USB introuvable")
        
        # Liste des moteurs 
        self.motors=[]
        self.motors.append(dxl_io.new_ax12(1)) # moteur 1  i --> ID des moteurs 1 2 3 
        self.motors.append(dxl_io.new_ax12(2)) # moteur 2    
        self.motors.append(dxl_io.new_ax12(3)) # moteur 3

        # Robot concerné par l'initilisation des moteurs
        self.robot=robot

    def pos_to_deg(self,pos):
        # -------- À COMPLÉTER AU TP2 --------
        pass
    
    def deg_to_pos(self,deg):
        # -------- À COMPLÉTER AU TP2 --------
        pass
    
    def updateMotors(self):
        # -------- À COMPLÉTER AU TP2 --------
        pass
   
    def setMotor(self,q_target,i):
        # -------- À COMPLÉTER AU TP2 --------
        pass
