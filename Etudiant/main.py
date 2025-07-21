from univers import *

def main():
    
    # -------- À MODIFIER AU TP2 --------
    connected=False 
    portName='' # string, se référer au README
    
    # -------- À COMPLÉTER AU TP1 --------
    # créer une instance de la classe 'Robot'
    q = ...
    l = ...
    robot= Robot(q,l) 

    # créer une instance de la classe 'Univers'
    univers=Univers(robot,connected,portName)

    # -------- RUN --------
    # utiliser la fonction 'run' de la classe 'Univers'
    mode = '' # mode d'interpolations
    univers.run(mode)
    
if __name__ == "__main__":
    main()
