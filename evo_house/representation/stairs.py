from evo_house.representation.room import Room
from evo_house.constants import STAIRS_HEIGHT, STAIRS_WIDTH
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle


class Stairs(Room):
    def __init__(
        self,
        initial_pos: list[float],
        window_pos: list[float],
        door_pos: list[float],
        opening_sides: list[str],
        fixed: bool = False,
        orientation: str = "left",
    ):
        super().__init__(
            initial_pos,
            STAIRS_WIDTH,
            STAIRS_HEIGHT,
            window_pos,
            door_pos,
            "escada",
            0,
            opening_sides,
        )
        self.fixed = fixed
        self.change_orientation(orientation)

    def change_orientation(self, orientation: str):
        if orientation == "left" or orientation == "right":
            self.width, self.height = STAIRS_WIDTH, STAIRS_HEIGHT
        else:
            self.width, self.height = STAIRS_HEIGHT, STAIRS_WIDTH
        self.orientation = orientation

    def draw(self, ax: Axes):
        # Desenhar o retângulo
        x, y = self.initial_pos
        w, h = self.width, self.height

        top_or_right = self.orientation in ["top", "right"]
        left_or_right = self.orientation in ["left", "right"]

        for i in range(7):
            down_pos = [1 * top_or_right + 0.28 * i, 0]
            up_pos = [1 * top_or_right + 0.28 * i, 1.15]
            step_w = 0.28 if left_or_right else 1
            step_h = 1 if left_or_right else 0.28
            if not left_or_right:
                down_pos = down_pos[::-1]
                up_pos = up_pos[::-1]
            step_down = Rectangle(
                (x + down_pos[0], y + down_pos[1]),
                step_w,
                step_h,
                fill=None,
                edgecolor="yellow",
            )
            step_up = Rectangle(
                (x + up_pos[0], y + up_pos[1]),
                step_w,
                step_h,
                fill=None,
                edgecolor="yellow",
            )
            ax.add_patch(step_down)
            ax.add_patch(step_up)

        landing_pos = [0.28 * 7 * (not top_or_right), 0]
        if not left_or_right:
            landing_pos = landing_pos[::-1]
        landing = Rectangle(
            (x + landing_pos[0], y + landing_pos[1]),
            1 if left_or_right else w,
            h if left_or_right else 1,
            fill=None,
            edgecolor="yellow",
        )
        ax.add_patch(landing)

        # Porta
        ax.plot(*self.door_pos, "rx")
