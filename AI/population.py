import numpy as np
import copy

from AI.brain import Brain


PARAMETERS = ["W1", "b1", "W2", "b2", "W3", "b3"]


def crossover(parent_a, parent_b):
    child = Brain()

    for name in PARAMETERS:
        a = getattr(parent_a, name)
        b = getattr(parent_b, name)

        # Cada elemento hereda de uno de los padres
        mask = np.random.random(a.shape) < 0.5

        inherited = np.where(mask, a, b)

        setattr(child, name, inherited.astype(np.float32))

    return child


def mutate(brain, rate=0.05, strength=0.1):

    for name in PARAMETERS:
        weights = getattr(brain, name)

        # Elegir qué valores mutan
        mask = np.random.random(weights.shape) < rate

        # Añadir variaciones aleatorias
        changes = np.random.randn(*weights.shape) * strength

        weights += (mask * changes).astype(np.float32)

    return brain


def evolve(brains, fitnesses, n_elite=4, rate=0.05, strength=0.1):
    order = np.argsort(fitnesses)[::-1]              # de mejor a peor
    ranked = [brains[i] for i in order]
    n = len(brains)

    new = [copy.deepcopy(b) for b in ranked[:n_elite]]   # élite, sin tocar
    parents = ranked[:max(2, n // 4)]                    # el 25% mejor se reproduce

    while len(new) < n:
        i, j = np.random.choice(len(parents), 2, replace=False)
        child = crossover(parents[i], parents[j])
        new.append(mutate(child, rate, strength))
    return new