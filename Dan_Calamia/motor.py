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
        self.motors.append(dxl_io.new_ax12(13)) # moteur 1  i --> ID des moteurs 1 2 3 
        self.motors.append(dxl_io.new_ax12(6)) # moteur 2    
        self.motors.append(dxl_io.new_ax12(7)) # moteur 3
        # Robot concerné par l'initilisation des moteurs
        self.robot=robot

    def pos_to_deg(self,pos):
        return (pos / 1023.0) * 300.0
    
    def deg_to_pos(self,deg):
        return (deg * 1023.0) / 300.0
    
    def updateMotors(self):
        for i in range(self.nMotors):
            try:
                pos = self.motors[i].get_position() # correspond à la position angulaire des moteurs de 0 à 1024 
                self.robot.q[i] = self.pos_to_deg(pos)
            except:
                print("Erreur de lecture des moteurs")
   
    # def getMotors(self):
    #     q_current=[]
    #     for i in range(self.nMotors):
    #         try:
    #             q_current.append(self.motors[i].get_position())
    #         except:
    #             print("Erreur de lecture des moteurs")
    #     return q_current

    def setMotor(self,q_target,i):
        self.robot.q[i]=q_target # mets à jour le q 
        self.motors[i].set_position(int(self.deg_to_pos(self.robot.q[i]))) # mets à jours les moteurs


