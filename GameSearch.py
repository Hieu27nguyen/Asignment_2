class GameSearch:
    def __init__(self, maze, max_agent, min_agent, search_method, player):
        self.maze = maze
        self.max_agent = max_agent
        self.min_agent = min_agent
        self.search_method = search_method
        self.player = player
        self.goal = self.set_goal()

    def set_goal(self):
        while True:
            goal = (random.randint(1, self.maze.rows), random.randint(1, self.maze.cols))
            if goal != self.max_agent.position and goal != self.min_agent.position:
                return goal

    def is_terminal(self, node):
        max_pos, min_pos = node
        return max_pos == self.goal or min_pos == self.goal

    def evaluate(self, node):
        max_pos, min_pos = node
        if max_pos == self.goal:
            return 100
        elif min_pos == self.goal:
            return -100
        max_dist = abs(max_pos[0] - self.goal[0]) + abs(max_pos[1] - self.goal[1])
        min_dist = abs(min_pos[0] - self.goal[0]) + abs(min_pos[1] - self.goal[1])
        return min_dist - max_dist

    def get_children(self, node, player):
        max_pos, min_pos = node
        children = []
        
        if player == 'MAX':
            possible_moves = self.maze.get_neighbors(max_pos[0], max_pos[1])
            for move in possible_moves:
                if 1 <= move[0] <= self.maze.rows and 1 <= move[1] <= self.maze.cols:
                    children.append(((move[0], move[1]), min_pos))
        else:
            possible_moves = self.maze.get_neighbors(min_pos[0], min_pos[1])
            for move in possible_moves:
                if 1 <= move[0] <= self.maze.rows and 1 <= move[1] <= self.maze.cols:
                    children.append((max_pos, (move[0], move[1])))
        
        return children

    def minimax(self, node, depth, maximizing_player):
        if depth == 0 or self.is_terminal(node):
            return self.evaluate(node)
        
        if maximizing_player:
            max_eval = float('-inf')
            for child in self.get_children(node, 'MAX'):
                eval = self.minimax(child, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for child in self.get_children(node, 'MIN'):
                eval = self.minimax(child, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def alpha_beta(self, node, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_terminal(node):
            return self.evaluate(node)
        
        if maximizing_player:
            max_eval = float('-inf')
            for child in self.get_children(node, 'MAX'):
                eval = self.alpha_beta(child, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for child in self.get_children(node, 'MIN'):
                eval = self.alpha_beta(child, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def start_game(self):
        current_node = (self.max_agent.position, self.min_agent.position)
        turn = 'MAX' if self.player == 1 else 'MIN'
        
        while not self.is_terminal(current_node):
            if turn == 'MAX':
                if self.search_method == 'MM':
                    best_move = self.minimax(current_node, 3, True)  # Adjust depth as needed
                else:
                    best_move = self.alpha_beta(current_node, 3, float('-inf'), float('inf'), True)  # Adjust depth as needed
                # Move the MAX agent to the best position
                current_node = (best_move, current_node[1])
                turn = 'MIN'
            else:
                # Human player makes a move
                print(f"Your turn. Current position: {current_node[1]}")
                move = input("Enter your move (format: row,col): ")
                try:
                    move = tuple(map(int, move.split(',')))
                    if move in self.maze.get_neighbors(current_node[1][0], current_node[1][1]):
                        current_node = (current_node[0], move)
                    else:
                        print("Invalid move. Try again.")
                        continue
                except ValueError:
                    print("Invalid input format. Use row,col.")
                    continue
                turn = 'MAX'
            
            print(f"Current state: {current_node}")
        
        if current_node[0] == self.goal:
            print("AI (MAX) wins!")
        else:
            print("Human (MIN) wins!")
