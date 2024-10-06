from evo_house.graph import create_graph, is_connected
from evo_house.representation import Floor


def ground_flow_penalty(floor: Floor):
    penalty = 0
    graph = create_graph(floor)
    # Verifica se é conexo
    if not is_connected(graph):
        penalty += 50

    # Verifica se nao ha presença de None
    if "None" in graph.keys():
        penalty += 50

    # Verifica sequencia de comodos validos
    # jantar e lavanderia sao vizinhos de cozinha
    n_cozinha = graph["cozinha"]
    penalty += 12.5 * (("jantar" not in n_cozinha) + ("lavanderia" not in n_cozinha))

    # banheiro e jantar associado a estar
    n_estar = graph["estar"]
    penalty += 12.5 * (("jantar" not in n_estar) + ("banheiro" not in n_estar))

    # estar ou jantar é vizinho de hall
    n_hall = graph["hall"]
    if not ("estar" in n_hall or "jantar" in n_hall):
        penalty += 50

    return penalty


# Penalidade por fluxo das portas no 1º andar
def first_flow_penalty(floor: Floor):
    penalty = 0
    graph = create_graph(floor)
    # Verifica se é conexo
    if not is_connected(graph):
        penalty += 50

    # Verifica se nao ha presença de None
    if "None" in graph.keys():
        penalty += 50

    # Conexões da sala de ginastica
    n_ginastica = graph["ginastica"]
    penalty += 12.5 * (
        ("quarto 1" not in n_ginastica) + ("quarto 2" not in n_ginastica)
    )

    # Conexões closet
    n_closet = graph["closet"]
    penalty += 12.5 * (("quarto 1" not in n_closet) + ("quarto 2" not in n_closet))

    # Mais de um banheiro conectado a um quarto
    n_quarto1 = list(graph["quarto 1"])
    qnt_q1 = len([v for v in n_quarto1 if "banheiro" in v])
    if qnt_q1 != 1:
        penalty += 25

    n_quarto1 = list(graph["quarto 2"])
    qnt_q2 = len([v for v in n_quarto1 if "banheiro" in v])
    if qnt_q2 != 1:
        penalty += 25

    return penalty
