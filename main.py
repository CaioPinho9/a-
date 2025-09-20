import csv
import datetime
import random
import statistics

debug = True

MAX_DISTANCE = 362880


class Node:
    def __init__(self, state, zero_pos, distance=0, heuristic=0, parent=None):
        self.state = state
        self.zero_pos = zero_pos
        self.distance = distance
        self.heuristic = heuristic
        self.parent = parent
        self.next = None


def is_solvable(puzzle):
    inv = 0
    nums = [x for x in puzzle if x != 0]
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] > nums[j]:
                inv += 1
    return inv % 2 == 0


def generate_random_puzzle():
    puzzle = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    while True:
        random.shuffle(puzzle)
        if is_solvable(puzzle):
            return puzzle


def print_puzzle(puzzle):
    if not debug:
        return

    count = 0
    for row in puzzle:
        print(row, end=" ")
        count += 1
        if count % 3 == 0:
            print()
    print()


def print_debug(message):
    if debug:
        print(message)


def generate_next_states(node, tree):
    next_states = []
    puzzle = node.state
    zero_pos = node.zero_pos
    directions_column = [-3, 3]
    directions_row = [-1, 1]

    def new_states():
        new_puzzle = puzzle.copy()
        new_puzzle[zero_pos], new_puzzle[new] = puzzle[new], puzzle[zero_pos]
        distance = node.distance + 1
        next_states.append(Node(new_puzzle, new, distance, tree.heuristic_function(node), node))
        # if distance > tree.path_size:
        #     print_debug(f"Level: {distance}")
        #     tree.path_size = distance
        #     print_debug(f"Frontier size: {tree.frontier_states.size}")
        #     print_debug(f"Visited size: {len(tree.visited_states)}")

    for direction in directions_column:
        new = zero_pos + direction
        if 0 <= new <= 8:
            new_states()

    for direction in directions_row:
        if 0 <= zero_pos % 3 + direction <= 2:
            new = zero_pos + direction
            new_states()

    node.next = next_states


final_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]


def check_final_state(state):
    return state == final_state


class OrderedNodeList:
    def __init__(self):
        self.buckets = {}
        self.keys = []
        self.max_key = None
        self.size = 0

    def add(self, node):
        key = node.heuristic
        if key not in self.buckets:
            self.keys.append(key)
            self.buckets[key] = []

        if not self.max_key or key > self.max_key:
            self.max_key = key

        self.buckets[key].append(node)
        self.size += 1

    def pop(self):
        if not self.buckets:
            raise IndexError("pop from empty OrderedNodeList")
        node = self.buckets[self.max_key].pop(0)
        self.size -= 1
        if not self.buckets[self.max_key]:
            del self.buckets[self.max_key]
            self.keys.remove(self.max_key)
            self.max_key = max(self.keys) if self.keys else None
        return node


class Tree:
    def __init__(self, root, heuristic_function):
        self.root = root
        self.frontier_states = OrderedNodeList()
        self.frontier_states.add(root)
        self.visited_states = set()
        self.path_size = 0
        self.heuristic_function = heuristic_function

    def already_visited(self, state):
        return tuple(state) in self.visited_states


def uniform_cost(node):
    return 0


def difference_heuristic(node):
    difference = [-1 for a, b in zip(final_state, node.state) if a != b]
    sum_difference = sum(difference)
    return MAX_DISTANCE - node.distance + 8 + sum_difference


def unnacceptable_heuristic(node):
    state = node.state
    sum_value = 0
    for i in range(8):
        state_value = state[i]
        final_index = final_state.index(state_value)
        sum_value += (abs(i % 3 - final_index % 3) + abs(i // 3 - final_index // 3))
    return MAX_DISTANCE - node.distance + sum_value


def inversion_heuristic(node):
    state = node.state
    inversions = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] != 0 and state[j] != 0 and state[i] > state[j]:
                inversions += 1
    return MAX_DISTANCE - node.distance + 28 - inversions


def print_tree(node):
    path = []
    while node:
        path.append(node)
        node = node.parent
    for n in reversed(path):
        print_puzzle(n.state)


def save_txts(tree):
    with open("fronteira.txt", "w") as f:
        for bucket in tree.frontier_states.buckets.values():
            for n in bucket:
                f.write(f"{n.state}\n")
    with open("visitados.txt", "w") as f:
        for state in tree.visited_states:
            f.write(f"{list(state)}\n")


examples = [
    [1, 8, 5, 7, 4, 6, 0, 3, 2],  # facil
    [6, 1, 4, 0, 8, 5, 7, 3, 2],  # medio
    [0, 3, 8, 6, 5, 1, 7, 4, 2],  # dificil
]

heuristics = [
    uniform_cost,
    difference_heuristic,
    unnacceptable_heuristic,
    inversion_heuristic
]


def execute(initial_value, heuristic):
    start_time = datetime.datetime.now()
    end_time = None

    state = initial_value
    zero_pos = state.index(0)
    node = Node(state, zero_pos)

    print_debug("Initial Puzzle:")
    print_puzzle(node.state)

    tree = Tree(node, heuristic)

    try:
        while True:
            node = tree.frontier_states.pop()

            if check_final_state(node.state):
                print(f"O tamanho do caminho: {node.distance}")
                end_time = datetime.datetime.now()
                print(f"Tempo de execução (em segundos): {end_time - start_time}")
                print(f"O total de nodos visitados: {len(tree.visited_states)}")
                print(f"O maior tamanho da fronteira (lista de abertos): {tree.frontier_states.size}")

                # save_txts(tree)

                # print_tree(node)
                break

            generate_next_states(node, tree)

            for next_node in node.next:
                if not tree.already_visited(next_node.state):
                    tree.frontier_states.add(next_node)

            tree.visited_states.add(tuple(node.state))

    except IndexError:
        print("Estado não resolvivel")

    return end_time - start_time


def benchmark(runs, seed=42):
    random.seed(seed)
    heuristic = difference_heuristic
    times = []
    for i in range(runs):
        initial_value = generate_random_puzzle()
        print("Run", i + 1)
        t = execute(initial_value, heuristic)
        times.append(t.total_seconds())
        print("-" * 20)
    mean_time = statistics.mean(times)
    print("\n--- Benchmark ---")
    print(f"Runs: {runs}")
    print("Times (s):", [round(x, 3) for x in times])
    print(f"Mean execution time: {mean_time:.3f} seconds")
    return mean_time


if __name__ == "__main__":
    rows = []

    for example in examples:
        for heuristic in heuristics:
            print(f"Using heuristic: {heuristic.__name__}")
            print("Example:", example)
            elapsed = execute(example, heuristic)  # assume this returns duration in seconds
            rows.append({
                "heuristic": heuristic.__name__,
                "example": str(example),
                "time_seconds": elapsed,
            })
            print("=" * 40)

    csv_path = "results.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["heuristic", "example", "time_seconds"])
        writer.writeheader()
        writer.writerows(rows)
    # benchmark(runs=50)
