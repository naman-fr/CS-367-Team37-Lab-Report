# puzzle8_solver.py
import heapq

class PuzzleNode:
    """Represents a node in the A* search tree for the 8-Puzzle."""
    def __init__(self, state, parent=None, move=None, depth=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = self.depth + self.manhattan_distance()

    def __lt__(self, other):
        return self.cost < other.cost

    def manhattan_distance(self):
        """Calculates the Manhattan distance heuristic."""
        distance = 0
        goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        for i in range(9):
            if self.state[i] != 0:
                current_pos = i
                goal_pos = goal_state.index(self.state[i])
                
                # Calculate row and column
                current_row, current_col = divmod(current_pos, 3)
                goal_row, goal_col = divmod(goal_pos, 3)
                
                distance += abs(current_row - goal_row) + abs(current_col - goal_col)
        return distance

def get_successors_8puzzle(node):
    """Generates successors for an 8-Puzzle node."""
    successors = []
    state = list(node.state)
    zero_index = state.index(0)
    row, col = divmod(zero_index, 3)

    # Possible moves: up, down, left, right
    moves = {'up': -3, 'down': 3, 'left': -1, 'right': 1}
    
    for move, delta in moves.items():
        if (move == 'left' and col == 0) or \
           (move == 'right' and col == 2) or \
           (move == 'up' and row == 0) or \
           (move == 'down' and row == 2):
            continue

        new_index = zero_index + delta
        new_state = state[:]
        new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
        successors.append(PuzzleNode(tuple(new_state), parent=node, move=move, depth=node.depth + 1))
        
    return successors

def solve_a_star(initial_state):
    """Solves the 8-Puzzle using A* search."""
    start_node = PuzzleNode(tuple(initial_state))
    open_list = [start_node]
    closed_set = set()

    while open_list:
        current_node = heapq.heappop(open_list)

        if list(current_node.state) == [1, 2, 3, 4, 5, 6, 7, 8, 0]:
            path = []
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent
            return path[::-1]

        if current_node.state in closed_set:
            continue
        
        closed_set.add(current_node.state)

        for successor in get_successors_8puzzle(current_node):
            heapq.heappush(open_list, successor)

    return None

if __name__ == "__main__":
    # Example initial state (solvable)
    initial_state = [1, 2, 3, 0, 4, 6, 7, 5, 8] 
    
    solution = solve_a_star(initial_state)
    if solution:
        print(f"🎉 Solved in {len(solution) - 1} moves!")
        for state in solution:
            print(state[0:3])
            print(state[3:6])
            print(state[6:9])
            print("-" * 10)
    else:
        print("Could not find a solution.")