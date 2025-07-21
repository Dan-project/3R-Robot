"""
File: robot3r.py
Author: Dan Calamia and some codes provided by Sylvain Argentieri
Date: 06/2025
Description: Simulation of 3R plan robot.
"""

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
        """
        Par défaut on crée un robot 3R plan. 
        Cependant, cette classe vous permets de choisir le nombre d'articulations sauf le MGI qui est calculé analytiquement pour 3 liaisons. 
        On peut créer un robot nR plan (n>=1).
        """
        # Longueurs des bras
        self.l = l
        # Paramètre articulaires 
        self.q = q  
        # Position des Liaisons (shoulder, elbow, wrist etc si il y a)
        self.pos=[[]]*(len(self.q)+1) # liste de liste de taille len(q) +1 pour l'effecteur

    def matriceRotZ(self, q):
        """
        Donne la matrice de rotation suivant z
        """
        mat =np.array([
            [np.cos(q), -np.sin(q), 0],
            [np.sin(q),  np.cos(q), 0],
            [0,              0,             1]
            ])

        return mat

    def transformationHomogene(self, R, T):
        """
        On vuet une matrice de la forme :
        TH= [ R(3x3) T(1*3)
            0 0 0     1
            ]
        """
        TH= np.eye(4)
        TH[:3, :3] = R
        TH[:3, 3] = T
        return TH

    def MGD(self):
        """
        TH --> Rotation (transformatio, homogène) puis Translation (transformatio, homogène) pour chaque articulations et effecteur
        TH =   [[r11 r12 r13 tx]
                [r21 r22 r23 ty]
                [r31 r32 r33 tz]
                [  0   0   0  1]]

        """
        # Nombre d'articulation ici 3
        nJoint=len(self.q)
        # Initialisation matrice de Transformation Homogène
        TH=np.eye(4) # initialement matrice identité 
        # Initialisation Liste des postions de chaque articulations + effecteur
        
        self.pos[0]=[0.0,0.0] # premier moteur sur la base fixé à l'origine
        # Angle en radians 
        q_radians=[]
        # print(self.q)
        for q in self.q :
            
            q_radians.append(np.radians(150 - q)) # 150 par convention car sur les moteurs Dynamixel la plage d'angle accesible est de 0 à 300
        # Calcul des positons 
        for i in range(nJoint):
            matRZ= self.matriceRotZ(q_radians[i]) # Calcul de la matrice de rotation R
            matTFRot = self.transformationHomogene(matRZ, np.zeros(3))# Calcul pour obtenir la transformation homogène de R
            matTFTrans = self.transformationHomogene(np.eye(3), np.array([self.l[i], 0, 0])) # Calcul pour obtenir la transformation homogène de T
            TH = TH @ matTFRot @ matTFTrans
            self.pos[i+1]= TH[:2,3] # on récupère les positions des articulations ou effecteur pour chaque matrice de transformation homogène, mais que x,y car z vaut toujours 0 dans T.     

    def MGI(self, pos_target, theta):
            """
            Inverse kinematic model for 3 dof planar manipulator
            Returns:
                q1, q2 : two solutions for the angular configurations

            By Sylvain Argentieri
            """
            x=pos_target[0]
            y=pos_target[1]

            if len(self.l) != 3:
                raise ValueError(
                    "mod_geo_inv is only available for a planar 3DOF manipulator.")
            
            # Coordonnées du poignet (centre de la dernière articulation)
            w1 = x - self.l[2] * np.cos(theta)
            w2 = y - self.l[2] * np.sin(theta)
            
            # Résolution pour q2
            cq2 = (w1**2 + w2**2 - self.l[0]**2 - self.l[1]**2) / (2 * self.l[0] * self.l[1])
            
            # Gestion du cas où la cible est hors d'atteinte
            if abs(cq2) > 1.0:
                cq2 = np.sign(cq2)

            sq2_1 = np.sqrt(1 - cq2**2)
            sq2_2 = -sq2_1

            q1 = [0.0, 0.0, 0.0]
            q2 = [0.0, 0.0, 0.0]

            q1[1] = np.arctan2(sq2_1, cq2)
            q2[1] = np.arctan2(sq2_2, cq2)

            # Résolution pour q1
            k1_1 = self.l[0] + self.l[1] * np.cos(q1[1])
            k2_1 = self.l[1] * np.sin(q1[1])
            den1 = k1_1**2 + k2_1**2
            cq1_1 = (w1 * k1_1 + w2 * k2_1) / den1
            sq1_1 = (-w1 * k2_1 + w2 * k1_1) / den1
            q1[0] = np.arctan2(sq1_1, cq1_1)

            k1_2 = self.l[0] + self.l[1] * np.cos(q2[1])
            k2_2 = self.l[1] * np.sin(q2[1])
            den2 = k1_2**2 + k2_2**2
            cq1_2 = (w1 * k1_2 + w2 * k2_2) / den2
            sq1_2 = (-w1 * k2_2 + w2 * k1_2) / den2
            q2[0] = np.arctan2(sq1_2, cq1_2)

            # Résolution pour q3
            q1[2] = theta - q1[0] - q1[1]
            q2[2] = theta - q2[0] - q2[1]

            # On convertit en degrès et on centre autours de 150°
            q1_final=[150-np.degrees(q) for q in q1] 
            q2_final = [150-np.degrees(q) for q in q1]
            
            return q1_final, q2_final
