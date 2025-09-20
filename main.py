import datetime
import random
import statistics


class Node:
    def __init__(self, state, zero_pos, distance=0, heuristic=0):
        self.state = state
        self.zero_pos = zero_pos
        self.distance = distance
        self.heuristic = heuristic
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


debug = False


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
        next_states.append(Node(new_puzzle, new, distance))
        if distance > tree.path_size:
            print_debug(f"Level: {distance}")
            tree.path_size = distance
            print_debug(f"Frontier size: {tree.frontier_states.size}")
            print_debug(f"Visited size: {len(tree.visited_states)}")

    for direction in directions_column:
        new = zero_pos + direction
        if 0 <= new <= 8:
            new_states()

    for direction in directions_row:
        if 0 <= zero_pos % 3 + direction <= 2:
            new = zero_pos + direction
            new_states()

    node.next = next_states


def check_final_state(state):
    return state == [1, 2, 3, 4, 5, 6, 7, 8, 0]


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
    def __init__(self, root):
        self.root = root
        self.frontier_states = OrderedNodeList()
        self.frontier_states.add(root)
        self.visited_states = set()
        self.path_size = 0

    def already_visited(self, state):
        return tuple(state) in self.visited_states


def execute():
    generated_nodes_count = 0
    start_time = datetime.datetime.now()

    state = generate_random_puzzle()
    zero_pos = state.index(0)
    node = Node(state, zero_pos)

    print_debug("Initial Puzzle:")
    print_puzzle(node.state)

    tree = Tree(node)

    try:
        while True:
            node = tree.frontier_states.pop()

            if check_final_state(node.state):
                print_debug("Final Puzzle:")
                print_puzzle(node.state)
                print_debug(f"Lenght: {node.distance}")
                print_debug("Final state reached!")
                break

            generate_next_states(node, tree)

            for next_node in node.next:
                if not tree.already_visited(next_node.state):
                    generated_nodes_count += 1
                    # TODO: ordenado por heuristica
                    tree.frontier_states.add(next_node)

            tree.visited_states.add(tuple(node.state))

    except IndexError:
        print("Estado não resolvivel")

    end_time = datetime.datetime.now()
    print_debug(f"Execution Time: {end_time - start_time}")
    print_debug(f"Frontier size: {tree.frontier_states.size}")
    print_debug(f"Visited size: {len(tree.visited_states)}")
    print_debug(f"Nodes generated: {generated_nodes_count}")

    return end_time - start_time


def benchmark(runs, seed=42):
    random.seed(seed)
    times = []
    for i in range(runs):
        print("Run", i + 1)
        t = execute()
        times.append(t.total_seconds())
    mean_time = statistics.mean(times)
    print("\n--- Benchmark ---")
    print(f"Runs: {runs}")
    print("Times (s):", [round(x, 3) for x in times])
    print(f"Mean execution time: {mean_time:.3f} seconds")
    return mean_time


if __name__ == "__main__":
    benchmark(runs=5)
