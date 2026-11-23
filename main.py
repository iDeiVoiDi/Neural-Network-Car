"""
Inicia la interfaz grafica y con ello, el programa

Este programa es una prueba con un simulador hecho en pygame
    la cual por genetica enseña a una red de 7→64→32→1 cruzar por
    un mapa que puede crear cualquier persona, definiendo el color
    negro como carretera y cualquier otro como pared
Utiliza las librerias:
 - numpy para la red y para el mapa
 - pygame para el simulador 
"""

__author__ = "David Turrión"
__version__ = "1.0.0"

from GUI.ui import Game

def main():
    """Inicia y ejecuta la instancia principal del programa"""
    game = Game()
    game.run()

if __name__ == '__main__':
    main()