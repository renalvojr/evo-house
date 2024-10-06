from evo_house.representation.floor import Floor
from .intersection import intersection_penalty
from .circulation import circulation_penalty
from .flow import ground_flow_penalty, first_flow_penalty
from .setorization import sectorial_penalty


def floor_fitness(floor: Floor, sectors: list[str], floor_type: str = "ground"):
    penalty = 0

    ### Interseções
    penalty += intersection_penalty(floor)

    ### Corredores (Circulação)
    penalty += circulation_penalty(floor)

    ### Portas (!)
    if floor_type == "ground":
        penalty += ground_flow_penalty(floor)
    elif floor_type == "first":
        penalty += first_flow_penalty(floor)
    ### Zoneamento
    penalty += sectorial_penalty(floor, sectors=sectors)

    return penalty
