import copy
from evo_house.ga import floor_GA
from evo_house.constants import (
    FIRST_ROOMS,
    GROUND_ROOMS,
    GROUND_RESULTS_FOLDER,
    FIRST_RESULTS_FOLDER,
)
from evo_house.graph import create_graph
from evo_house.render import generate_gif, render_floor, render_graph, get_convex_hull


def generate_house():
    try_again = True
    generations = int(input("Digite a quantidade de gerações: "))

    while try_again:
        print("\n\033[36m######## GERAÇÃO DO ANDAR TÉRREO ########\033[0m\n")
        best_ground_floor, _, ggen_idx = floor_GA(
            1000,
            GROUND_ROOMS,  # type: ignore
            None,
            generations,
            0.6,
            ["social", "serviço"],
            "ground",
            GROUND_RESULTS_FOLDER,
        )

        print(f"\nResultado salvos na pasta: {GROUND_RESULTS_FOLDER}")
        ask = input("Gostaria de tentar novamente? (y/n) ")
        if ask[0].lower() != "y":
            try_again = False

    ground_graph = create_graph(best_ground_floor)  # type: ignore
    render_graph(ground_graph, "ground_floor_graph.png", prog="dot")
    render_floor(
        best_ground_floor,  # type: ignore
        get_convex_hull(best_ground_floor),  # type: ignore
        "ground_floor_blueprint.png",
    )
    generate_gif(GROUND_RESULTS_FOLDER, ggen_idx, "ground_floor_blueprint.png")  # type: ignore

    try_again = True
    ### Fixa escada
    fixed_stairs = copy.deepcopy(best_ground_floor.stairs)  # type: ignore
    fixed_stairs.fixed = True  # type: ignore

    while try_again:
        print("\033[36m######## GERAÇÃO DO PRIMEIRO ANDAR ########\033[0m")
        best_first_floor, _, fgen_idx = floor_GA(
            1000,
            FIRST_ROOMS,
            fixed_stairs,
            generations,
            0.6,
            ["privativo"],
            "first",
            FIRST_RESULTS_FOLDER,
        )

        print(f"\nResultado salvos na pasta: {FIRST_RESULTS_FOLDER}")
        ask = input("Gostaria de tentar novamente? (y/n) ")
        if ask[0].lower() != "y":
            try_again = False

    first_graph = create_graph(best_first_floor)  # type: ignore
    render_graph(first_graph, "first_floor_graph.png", prog="dot")
    render_floor(
        best_first_floor,  # type: ignore
        get_convex_hull(best_first_floor),  # type: ignore
        "first_floor_blueprint.png",
    )

    generate_gif(FIRST_RESULTS_FOLDER, fgen_idx, "first_floor_blueprint.png")  # type: ignore


if __name__ == "__main__":
    generate_house()
