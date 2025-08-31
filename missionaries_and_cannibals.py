# missionaries_and_cannibals.py
from collections import deque

def is_valid(state):
    """Checks if a state is valid."""
    missionaries_left, cannibals_left, boat_pos = state
    missionaries_right = 3 - missionaries_left
    cannibals_right = 3 - cannibals_left

    # Rule 1: Missionaries are not outnumbered on the left bank
    if missionaries_left > 0 and missionaries_left < cannibals_left:
        return False
    # Rule 2: Missionaries are not outnumbered on the right bank
    if missionaries_right > 0 and missionaries_right < cannibals_right:
        return False
    return True

def get_successors(state):
    """Generates all possible valid successor states."""
    successors = []
    m, c, b = state
    
    # Possible moves: (missionaries, cannibals)
    moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
    
    for dm, dc in moves:
        if b == 1:  # Boat is on the left bank, moving to the right
            new_state = (m - dm, c - dc, 0)
        else:  # Boat is on the right bank, moving to the left
            new_state = (m + dm, c + dc, 1)

        # Check if the move is possible (enough people to move) and the resulting state is valid
        if 0 <= new_state[0] <= 3 and 0 <= new_state[1] <= 3 and is_valid(new_state):
            successors.append(new_state)
            
    return successors

def solve_bfs():
    """Solves the problem using Breadth-First Search."""
    start_state = (3, 3, 1)
    goal_state = (0, 0, 0)
    
    queue = deque([(start_state, [start_state])])
    visited = {start_state}
    
    while queue:
        current_state, path = queue.popleft()
        
        if current_state == goal_state:
            return path
        
        for successor in get_successors(current_state):
            if successor not in visited:
                visited.add(successor)
                new_path = path + [successor]
                queue.append((successor, new_path))
                
    return None

if __name__ == "__main__":
    solution = solve_bfs()
    if solution:
        print("🎉 Solution Found (BFS Optimal Path):")
        for i, state in enumerate(solution):
            print(f"Step {i}: {state}")
    else:
        print("No solution found.")