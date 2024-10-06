import random
from evo_house.representation.room import Room
from evo_house.representation.stairs import Stairs


def get_rect_sides(x, y, width, height):
    return {
        "bottom": (x, y, x + width, y),
        "right": (
            x + width,
            y,
            x + width,
            y + height,
        ),
        "top": (
            x,
            y + height,
            x + width,
            y + height,
        ),
        "left": (x, y, x, y + height),
    }


def get_rect_side_distances(x, y, width, height, min_floor_point, max_floor_point):
    xmin, ymin = min_floor_point
    xmax, ymax = max_floor_point
    max_width, max_height = xmax - xmin, ymax - ymin
    return {
        "top": max_height - (y + height),
        "bottom": y - ymin,
        "left": x - xmin,
        "right": max_width - (x + width),
    }


def random_point_on_side(sides, side):
    (x1, y1, x2, y2) = sides[side]
    if x1 == x2:  # Vertical side (left or right)
        offset = (y2 - y1) * 0.2
        rand_y = random.uniform(y1 + offset, y2 - offset)
        return [x1, rand_y]
    else:  # Horizontal side (top or bottom)
        offset = (x2 - x1) * 0.2
        rand_x = random.uniform(x1 + offset, x2 - offset)
        return [rand_x, y1]


def random_points_on_perimeter(x, y, width, height, min_floor_point, max_floor_point):
    # Definir os quatro lados do retângulo
    sides = get_rect_sides(x, y, width, height)

    distances = get_rect_side_distances(
        x, y, width, height, min_floor_point, max_floor_point
    )

    sorted_choices = sorted(distances, key=distances.get)  # type: ignore

    # Escolher dois lados aleatórios diferentes
    side1 = sorted_choices[0]  # janela
    side2 = random.choice(sorted_choices[2:])  # porta

    # Gerar os dois pontos
    point1 = random_point_on_side(sides, side1)
    point2 = random_point_on_side(sides, side2)

    return point1, point2, [side1, side2]


##### MUTATION UTILS #####


def get_relative_pos(point, initial_point, width, height):
    x = (point[0] - initial_point[0]) / width
    y = (point[1] - initial_point[1]) / height

    return [x, y]


def set_relative_pos(initial_point, width, height, rel_point):
    x = initial_point[0] + rel_point[0] * width
    y = initial_point[1] + rel_point[1] * height
    return [x, y]


def repair_window(room: Room, min_floor_point, max_floor_point):
    x, y = room.initial_pos
    distances = get_rect_side_distances(
        x, y, room.width, room.height, min_floor_point, max_floor_point
    )

    sorted_choices = sorted(distances, key=distances.get)  # type: ignore

    if sorted_choices[0] == room.opening_sides[0]:
        return

    window_pos, door_pos, opening_sides = random_points_on_perimeter(
        x, y, room.width, room.height, min_floor_point, max_floor_point
    )
    if sorted_choices[0] == room.opening_sides[1]:
        room.door_pos = door_pos
        room.opening_sides[1] = opening_sides[1]

    room.window_pos = window_pos
    room.opening_sides[0] = opening_sides[0]


##### FITNESS UTILS #####


def get_rooms_distance(room1: Room, room2: Room):
    x1_min, y1_min = room1.initial_pos
    x1_max, y1_max = x1_min + room1.width, y1_min + room1.height

    x2_min, y2_min = room2.initial_pos
    x2_max, y2_max = x2_min + room2.width, y2_min + room2.height

    horizontal_dis = max(x2_min - x1_max, x1_min - x2_max)
    vertical_dis = max(y2_min - y1_max, y1_min - y2_max)

    return max(horizontal_dis, vertical_dis)


def has_room_on_the_way(room1: Room, room2: Room, rooms: list[Room]):
    x1, y1 = room1.initial_pos
    x2, y2 = room2.initial_pos
    x_min = min(x1 + room1.width, x2 + room2.width)
    x_max = max(x1, x2)
    y_min = min(y1 + room1.height, y2 + room2.height)
    y_max = max(y1, y2)

    for room in rooms:
        if room == room1 or room == room2:
            continue

        x, y = room.initial_pos
        if not (
            x + room.width < x_min or x > x_max or y + room.height < y_min or y > y_max
        ):
            # print(room.tag)
            return True
    return False


##### RENDERIZATION UTILS #####


def get_room_vertices(room: Room | Stairs | None):
    if not room:
        return []
    x, y = room.initial_pos
    w, h = room.width, room.height
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
