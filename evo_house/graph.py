from evo_house.representation import Room, Stairs, Floor
from evo_house.utils import has_room_on_the_way


def create_graph(floor: Floor):
    graph = {tag: set() for tag in floor.room_names}
    for i in range(len(floor)):
        N_count = 0
        for j in range(len(floor)):
            if i == j or has_room_on_the_way(floor[i], floor[j], floor.rooms):  # type: ignore
                continue
            if is_neighbor(floor[i], floor[j]):  # type: ignore
                if isinstance(floor[j], Stairs):
                    continue
                graph[floor[i].name].add(floor[j].name)  # type: ignore
                graph[floor[j].name].add(floor[i].name)  # type: ignore
                N_count += 1
        if N_count == 0:
            if "None" not in graph.keys():
                graph["None"] = set()
            graph[floor[i].name].add("None")  # type: ignore
            graph["None"].add(floor[i].name)  # type: ignore
    return graph


# Verifica se o grafo é conexo
def is_connected(graph: dict[str, set]):
    stack = []
    visited = set()
    stack.append(next(iter(graph)))

    while stack:
        v = stack.pop()
        visited.add(v)
        for u in graph[v]:
            if u not in visited:
                stack.append(u)

    return len(visited) == len(graph)


def is_neighbor(room1: Room, room2: Room):
    target_side = room1.opening_sides[1]

    x1, y1 = room1.initial_pos
    x2, y2 = room2.initial_pos
    w1, h1 = room1.width, room1.height
    w2, h2 = room2.width, room2.height

    # considerar intervalo da porta com offset de 0.6
    xp, yp = room1.door_pos

    if target_side == "left" or target_side == "right":
        ypi = max(yp - 0.6, y1)
        ypf = min(yp + 0.6, y1 + h1)
        start = max(ypi, y2)
        end = min(ypf, y2 + h2)
        if start > end:
            return False

        length = end - start
        hp = ypf - ypi

        if not (length / hp > 0.5 or length / h2 > 0.5):
            return False

        return (target_side == "left" and (x2 + w2) - x1 <= 0) or (
            target_side == "right" and x2 - (x1 + w1) >= 0
        )
    else:
        xpi = max(xp - 0.6, x1)
        xpf = min(xp + 0.6, x1 + w1)
        start = max(xpi, x2)
        end = min(xpf, x2 + w2)
        if start > end:
            return False

        length = end - start
        wp = xpf - xpi

        if not (length / wp > 0.5 or length / w2 > 0.5):
            return False

        return (target_side == "bottom" and (y2 + h2) - y1 <= 0) or (
            target_side == "top" and y2 - (y1 + h1) >= 0
        )


def join_graphs(graph1: dict[str, set[str]],graph2: dict[str, set[str]]):
    merged_graph = graph1.copy()  # Começa com uma cópia de dict1

    for key, value in graph2.items():
        if key in merged_graph:
            merged_graph[key] = merged_graph[key].union(value)
        else:
            merged_graph[key] = value

    return merged_graph
