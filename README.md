# Simulation d'un robot nR plan 

Ce code utilise la programmation orientée objet en Python. Pour faire simple, La POO (programmation orientée objet) en Python permet de structurer le code autour d’objets créés à partir de classes, qui regroupent données (attributs) et comportements (méthodes/fonctions). Une classe se construit avec le mot-clé class, puis on crée des objets (instances) en l’appelant comme une fonction, ce qui rend le code plus organisé, réutilisable et modulable. Le \__init__ est une méthode spéciale appelée automatiquement quand on crée une nouvelle instance d’une classe ; elle sert à initialiser les attributs de l’objet avec les valeurs que tu lui donnes.

### Importation des bibliothèques nécessaires 

```
pip upragde && update 
pip install dynamixel-controller 
pip install pygame 
pip install numpy 
```

### Importation des classes Univers, Robot et Moto via le fichier univers.py

```
from univers import *
```



- **Robot** : permet de créer un robot à *n* articulations rotoïdes dans un plan 2D.  
  La première articulation est fixée au bâti à l'origine, et un effecteur est présent en bout de bras.

- **Motor** : permet d'initialiser les moteurs Dynamixel sur le robot et d'utiliser des fonctions propres à l'utilisation des moteurs à condition que le robot soit bien connecté via USB.

- **Univers** : cette classe permet de gérer les événements Pygame utiles à la simulation du modèle.

Création d'un robot avec n liaisons. Intialisation de q et l (distance entre liaisons)


 # Initialisation
 ```
q_i=[130]*3 # angles initiaux des moteurs (théoriquement entre 0° et 300°)
l_i=[0.06]*3
# Création robot:
robot= Robot(q_i,l_i)
```

Indiquez si oui ou non le roobt est connecté, si il n'est pas connecté seul la simulation se lançera. Le portName est le nom du port USB où le robot est connecté. Suivez les indications suivantes pour le connaitre suivant votre machine.

- **Linux** : `ls /dev/ttyUSB*`  

- **Mac** : `ls /dev/tty.usbserial*` 

- **Windows** : Allez dans votre gestionnaire de périphériques puis dans la section Port (COM et LPT), vous verrez USB Serial Port (COM*). Le numéro COM* sera le nom du port à connaitre.


```
portName='/dev/tty.usbserial-FT6S4E5D'
connected=True 
```

Création d'une instance de la classe Univers

```
univers = Univers(robot=robot,connected=connected,portName=portName) # création d'un univers (instance de Univers)
```

Pour tester le MGD, vous pouvez indiquez au robot une position angulaire en degrès à atteindre. Pour le MGI (marche uniquement pour un robot 3R plan), indiquez une position x,y en mètre à atteindre.


# Test des target pour MGD MGI
```
q_target = [50]*3 # angle cible en degrés
pos_target = [0.1,-0.1] # postion x y cible en mètre
```

Run la simulation

```
# Run simulation, mode = qTarget, posTarget, jointControl, cartesianControl, manipulate (real robot)
univers.simulation(mode="jointControl",q_target=q_target,pos_target=pos_target)
```

### Ressources

- Documentation Pygame : https://www.pygame.org/docs/  
- Dynio pour Dynamixel : https://github.com/kissgyorgy/dynio  
- Flash moteur : https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/
- Théorie robotique plan 3R : consulter les cours de cinématique des robots sériels.
