import pygraphviz as pgv
from matplotlib.patches import Polygon, Rectangle
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from evo_house.representation.floor import Floor
from evo_house.utils import get_room_vertices
import numpy as np
from PIL import Image


def render_graph(graph: dict[str, set[str]], file_path: str, prog: str):
    G = pgv.AGraph(directed=False)

    for u, N in graph.items():
        for v in N:
            G.add_edge(u, v)

    # Desenha o grafo e salva como imagem
    G.draw(file_path, prog=prog)


def get_convex_hull(floor: Floor):
    floor_points = []
    for room in floor.rooms + [floor.stairs]:
        room_vertices = get_room_vertices(room)
        floor_points += room_vertices
    floor_points = np.array(floor_points)
    hull = ConvexHull(floor_points)
    hull_points = floor_points[hull.vertices]
    centroid = np.mean(hull_points, axis=0)
    wall_size = 0.01
    return hull_points + wall_size * (hull_points - centroid)


def render_floor(floor: Floor, hull_points, filename: str):
    _, ax = plt.subplots()
    perimeter = Polygon(hull_points, closed=True, fill=False, edgecolor="deeppink")
    ax.add_patch(perimeter)

    def draw_room(ax, x, y, width, height, point1, point2, name, tag):
        rect = Rectangle(
            (x, y), room.width, room.height, fill=None, edgecolor="deeppink"
        )
        ax.add_patch(rect)
        # Define os pontos
        ax.plot(point1[0], point1[1], "yx")  # porta
        ax.plot(
            point2[0], point2[1], "go" if tag != "hall" else "yx"
        )  # janela / porta entrada

        # Calcula o centro do retângulo
        center_x = x + width / 2
        center_y = y + height / 2

        # Adiciona o texto no centro do retângulo
        ax.text(
            center_x,
            center_y,
            f"{name}\n{width*height:.2f}m²",
            fontsize=6,
            ha="center",
            va="center",
        )

    for room in floor.rooms:
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
    floor.stairs.draw(ax)  # type: ignore

    plt.style.use("dark_background")
    plt.gca().set_aspect("equal", adjustable="box")
    ax.set_xlim(-1, 16)
    ax.set_ylim(-1, 11)

    plt.savefig(filename)
    plt.close()


def generate_gif(images_folder: str, last_gen: int, render_filepath: str):
    images = [
        Image.open(f"{images_folder}/gen_{i}.png") for i in range(0, last_gen + 1, 10)
    ]
    images.append(Image.open(f"{images_folder}/gen_{last_gen}.png"))

    for _ in range(15):
        images.append(Image.open(render_filepath))

    images[0].save(
        f"{images_folder}/output.gif",
        save_all=True,
        append_images=images[1:],
        duration=150,
        loop=0,
    )
