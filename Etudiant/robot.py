

# Importation numpy 
import numpy as np

class Robot:
    """
    Classe Robot:
        Paramètres:
            - q : paramètres articulaires
            - l : longueurs des segments en mètres

        Fonctions à implémenter: 
            - fonction qui retourne la matrice de rotation d'un angle suivant l'axe z ('matriceRotZ').
            - fonction qui calcul la matrice de transformation homogène entre une rotation R et translation T ('transformationHomogene')

            - calcul du MGD : mets à jour les positions de chaque articulation et de l'effcteur sur le plan x,y, en fonction des paramètres articulaires courants q.
            - calcul analytique du MGI (valable que pour 3 liaisons rotoides plan) -> retourne deux solutions sous forme d'une liste 2D [a,b]. Prends en paramètres une cible (x,y) à atteindre et un angle fixé de l'effecteur (obligatoire pour trouver une solution)

        
        À NOTER : 
        - Par défaut on crée un robot 3R plan. 
        - Cependant, cette classe vous permets de choisir le nombre d'articulations (robot nR plan (n>=1)) sauf le MGI qui sera calculé analytiquement pour 3 liaisons. 
        - Numpy est importé pour l'utiliser lors de la création de matrice
    """
    

    def __init__(self,q=[0,0,0],l=[0.06,0.06,0.08]):
        # Longueurs des bras
        self.l = l
        # Paramètre articulaires 
        self.q = q  
        # Position des Liaisons (shoulder, elbow, wrist etc si il y a)
        self.pos=[[]]*(len(self.q)+1) # liste de liste de taille len(q) +1 pour l'effecteur

    def matriceRotZ(self, q):
        """
        R(3x3)
        """
        # -------- À COMPLÉTER AU TP1 --------
        pass

    def transformationHomogene(self, R, T):
        """
        TH= [ R(3x3) T(1*3)
            0 0 0     1]
        """
        
        # -------- À COMPLÉTER AU TP1 --------
        pass

        

    def MGD(self):
        """
        TH --> Rotation (transformation homogène) puis Translation (transformation homogène) pour chaque articulation et pour l'effecteur
        TH =   [[r11 r12 r13 tx]
                [r21 r22 r23 ty]
                [r31 r32 r33 tz]
                [  0   0   0  1]]

        """
        # Nombre d'articulation ici 3
        nJoint=len(self.q)
        # Initialisation matrice de Transformation Homogène
        TH=np.eye(4) # initialement matrice identité 
        # Initialisation de la liste des postions de chaque articulations + effecteur
        self.pos[0]=[0.0,0.0] # premier moteur sur la base fixé à l'origine
        # Conversion en radians et centrage
        q_radians=[]
        for q in self.q :
            q_radians.append(np.radians(150 - q)) # 150 par convention car sur les moteurs Dynamixel la plage d'angle accesible est de 0 à 300, donc centré à 150°
        
        # Calcul des positons 
        for i in range(nJoint):
            # -------- À COMPLÉTER AU TP1 --------
            pass

    def MGI(self, pos_target, theta):
            """
            Modèle de cinématique inverse pour un manipulateur planaire à 3 degrés de liberté
            Prends en paramètres une cible (x,y) à atteindre et un angle fixé de l'effecteur (obligatoire pour trouver une solution)
            Retourne :
            q1, q2 : deux solutions possibles pour les configurations angulaires
            """
            # -------- À COMPLÉTER AU TP1 --------
            pass
