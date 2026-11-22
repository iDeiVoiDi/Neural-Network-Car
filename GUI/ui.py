#==================================================
# GUI.UI | Codigo principal donde funciona el juego
#==================================================
from pathlib import Path
import pygame

from config.config import load_config
from GUI.car import Car
from GUI.map_loader import load_walls
from AI.brain import Brain
from AI.population import evolve


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
        '''
        Corre la simulacion: poblacion de coches evolucionando
        '''
        config = load_config()
        ppu = 32

        # == Parametros del entrenamiento ==
        POP = 50
        DT = 1 / 60
        MAX_FRAMES = 60 * 20          # una generacion dura como mucho 20 s
        steps_per_frame = 1           # velocidad de simulacion (flechas arriba/abajo)
        draw_enabled = True           # tecla D para apagar/encender el dibujo
        x0, y0 = config["SCREEN_CAR_INIT_X"], config["SCREEN_CAR_INIT_Y"]
        car_angle = config["CAR_INIT_ANGLE"]

        # == Cargamos imagenes y mapa ==
        image_path = Path(__file__).resolve().parent.parent / "assets" / "car.png"
        map_path = Path(__file__).resolve().parent.parent / "assets" / "map.png"
        size = (config["SCREEN_WIDTH"], config["SCREEN_HEIGHT"])

        walls = load_walls(map_path, size)
        map_surface = pygame.transform.scale(
            pygame.image.load(map_path).convert(), size)

        # == Poblacion inicial (coches creados UNA vez, luego se reutilizan) ==
        cars = [Car(x0, y0, angle=car_angle, image_path=image_path) for _ in range(POP)]
        for car in cars:
            car.reset(x0, y0, car_angle, Brain())

        generation, frames = 1, 0
        best_ever = 0.0
        font = pygame.font.SysFont(None, 24)

        # == Bucle Principal ==
        while not self.exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        steps_per_frame = min(steps_per_frame + 1, 30)
                    elif event.key == pygame.K_DOWN:
                        steps_per_frame = max(steps_per_frame - 1, 1)
                    elif event.key == pygame.K_d:
                        draw_enabled = not draw_enabled

            # == Simulacion (uno o varios pasos por fotograma) ==
            for _ in range(steps_per_frame):
                for car in cars:
                    car.think_and_move(DT, walls, ppu)
                frames += 1

                # == Fin de generacion: todos muertos o se acabo el tiempo ==
                if frames >= MAX_FRAMES or not any(c.alive for c in cars):
                    best = max(cars, key=lambda c: c.fitness)
                    print(f"Gen {generation}: mejor = {best.fitness:.1f}")

                    if best.fitness > best_ever:
                        best_ever = best.fitness
                        best.brain.save("best_brain.npz")

                    new_brains = evolve([c.brain for c in cars],
                                        [c.fitness for c in cars])
                    for car, brain in zip(cars, new_brains):
                        car.reset(x0, y0, car_angle, brain)
                    generation += 1
                    frames = 0

            alive = [c for c in cars if c.alive]
            pygame.display.set_caption(
                f"Gen {generation} | vivos {len(alive)} | x{steps_per_frame}")

            # == Dibujado ==
            if draw_enabled:
                self.screen.blit(map_surface, (0, 0))
                if alive:
                    leader = max(alive, key=lambda c: c.fitness)
                    for s in leader.sensors:      # sensores solo del mejor
                        s.draw(self.screen)
                    for car in alive:
                        car.draw(self.screen, ppu)
                hud = font.render(
                    f"Gen {generation}  vivos {len(alive)}  mejor historico {best_ever:.0f}",
                    True, (255, 255, 255))
                self.screen.blit(hud, (10, 10))
                pygame.display.flip()
                self.clock.tick(self.ticks)

        pygame.quit()