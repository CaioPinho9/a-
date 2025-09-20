import datetime


class Node:
    def __init__(self, state, distance=0, heuristic=0):
        self.state = state
        self.distance = distance
        self.heuristic = heuristic
        self.next = None


def generate_random_puzzle():
    set_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    import random
    puzzle = [[], [], []]

    while len(set_numbers) > 0:
        for i in range(3):
            num = random.choice(set_numbers)
            set_numbers.remove(num)
            puzzle[i].append(num)

    return puzzle


def print_puzzle(puzzle):
    for row in puzzle:
        print(row)
    print()


current_level = 0


def generate_next_states(node, tree):
    global current_level
    next_states = []
    puzzle = node.state
    zero_pos = [(i, row.index(0)) for i, row in enumerate(puzzle) if 0 in row][0]
    x, y = zero_pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_puzzle = [row[:] for row in puzzle]
            new_puzzle[x][y], new_puzzle[new_x][new_y] = new_puzzle[new_x][new_y], new_puzzle[x][y]
            next_states.append(Node(new_puzzle, node.distance + 1))
            if (node.distance + 1) > current_level:
                print(f"Level: {node.distance + 1}")
                current_level = node.distance + 1
                print(f"Frontier size: {len(tree.frontier_states)}")
                print(f"Visited size: {len(tree.visited_states)}")

    node.next = next_states


def check_final_state(state):
    final_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    return state == final_state


class Tree:
    def __init__(self, root):
        self.root = root
        self.frontier_states = [root]
        self.visited_states = []
        self.path_size = 0

    def already_visited(self, state):
        return any(state == visited.state for visited in self.visited_states)


def main():
    start_time = datetime.datetime.now()
    print("Initial Puzzle:")
    node = Node(generate_random_puzzle())
    print_puzzle(node.state)
    tree = Tree(node)

    for node in tree.frontier_states:
        if check_final_state(node.state):
            print_puzzle(node.state)
            print("Lenght: ", node.distance)
            print("Final state reached!")
            return

        generate_next_states(node, tree)

        for next_node in node.next:
            if not tree.already_visited(next_node.state):
                # TODO: ordenado por heuristica
                tree.frontier_states.append(next_node)

        tree.visited_states.append(node)

    end_time = datetime.datetime.now()
    print(f"Execution Time: {end_time - start_time}")


main()
