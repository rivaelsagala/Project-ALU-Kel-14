class PuzzleSolver:
    @staticmethod
    def is_solvable(puzzle_state):
        inversions = 0
        for i in range(len(puzzle_state)):
            for j in range(i + 1, len(puzzle_state)):
                if puzzle_state[i] > puzzle_state[j]:
                    inversions += 1
        return inversions % 2 == 0
    
    @staticmethod
    def solve(puzzle_state):
        if not PuzzleSolver.is_solvable(puzzle_state):
            return None
            
        def is_goal(state):
            return state == list(range(len(state)))
            
        def get_neighbors(state):
            neighbors = []
            size = int(len(state) ** 0.5)
            
            for i in range(len(state)):
                # Cek tetangga horizontal
                if i % size > 0:
                    new_state = state.copy()
                    new_state[i], new_state[i-1] = new_state[i-1], new_state[i]
                    neighbors.append(new_state)
                
                if i % size < size - 1:
                    new_state = state.copy()
                    new_state[i], new_state[i+1] = new_state[i+1], new_state[i]
                    neighbors.append(new_state)
                
                # Cek tetangga vertikal
                if i - size >= 0:
                    new_state = state.copy()
                    new_state[i], new_state[i-size] = new_state[i-size], new_state[i]
                    neighbors.append(new_state)
                
                if i + size < len(state):
                    new_state = state.copy()
                    new_state[i], new_state[i+size] = new_state[i+size], new_state[i]
                    neighbors.append(new_state)
            
            return neighbors
        
        def backtrack(state, visited):
            if is_goal(state):
                return state
            
            state_tuple = tuple(state)
            if state_tuple in visited:
                return None
            
            visited.add(state_tuple)
            
            for neighbor in get_neighbors(state):
                result = backtrack(neighbor, visited)
                if result is not None:
                    return result
            
            return None
        
        return backtrack(puzzle_state.copy(), set())