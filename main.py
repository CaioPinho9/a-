import datetime
import random


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


def print_puzzle(puzzle):
    count = 0
    for row in puzzle:
        print(row, end=" ")
        count += 1
        if count % 3 == 0:
            print()
    print()


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
            print(f"Level: {distance}")
            tree.path_size = distance
            print(f"Frontier size: {len(tree.frontier_states)}")
            print(f"Visited size: {len(tree.visited_states)}")

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


class Tree:
    def __init__(self, root):
        self.root = root
        self.frontier_states = [root]
        self.visited_states = set()
        self.path_size = 0

    def already_visited(self, state):
        return tuple(state) in self.visited_states


def main():
    generated_nodes_count = 0
    start_time = datetime.datetime.now()

    state = generate_random_puzzle()
    zero_pos = state.index(0)
    node = Node(state, zero_pos)

    print("Initial Puzzle:")
    print_puzzle(node.state)

    tree = Tree(node)

    try:
        while True:
            node = tree.frontier_states.pop(0)

            if check_final_state(node.state):
                print("Final Puzzle:")
                print_puzzle(node.state)
                print("Lenght: ", node.distance)
                print("Final state reached!")
                break

            generate_next_states(node, tree)

            for next_node in node.next:
                if not tree.already_visited(next_node.state):
                    generated_nodes_count += 1
                    # TODO: ordenado por heuristica
                    tree.frontier_states.append(next_node)

            tree.visited_states.add(tuple(node.state))

    except IndexError:
        print("Estado não resolvivel")

    end_time = datetime.datetime.now()
    print("Execution Time: ", end_time - start_time)
    print("Frontier size: ", len(tree.frontier_states))
    print("Visited size: ", len(tree.visited_states))
    print("Nodes generated: ", generated_nodes_count)


main()
