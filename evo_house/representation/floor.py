from dataclasses import dataclass, field
from typing import Union

from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from evo_house.constants import HOUSE_WIDTH, HOUSE_HEIGHT
from evo_house.generators import generate_by_tag, generate_stairs
from .stairs import Stairs
from .room import Room


@dataclass
class Floor:
    room_infos: list[tuple[str, int] | str]
    stairs: Stairs | None = None
    rooms: list[Room] = field(default_factory=list)
    min_floor_point: tuple[float, float] = (0, 0)
    max_floor_point: tuple[float, float] = (HOUSE_WIDTH, HOUSE_HEIGHT)

    def __post_init__(self):
        xmin, ymin = self.min_floor_point
        xmax, ymax = self.max_floor_point
        self.room_tags = [
            info[0] if isinstance(info, tuple) else info for info in self.room_infos
        ]
        for info in self.room_infos:
            if isinstance(info, tuple):
                tag, id = info
            else:
                tag, id = info, 0
            self.rooms.append(generate_by_tag(tag, id, xmin, ymin, xmax, ymax))

        self.room_names = [r.name for r in self.rooms]

        # Construção da escada:
        if not self.stairs:
            self.stairs = generate_stairs(xmin, ymin, xmax, ymax, "left")

        self.room_names.append(self.stairs.name)  # type: ignore

    def __getitem__(self, index) -> Union["Floor", Room]:
        if isinstance(index, slice):
            new_floor = Floor(
                self.room_infos[index],
                stairs=self.stairs,
                min_floor_point=self.min_floor_point,
                max_floor_point=self.max_floor_point,
            )
            new_floor.rooms = self.rooms[index]
            return new_floor
        return (self.rooms + [self.stairs])[index]

    def __add__(self, floor) -> "Floor":
        new_floor = Floor(
            self.room_infos + floor.room_infos,
            stairs=self.stairs,
            min_floor_point=self.min_floor_point,
            max_floor_point=self.max_floor_point,
        )
        new_floor.rooms = self.rooms + floor.rooms
        return new_floor

    def __len__(self):
        return len(self.rooms) + 1

    def draw(self, save: bool = False, filename: str = "floor_repr.png"):
        limit_width = self.max_floor_point[0] - self.min_floor_point[0]
        limit_height = self.max_floor_point[1] - self.min_floor_point[1]

        plt.style.use("dark_background")
        _, ax = plt.subplots()
        rectangle = Rectangle(
            self.min_floor_point,
            limit_width,
            limit_height,
            fill=None,
            edgecolor="deeppink",
        )
        ax.add_patch(rectangle)

        def draw_room(ax, x, y, width, height, point1, point2, name, tag):
            rect = Rectangle(
                (x, y), room.width, room.height, fill=None, edgecolor="deeppink"
            )
            ax.add_patch(rect)
            # Definir os pontos
            ax.plot(point1[0], point1[1], "yx")  # porta
            ax.plot(
                point2[0], point2[1], "go" if tag != "hall" else "yx"
            )  # janela / porta entrada

            # Calcular o centro do retângulo
            center_x = x + width / 2
            center_y = y + height / 2

            # Adicionar o texto no centro do retângulo
            ax.text(
                center_x,
                center_y,
                f"{name}\n{width*height:.2f}m²",
                fontsize=6,
                ha="center",
                va="center",
            )

        for room in self.rooms:
            draw_room(
                ax,
                room.initial_pos[0],
                room.initial_pos[1],
                room.width,
                room.height,
                room.door_pos,
                room.window_pos,
                room.name,
                room.tag,
            )

        if isinstance(self.stairs, Stairs):
            self.stairs.draw(ax)

        plt.gca().set_aspect("equal", adjustable="box")
        ax.set_xlim(-1, HOUSE_WIDTH + 1)
        ax.set_ylim(-1, HOUSE_HEIGHT + 1)
        # Exibir a figura
        if not save:
            plt.show()
        else:
            # Salvar figura
            plt.savefig(filename)
            plt.close()
