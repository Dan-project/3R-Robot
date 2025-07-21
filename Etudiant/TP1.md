# Séance 1
## Modélisation et commande géométrique d’un robot sériel nR

### UE : L3 Elec/Méca – LU3MEE01  
**Introduction à la Robotique**

> *Pour rappel, et comme indiqué dans l'introduction, les questions repérées par un encadré gris sont celles pour lesquelles il est demandé une réponse détaillée et argumentée dans votre compte-rendu final.*

## Considérations préliminaires

Où on vous explique un peu ce que vous devez faire par la suite.

### Objet de la séance de TP

Ce TP a pour objet le développement d'outils de calcul des modèles géométrique direct et inverse pour un robot 3R plan. Ces outils prennent la forme de fonctions Python, qui permettent de calculer les transformations entres les coordonnées articulaires (les angles aux articulations) et opérationelles (la position et l'orientation de l'outil terminal).

Hormis le modèle géométrique inverse pour lequel il est impossible de trouver une solution analytique générale pour tout robot, les fonctions développées ont une portée plus large que le simple 3R plan et peuvent être utilisées pour tout robot sériel plan à n degrés de liberté de type rotoïde. (L'extension au cas prismatique serait une formalité mais, dans les séances de TP suivantes, seuls de robots à liaisons rotoïdes pourront être construits.)

En 2nde partie de TP, ces fonctions sont utilisées pour mettre en œuvre des techniques d'interpolation géométrique simples mais dont les concepts associés sont fondamentaux en Robotique.

### Modèle géométrique direct

Le modèle géométrique direct (MGD) permet de connaître la pose (position et orientation) du repère R_OT associé à l'organe terminal d'un robot et exprimé dans un repère de référence R_0 en fonction des paramètres géométriques constants et variables (degrés de liberté) du système.

Dans le cas d'un système constitué de solides rigides, cette pose peut être calculée à partir des transformations homogènes successives permettant de passer du repère associé à l'organe terminal à des repères intermédiaires et finalement au repère de référence.

Un choix judicieux du repérage intermédiaire facilite grandement la description des calculs à mettre en œuvre afin d'obtenir le MGD. Nous proposons ici l'utilisation d'une convention dédiée au robots nR plans et donc plus simple d'interprétation, comme il a été vu en TD 1.2.

### Convention de repérage

Étant donnés deux corps successifs i-1 et i et la liaison rotoïde i entre ces deux corps, les repères intermédiaires d'intérêts retenus pour ce TP sont décrits par une figure (voir figure `robot_nRplan.pdf`). Par convention, l'axe de la liaison i est porté par l'axe z_{i-1} et le centre O_i du repère R_i est placé à l'extrémité du corps i.

La transformation homogène permettant d'exprimer les coordonnées d'un point P dans le repère R_{i-1} à partir de ses coordonnées dans le repère R'_i (la transformation R_{i-1} → R'_i) est une rotation pure d'axe z_{i-1} et d'angle q_i. Cette première transformation permet de tenir compte du degré de liberté en rotation associé à la ième liaison.

Elle s’écrit :

    H_{R_{i-1} → R'_i} = [ Rz(q_i)       | 0 ]
                         [ 0             | 1 ]

où Rz(q) est la matrice de rotation 3x3 correspondant à une rotation d'angle q autour du vecteur z. 0 indique une ligne ou colonne de zéros. Donc la matrice H est de dimension 4x4.

La transformation homogène permettant d'exprimer les coordonnées d'un point P dans le repère R'_i à partir de ses coordonnées dans le repère R_i est une translation pure (la transformation R'_i → R_i). Cette seconde transformation permet de tenir compte de la translation O_{i-1}O_i qui correspond donc à la longueur du segment l_i.

