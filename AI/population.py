#==================================================
# AI.POPULATION | Gentica, poblacion y seleccion
#==================================================
import numpy as np
import copy

from AI.brain import Brain

PARAMETERS = ["W1", "b1", "W2", "b2", "W3", "b3"]

def crossover(parent_a, parent_b):
    '''
    Mezcla la red neuronal de los padres
    '''
    child = Brain()

    # == Parametros por lo q pasa ==
    for name in PARAMETERS:
        a = getattr(parent_a, name)
        b = getattr(parent_b, name)

        # == Seleccion de elementos
        mask = np.random.random(a.shape) < 0.5

        inherited = np.where(mask, a, b)

        setattr(child, name, inherited.astype(np.float32))

    return child


def mutate(brain, rate=0.05, strength=0.1):
    '''
    Muta la red neuronal por cada parametro
    '''
    for name in PARAMETERS:
        weights = getattr(brain, name)

        # == Seleccion de los valores ==
        mask = np.random.random(weights.shape) < rate

        # == Añadido aleatorio ==
        changes = np.random.randn(*weights.shape) * strength

        weights += (mask * changes).astype(np.float32)

    return brain


def evolve(brains, fitnesses, n_elite=4, rate=0.05, strength=0.1):
    '''
    Da paso a la nueva generacion, mezcla genes y los muta
    '''
    order = np.argsort(fitnesses)[::-1]
    ranked = [brains[i] for i in order]
    n = len(brains)

    new = [copy.deepcopy(b) for b in ranked[:n_elite]]   # → Mejor sin tocar
    parents = ranked[:max(2, n // 4)]                    # → 25% se reproduce

    while len(new) < n:
        i, j = np.random.choice(len(parents), 2, replace=False)
        child = crossover(parents[i], parents[j])
        new.append(mutate(child, rate, strength))
    return new