# Penalidade por Circulação

## Calcula distancia entre laterais de dois comodos
## se nao tiver comodo no caminho
##   se distancia nao é parade nem corredor
##       penaliza
from evo_house.constants import FLOOR_SIZE
from evo_house.representation.floor import Floor
from evo_house.utils import get_rooms_distance, has_room_on_the_way


def circulation_penalty(floor: Floor):
    penalty = 0

    for i in range(FLOOR_SIZE - 1):
        for j in range(i + 1, FLOOR_SIZE):
            distance = get_rooms_distance(floor[i], floor[j])  # type: ignore
            if distance < 0:
                penalty += distance**2
                continue
            if not has_room_on_the_way(floor[i], floor[j], floor.rooms):  # type: ignore
                # não é parede ou corredor
                if not (distance <= 0.6 or 0.8 <= distance <= 1.2):
                    penalty += 50 * distance

    return penalty
