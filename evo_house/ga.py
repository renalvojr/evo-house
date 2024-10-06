import shutil
from evo_house.fitness import (
    floor_fitness,
    intersection_penalty,
    circulation_penalty,
    sectorial_penalty,
    ground_flow_penalty,
    first_flow_penalty,
)
from evo_house.representation import Floor, Stairs
from evo_house.selection import get_best_floor, roulette_selection
from evo_house.operators import two_points_crossover, floor_mutation
import numpy as np
import os
from tqdm import tqdm


def floor_GA(
    pop_size: int,
    room_tags: list[tuple[str, int] | str],
    stairs: Stairs | None,
    generations: int,
    mutation_rate: float,
    sectors: list[str],
    floor_type: str,
    folder_name: str,
):
    pop = [Floor(room_tags, stairs=stairs) for _ in range(pop_size)]
    fitnesses = [
        floor_fitness(floor, sectors=sectors, floor_type=floor_type) for floor in pop
    ]

    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    else:
        if os.path.isdir(folder_name):
            shutil.rmtree(folder_name)
            os.mkdir(folder_name)

    best_floor, best_fitness = get_best_floor(pop, fitnesses)
    tqdm.write(f"População inicial | {best_fitness = :.2f}\n")
    best_floor.draw(save=True, filename=f"{folder_name}/gen_0.png")
    gen_idx = 1
    mr = mutation_rate
    pos_factor = 1 / 50
    area_factor = 1 / 10
    best_fitnesses = []
    diversity = 50
    elite_size = round(pop_size * 0.10)
    for gen_idx in tqdm(range(1, generations + 1), desc="Evoluindo"):
        sorted_pop = sorted(zip(pop, fitnesses), key=lambda x: x[1])
        elites = [floor for floor, _ in sorted_pop[:elite_size]]

        new_pop = []
        for _ in range((pop_size - elite_size) // 2):
            floor1, floor2 = roulette_selection(pop, fitnesses, 2)
            child1, child2 = two_points_crossover(floor1, floor2)
            floor_mutation(child1, mr, pos_factor, area_factor)
            floor_mutation(child2, mr, pos_factor, area_factor)
            new_pop.extend([child1, child2])

        pop = elites + new_pop
        fitnesses = [
            floor_fitness(floor, sectors=sectors, floor_type=floor_type)
            for floor in pop
        ]

        best_floor, best_fitness = get_best_floor(pop, fitnesses)
        best_fitnesses.append(best_fitness)
        if gen_idx % 10 == 0:
            best_floor.draw(save=True, filename=f"{folder_name}/gen_{gen_idx}.png")
        if gen_idx % 20 == 0:
            tqdm.write(f"Gen: {gen_idx} | {best_fitness = :.2f}")

            ip = intersection_penalty(best_floor)
            sp = sectorial_penalty(best_floor, sectors=sectors)
            cp = circulation_penalty(best_floor)

            if floor_type == "ground":
                fp = ground_flow_penalty(best_floor)
            else:
                fp = first_flow_penalty(best_floor)

            change_factor = 130 / (ip + sp)
            if ip >= 100 or sp >= 30 or fp > 0:
                pos_factor = min(pos_factor + change_factor, 5)
                area_factor = min(area_factor + (change_factor / 1.5), 5)
            else:
                pos_factor = max(pos_factor - change_factor, 1 / 50)
                area_factor = max(area_factor - (change_factor / 1.5), 1 / 10)

            tqdm.write(f"interseção: {ip :.2f}")
            tqdm.write(f"setorização: {sp :.2f}")
            tqdm.write(f"circulação: {cp :.2f}")
            tqdm.write(f"fluxo: {fp :.2f}")
            tqdm.write(f"{pos_factor = :.2f} | {area_factor = :.2f}")
            tqdm.write(f"std: {np.std(best_fitnesses):.2f} | mutation: {mr:.2f}\n")

            if ip >= 100 or sp >= 30 or fp > 0:
                diversity = np.std(best_fitnesses)
            else:
                diversity = 50
            best_fitnesses = []
            best_floor.draw(save=True, filename=f"{folder_name}/gen_{gen_idx}.png")
        gen_idx += 1

        if diversity < 10:
            mr = min(mr + 0.01, mutation_rate)
        else:
            mr = max(mutation_rate * (1 - gen_idx / generations), 0.1)

        if best_fitness < 25:
            break

    if gen_idx <= generations:
        best_floor, best_fitness = get_best_floor(pop, fitnesses)
        tqdm.write(f"Encontrado!!! Gen: {gen_idx} | {best_fitness = :.2f}\n")
        best_floor.draw(save=True, filename=f"{folder_name}/gen_{gen_idx}.png")

    return best_floor, best_fitness
