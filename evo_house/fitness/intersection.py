from evo_house.constants import FLOOR_SIZE
from evo_house.representation.floor import Floor
from evo_house.representation.room import Room


def calc_intersect(room1: Room, room2: Room):
    (x_A, y_A), width_A, height_A = room1.initial_pos, room1.width, room1.height
    (x_B, y_B), width_B, height_B = room2.initial_pos, room2.width, room2.height

    # Verificar se há interseção no eixo X
    if max(x_A, x_B) < min(x_A + width_A, x_B + width_B):
        # Verificar se há interseção no eixo Y
        if max(y_A, y_B) < min(y_A + height_A, y_B + height_B):
            # Calcular os limites da interseção
            x_intersec_left = max(x_A, x_B)
            y_intersec_bottom = max(y_A, y_B)
            x_intersec_right = min(x_A + width_A, x_B + width_B)
            y_intersec_top = min(y_A + height_A, y_B + height_B)

            # Calcular largura e altura da interseção
            intersec_width = x_intersec_right - x_intersec_left
            intersec_height = y_intersec_top - y_intersec_bottom

            # Calcular a área da interseção
            intersec_area = intersec_width * intersec_height

            return intersec_area

    return 0


def intersection_penalty(floor: Floor):
    penalty = 0
    for i in range(FLOOR_SIZE - 1):
        for j in range(i + 1, FLOOR_SIZE):
            intersec_area = calc_intersect(floor[i], floor[j])  # type: ignore
            if intersec_area > 0:
                # penalty += intersec_area ** 2
                penalty += 100

    return penalty
