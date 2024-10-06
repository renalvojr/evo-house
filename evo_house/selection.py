import random

from evo_house.representation.floor import Floor


def cumsum(probs: list[float]):
    cumulative = []
    total = 0
    for value in probs:
        total += value
        cumulative.append(total)
    return cumulative


def roulette_selection(floors: list[Floor], fitnesses: list[float], qnt: int):
    # inverte fitness
    fitnesses = [1.0 / (f + 1e-6) for f in fitnesses]

    total_fitness = sum(fitnesses)
    probs = [f / total_fitness for f in fitnesses]

    cum_probs = cumsum(probs)

    selected = []

    for _ in range(qnt):
        r = random.random()
        selected_index = next(i for i, prob in enumerate(cum_probs) if prob > r)
        selected.append(floors[selected_index])

    return selected


def k_best_selection(population: list[Floor], fitnesses: list[float], k: int):
    joined = list(zip(population, fitnesses))
    return [crom for crom, _ in sorted(joined, key=lambda x: x[1])[:k]]


def get_best_floor(pop: list[Floor], fitnesses: list[float]):
    joined = list(zip(pop, fitnesses))
    return sorted(joined, key=lambda x: x[1])[0]  # minimização
