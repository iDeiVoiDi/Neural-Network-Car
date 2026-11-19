#==================================================
# GUI.SENSORS | Creacion de los objetos de los sensores
#==================================================
import math
import pygame

from config.config import load_config

class Sensor:
    '''
    Objeto → Sensor | Linea q mide distancia coche → pared
    '''
    def __init__(self, offset=0, max_distance=None):
        config = load_config()

        # == Parametros Bases ==
        self.offset = offset
        self.max_distance = max_distance or config["DISTANT_SENSOR"]
        self.distance = self.max_distance
        self.hit = False
        self.start = (0, 0)
        self.end = (0, 0)

    def measure(self, map_surface, x, y, car_angle):
        '''
        Lanza el rayo y guarda la distancia (en pixeles)
        '''
        # == Datos Suyos ==
        angle = math.radians(car_angle + self.offset)
        dx = math.cos(angle)
        dy = -math.sin(angle)
        width, height = map_surface.get_size()
        self.distance = self.max_distance
        self.hit = False

        # == Marca por cada Rayo su Distancia ==
        self.distance = self.max_distance
        for d in range(self.max_distance):
            px = int(x + dx * d)
            py = int(y + dy * d)
            # == Toca un borde ==
            if px < 0 or px >= width or py < 0 or py >= height:
                self.distance = d
                self.hit = True
                break
            # == Toca algo q no es negro (Pared) ==
            if map_surface.get_at((px, py))[:3] != (0, 0, 0):
                self.distance = d
                self.hit = True
                break

        self.start = (x, y)
        self.end = (x + dx * self.distance, y + dy * self.distance)
        return self.distance

    def draw(self, surface):
        pygame.draw.line(surface, (0, 255, 0), self.start, self.end, 2)