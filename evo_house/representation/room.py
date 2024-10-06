from dataclasses import dataclass


@dataclass
class Room:
    initial_pos: list[float]
    width: float
    height: float
    window_pos: list[float]
    door_pos: list[float]
    tag: str
    id: int
    opening_sides: list[str]

    def __post_init__(self):
        self.area = self.width * self.height
        self.name = f"{self.tag}" + (f" {self.id}" if self.id else "")

    def __repr__(self):
        return f"""<Room {self.name}
    type: {self.tag}
    id: {self.id}
    initial_pos: {self.initial_pos[0] :.2f}, {self.initial_pos[1] :.2f}
    width: {self.width :.2f}
    height: {self.height :.2f}
    door_pos: {self.door_pos[0] :.2f}, {self.door_pos[1] :.2f}
    window_pos: {self.window_pos[0] :.2f}, {self.window_pos[1] :.2f}
    opening_sides: {self.opening_sides}
    area: {self.area :.2f}>
    """
