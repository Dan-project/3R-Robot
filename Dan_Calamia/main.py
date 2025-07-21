from univers import *

def main():
    
    # Initialisation
    q_i=[130]*3 # angles initiaux des moteurs (réel entre 0° et 300°)
    l_i=[0.06]*3
    # Création robot:
    robot3R= Robot(q_i,l_i)
    portName='/dev/tty.usbserial-FT6S4F81'
    connected=True
    univers = Univers(robot=robot3R,connected=connected,portName=portName) # création d'un univers (instance de Univers)
    
    # Test des target pour MGD MGI
    q_target = [50]*3 # angle cible en degrés
    pos_target = [0.1,-0.1] # postion x y cible en mètre
    
    # Run simulation, mode = qTarget, posTarget, jointControl, cartesianControl, manipulate (real robot)
    univers.run(mode="cartesianControl",q_target=q_target,pos_target=pos_target)
    
if __name__ == "__main__":
    main()
