import copy
import random

from evo_house.representation.floor import Floor
from evo_house.representation.room import Room
from evo_house.representation.stairs import Stairs
from evo_house.utils import (
    get_rect_sides,
    get_relative_pos,
    random_point_on_side,
    repair_window,
    set_relative_pos,
)
from evo_house.constants import MAX_RATIO, ROOM_AREAS


def two_points_crossover(floor1: Floor, floor2: Floor):
    floor1 = copy.deepcopy(floor1)
    floor2 = copy.deepcopy(floor2)

    point1 = random.randint(1, len(floor1) - 2)
    point2 = random.randint(point1 + 1, len(floor1))

    child1 = floor1[:point1] + floor2[point1:point2] + floor1[point2:]  # type: ignore
    child2 = floor2[:point1] + floor1[point1:point2] + floor2[point2:]  # type: ignore

    return child1, child2


def room_mutation(
    room: Room | Stairs | None,
    min_floor_point: tuple[float, float],
    max_floor_point: tuple[float, float],
    mutation_rate: float = 1 / 10,
    pos_factor: float = 1 / 50,
    area_factor: float = 1 / 10,
):
    if not room:
        return

    xmin, ymin = min_floor_point
    xmax, ymax = max_floor_point
    max_width = xmax - xmin
    max_height = ymax - ymin

    def change_area(room: Room, new_area: float, proportion: float):
        room.width = (new_area * proportion) ** 0.5
        room.height = new_area / room.width
        room.area = new_area

    def change_position(room: Room, x: float, y: float):
        if isinstance(room, Stairs) and room.fixed:
            return
        x = min(max(xmin, x), max_width - room.width)
        y = min(max(ymin, y), max_height - room.height)
        room.initial_pos = [x, y]

    rel_door = get_relative_pos(
        room.door_pos, room.initial_pos, room.width, room.height
    )
    rel_window = get_relative_pos(
        room.window_pos, room.initial_pos, room.width, room.height
    )

    # muta area
    if random.random() <= mutation_rate and not isinstance(room, Stairs):
        # muta aspect ratio
        if random.random() <= mutation_rate / 2:
            proportion = random.uniform(1 / MAX_RATIO, MAX_RATIO)
        else:
            proportion = room.width / room.height

        area = room.area + random.uniform(-area_factor, area_factor)
        area = min(max(ROOM_AREAS[room.tag][0], area), ROOM_AREAS[room.tag][1])
        change_area(room, area, proportion)

    # muta posicao inicial
    if random.random() <= mutation_rate:
        # print("mutado")
        x, y = room.initial_pos
        x += random.uniform(-pos_factor, pos_factor)
        y += random.uniform(-pos_factor, pos_factor)
        change_position(room, x, y)

    # Caso a mudança de area tenha tirado o comodo da casa:
    change_position(room, *room.initial_pos)

    # repara P e J posicao em relacao ao comodo
    room.door_pos = set_relative_pos(
        room.initial_pos, room.width, room.height, rel_door
    )
    room.window_pos = set_relative_pos(
        room.initial_pos, room.width, room.height, rel_window
    )

    repair_window(
        room, min_floor_point, max_floor_point
    )  # repara a posicao da janela em relacao a casa

    sides = get_rect_sides(*room.initial_pos, room.width, room.height)  # type: ignore
    # muta posicao lateral da porta:
    if random.random() <= mutation_rate and not isinstance(room, Stairs):
        options = [s for s in sides.keys() if s not in room.opening_sides]
        side = random.choice(options)
        room.door_pos = random_point_on_side(sides, side)
        room.opening_sides[1] = side

    # realiza algum deslocamento na porta
    if random.random() <= mutation_rate and not isinstance(room, Stairs):
        room.door_pos = random_point_on_side(sides, room.opening_sides[1])

    # Mutação da escada (rotaciona)
    if random.random() <= mutation_rate and isinstance(room, Stairs) and not room.fixed:
        options = ["left", "right", "top", "bottom"]
        options.remove(room.orientation)
        new_orientation = random.choice(options)
        room.change_orientation(new_orientation)
        sides = get_rect_sides(*room.initial_pos, room.width, room.height)  # type: ignore
        room.door_pos = random_point_on_side(sides, new_orientation)
        room.opening_sides[1] = new_orientation


def floor_mutation(
    floor: Floor,
    mutation_rate: float = 1 / 10,
    pos_factor: float = 1 / 50,
    area_factor: float = 1 / 10,
):
    for room in floor.rooms + [floor.stairs]:
        if random.random() <= mutation_rate:
            room_mutation(
                room,
                floor.min_floor_point,
                floor.max_floor_point,
                mutation_rate,
                pos_factor,
                area_factor,
            )
