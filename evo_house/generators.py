from evo_house.constants import (
    HOUSE_WIDTH,
    HOUSE_HEIGHT,
    ROOM_AREAS,
    MAX_RATIO,
    STAIRS_WIDTH,
    STAIRS_HEIGHT,
)
import random

from evo_house.representation import Room, Stairs
from evo_house.utils import (
    get_rect_sides,
    random_point_on_side,
    random_points_on_perimeter,
)


def generate_by_tag(
    tag: str,
    id: int = 0,
    xmin: float = 0,
    ymin: float = 0,
    xmax: float = HOUSE_WIDTH,
    ymax: float = HOUSE_HEIGHT,
):
    area = random.uniform(ROOM_AREAS[tag][0], ROOM_AREAS[tag][1])

    while True:
        # Gerar um fator de proporção aleatório entre 1/r e r/1
        proportion = random.uniform(1 / MAX_RATIO, MAX_RATIO)

        # Calcular width e height com base na área e no fator de proporção
        width = (area * proportion) ** 0.5
        height = area / width

        # Verificar se ambos width e height são maiores que o mínimo
        if width / height <= MAX_RATIO and height / width <= MAX_RATIO:
            if width >= 1.5 and height >= 1.5:
                break

    max_width = abs(xmax - xmin)
    max_height = abs(ymax - ymin)

    x, y = [
        random.uniform(xmin, max_width - width),
        random.uniform(ymin, max_height - height),
    ]

    window_pos, door_pos, opening_sides = random_points_on_perimeter(
        x, y, width, height, (xmin, ymin), (xmax, ymax)
    )

    return Room([x, y], width, height, window_pos, door_pos, tag, id, opening_sides)


def generate_stairs(
    xmin: float = 0,
    ymin: float = 0,
    xmax: float = HOUSE_WIDTH,
    ymax: float = HOUSE_HEIGHT,
    orientation: str = "left",
):
    max_width = abs(xmax - xmin)
    max_height = abs(ymax - ymin)

    left_or_right = orientation in ["left", "right"]
    if left_or_right:
        width, height = STAIRS_WIDTH, STAIRS_HEIGHT
    else:
        width, height = STAIRS_HEIGHT, STAIRS_WIDTH

    x, y = [
        random.uniform(xmin, max_width - width),
        random.uniform(ymin, max_height - height),
    ]

    sides = get_rect_sides(x, y, width, height)
    window_pos, _, opening_sides = random_points_on_perimeter(
        x, y, width, height, (xmin, ymin), (xmax, ymax)
    )
    door_pos = random_point_on_side(sides, orientation)
    opening_sides[1] = orientation

    return Stairs([x, y], window_pos, door_pos, opening_sides, orientation=orientation)