Elle s’écrit :

    H_{R'_i → R_i} = [ I3      | T ]
                     [ 0       | 1 ]

Finalement, la transformation homogène H_{i-1 → i} s’écrit comme la multiplication des deux matrices précédentes :

    H_{R_{i-1} → R_i} = H_{R_{i-1} → R'_i} × H_{R'_i → R_i}


# Modélisation

## Préparation

L'ensemble des TPs s'appuient sur le code fourni au sein du fichier `robot3rPlan` qui utilise la programmation orientée objet avec Python. Ce fichier contient tous les éléments nécessaires pour modéliser un robot 3R plan, l'affichage avec Pygame, mais également communiquer avec la maquette du robot réel que vous utiliserez dans les séances suivantes.

Voici une explication rapide des trois classes (seule la classe `Robot` sera à compléter) :

- **Classe `Robot`**  
  Permet de créer un robot en associant les paramètres articulaires initiaux et la taille des segments du robot. Votre travail sera de compléter cette classe, qui doit contenir toutes les fonctions de modélisation du robot.

- **Classe `Univers`**  
  Permet de simuler un robot plan à *n* articulations (notamment un robot 3R) avec visualisation Pygame. Elle offre des modes de contrôle articulaires et cartésiens, ainsi qu'une interface optionnelle avec des moteurs réels via une connexion série. Elle gère l'affichage, les interactions clavier et le pilotage en temps réel.

- **Classe `Motor`**  
  Permet d’initialiser et de contrôler des moteurs Dynamixel AX-12 pour un robot articulé. Elle gère la conversion entre positions en degrés et valeurs brutes des moteurs, la lecture de l’état des moteurs, et l’envoi de commandes de position.

---

## Construction et affichage d'un robot 3R plan

Dans le dossier où se situent les fichiers téléchargés précédemment, ouvrir le fichier `main.py`.

1. Créer une instance de la classe `Robot` avec comme configuration articulaire :  
  \[
  \left[\frac{\pi}{2},~0,~0\right]^T
  \]  
  et des segments respectivement de longueurs 0.5 m, 0.3 m et 0.2 m.

2. Afficher le robot et vérifier graphiquement que la position et l'orientation de l’organe terminal correspondent bien à celles attendues pour la configuration choisie.

---

## Construction des modèles géométriques

Fonctions à compléter dans la classe `Robot`.

1. Écrire une fonction `matriceRotZ` qui retourne une matrice de rotation autour de l’axe Z pour un angle `a` donné.

2. Écrire une fonction `transformationHomogene` qui retourne une matrice de transformation homogène correspondant à une rotation `R` suivie d’une translation `T`, toutes deux passées en paramètre.

  Ces transformations peuvent être obtenues de manière itérative en partant du repère de référence \(\mathcal{R}_{0}\), en utilisant les compositions de transformations homogènes vues en cours et dans le TD1.

> 3. Créer la fonction `MGD` qui permets de calculer les positions des articulations (x,y) en fonctions des paramètres articulaires.

> 4. Tester votre fonction `MGD` dans trois configurations articulaires simples, où la solution peut se calculer facilement à la main.

> 5. Dans le cas particulier du robot 3R plan, écrire une fonction `MGI` qui retourne les configurations du robot correspondant à une position cartésienne \((x, y)\) et à une orientation \(\theta\) dans le plan.

6. Utiliser maintenant la fonction pour déterminer les configurations articulaires nécessaires à l’atteinte d’une cible opérationnelle (simple ou non). Vérifier ensuite que l’utilisation du modèle direct permet bien d’atteindre cette cible.  
  *Existe-t-il une seule solution ?*

7. Utiliser le modèle inverse pour déterminer les configurations articulaires permettant d'atteindre la position \([1.0,~1.0]^T\) et l'orientation \(\frac{3\pi}{2}\). Tester ensuite la configuration obtenue via le modèle direct.  
  *Que peut-on dire de la solution obtenue avec le modèle inverse ?*

---

# Simulation : Génération de trajectoires par interpolation

En pratique, lorsqu'une application robotique nécessite de placer l'organe terminal en une position opérationnelle particulière (par exemple pour récupérer une pièce), il faut générer une trajectoire pour chaque moteur, c’est-à-dire une suite de configurations articulaires que le robot doit suivre dans le temps.

Cette suite est déterminée par interpolation, effectuée :
- soit dans l’espace **articulaire** ;
- soit dans l’espace **opérationnel**.

Fonction `simulateVirtualRobot` à compléter dans la classe `Univers`.

---

## Interpolation articulaire


  1. Étant donnée une configuration articulaire de départ quelconque et une cible opérationnelle (position et orientation dans le plan), écrire dans le script principal les instructions permettant de rejoindre la cible en interpolant sur \(N\) positions articulaires intermédiaires.

  Proposer un critère simple pour choisir entre les deux solutions \(A\) et \(B\) du modèle géométrique inverse.

    2. Quels sont les avantages et inconvénients de cette méthode d’interpolation ?

---

## Interpolation opérationnelle

1. Étant donnée une configuration articulaire de départ quelconque et une cible opérationnelle (position et orientation dans le plan), écrire les instructions permettant de rejoindre la cible en interpolant sur 100 configurations intermédiaires **dans l’espace opérationnel**.

2. Quels sont les avantages et inconvénients de cette méthode ?

