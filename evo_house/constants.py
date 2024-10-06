HOUSE_WIDTH: int = 15
HOUSE_HEIGHT: int = 10
MAX_RATIO: int = 3
FLOOR_SIZE: int = 7
POPULATION_SIZE: int = 100
STAIRS_WIDTH = 2.96
STAIRS_HEIGHT = 2.15
GROUND_RESULTS_FOLDER = "ground_floor_gens"
FIRST_RESULTS_FOLDER = "first_floor_gens"

ROOM_AREAS: dict[str, list[int]] = {
    "quarto": [12, 20],
    "banheiro": [3, 6],
    "cozinha": [10, 15],
    "ginastica": [10, 20],
    "closet": [3, 4],
    "lavanderia": [6, 10],
    "estar": [15, 20],
    "jantar": [15, 20],
    "hall": [3, 5],
}

GROUND_ROOMS = ["cozinha", "estar", "jantar", "banheiro", "lavanderia", "hall"]
FIRST_ROOMS = [
    ("quarto", 1),
    ("quarto", 2),
    ("banheiro", 1),
    ("banheiro", 2),
    "closet",
    "ginastica",
]
SECTORS: dict[str, list[str]] = {
    "social": ["estar", "jantar", "banheiro"],
    "privativo": ["quarto", "banheiro", "closet"],
    "serviço": ["cozinha", "lavanderia"],
}
