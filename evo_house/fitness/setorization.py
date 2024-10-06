# Penalidade por setorização

from evo_house.constants import SECTORS
from evo_house.representation import Floor, Room
from evo_house.utils import get_rooms_distance


def sectorial_penalty(floor: Floor, sectors: list[str]):
    def calc_center(room: Room):
        x_c = room.initial_pos[0] + room.width / 2
        y_c = room.initial_pos[1] + room.height / 2
        return (x_c, y_c)

    def calc_square_distance(room1: Room, room2: Room):
        c1 = calc_center(room1)
        c2 = calc_center(room2)
        return (c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2

    penalty = 0
    for sector in sectors:
        room_tags = SECTORS[sector]
        rooms = [room for room in floor.rooms if room.tag in room_tags]
        for i in range(len(rooms) - 1):
            for j in range(i + 1, len(rooms)):
                # print(rooms[i].tag, " | ", rooms[j].tag)
                penalty += get_rooms_distance(rooms[i], rooms[j]) ** 2

    return penalty
