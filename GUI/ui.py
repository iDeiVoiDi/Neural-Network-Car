#==================================================
# GUI.UI | Codigo principal donde funciona el juego
#==================================================
from pathlib import Path
import pygame

from config.config import load_config
from GUI.car import Car
from GUI.sensors import Sensor

class Game:
    '''
    Pantalla principal del juego
    '''
    def __init__(self):
        config = load_config()

        # == Parametros base ==
        pygame.init()
        pygame.display.set_caption(config["NAME"])
        width = config["SCREEN_WIDTH"]
        height = config["SCREEN_HEIGHT"]
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False


    def run(self):
        ''''
        Corre la imagen principal del juego
        '''
        image_path = Path(__file__).resolve().parent.parent / "assets" / "car.png"
        config = load_config()
        ppu = 32

        # == Creacion del Objeto Coche ==
        car = Car(x=config["SCREEN_CAR_INIT_X"], 
                  y=config["SCREEN_CAR_INIT_Y"], 
                  image_path=image_path)

        #! == Mapa provisional (negro = carretera, rojo = pared) ==
        map_surface = pygame.Surface(self.screen.get_size())
        map_surface.fill((0, 0, 0))
        pygame.draw.rect(map_surface, (255, 0, 0), (800, 0, 480, 720))

        # == Sensores: 7 rayos en abanico ==
        sensors = [Sensor(offset) for offset in (-90, -60, -30, 0, 30, 60, 90)]

        # == Bucle Principal | (Imagen) ==
        while not self.exit:
            dt = self.clock.get_time() / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            pressed = pygame.key.get_pressed()

            # == Teclas ==
            accelerate = pressed[pygame.K_UP]
            reverse = pressed[pygame.K_DOWN]
            
            turn_dir = 0
            if pressed[pygame.K_LEFT]:
                turn_dir += 1
            if pressed[pygame.K_RIGHT]:
                turn_dir -= 1

            # == Actualizacion del Coche ==
            car.update(dt, accelerate, reverse, turn_dir)
            
            # == Medicion de sensores ==
            car_px = car.position * ppu
            for s in sensors:
                s.measure(map_surface, car_px.x, car_px.y, car.angle)

            # == Dibujado en pantalla ==
            self.screen.blit(map_surface, (0, 0))
            for s in sensors:
                s.draw(self.screen)
            car.draw(self.screen, ppu)
            pygame.display.flip()

            self.clock.tick(self.ticks)

        pygame.quit()