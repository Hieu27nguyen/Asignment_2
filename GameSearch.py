import math

class GameSearch:
    def __init__(self, maze, max_agent, min_agent, search_method, player):
        self.maze = maze
        self.max_agent = max_agent
        self.min_agent = min_agent
        self.search_method = search_method
        self.player = player
        self.goal = (self.maze.rows, self.maze.cols)
        self.path = {max_agent: [(max_agent.x, max_agent.y)], min_agent: [(min_agent.x, min_agent.y)]}

    def is_terminal_state(self):
        return (self.max_agent.x == self.goal[0] and self.max_agent.y == self.goal[1]) or \
               (self.min_agent.x == self.goal[0] and self.min_agent.y == self.goal[1])

    def update_display(self):
        print(f"Updating display...")
        print(f"Max agent position: ({self.max_agent.x}, {self.max_agent.y})")
        print(f"Min agent position: ({self.min_agent.x}, {self.min_agent.y})")
        print(f"Max agent path: {self.path[self.max_agent]}")
        print(f"Min agent path: {self.path[self.min_agent]}")
        self.maze.tracePath({self.max_agent: self.path[self.max_agent], self.min_agent: self.path[self.min_agent]}, delay=100)

    def apply_move(self, move, agent):
        print(f"Applying move {move} for agent at position ({agent.x}, {agent.y})")
        if move == 'U':
            agent.moveUp()
        elif move == 'D':
            agent.moveDown()
        elif move == 'L':
            agent.moveLeft()
        elif move == 'R':
            agent.moveRight()
        new_position = (agent.x, agent.y)
        print(f"New position of agent: {new_position}")
        self.path[agent].append(new_position)
        self.update_display()

    def get_valid_moves(self, agent):
        moves = []
        cell = self.maze.maze_map[(agent.x, agent.y)]
        if cell.get('U', False):
            moves.append('U')
        if cell.get('D', False):
            moves.append('D')
        if cell.get('L', False):
            moves.append('L')
        if cell.get('R', False):
            moves.append('R')
        return moves

    def minimax(self, node, depth, maximizing_player):
        if depth == 0 or self.is_terminal_state():
            return self.evaluate_state(node)

        valid_moves = self.get_valid_moves(node)
        if maximizing_player:
            max_eval = -math.inf
            best_move = None
            for move in valid_moves:
                self.apply_move(move, node)
                eval = self.minimax(node, depth - 1, False)
                self.undo_move(move, node)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return best_move if depth == 3 else max_eval
        else:
            min_eval = math.inf
            best_move = None
            for move in valid_moves:
                self.apply_move(move, node)
                eval = self.minimax(node, depth - 1, True)
                self.undo_move(move, node)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return best_move if depth == 3 else min_eval

    def alpha_beta(self, node, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_terminal_state():
            return self.evaluate_state(node)

        valid_moves = self.get_valid_moves(node)
        if maximizing_player:
            max_eval = -math.inf
            best_move = None
            for move in valid_moves:
                self.apply_move(move, node)
                eval = self.alpha_beta(node, depth - 1, alpha, beta, False)
                self.undo_move(move, node)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return best_move if depth == 3 else max_eval
        else:
            min_eval = math.inf
            best_move = None
            for move in valid_moves:
                self.apply_move(move, node)
                eval = self.alpha_beta(node, depth - 1, alpha, beta, True)
                self.undo_move(move, node)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return best_move if depth == 3 else min_eval

    def evaluate_state(self, agent):
        if agent.x == self.goal[0] and agent.y == self.goal[1]:
            if agent == self.max_agent:
                return 100
            else:
                return -100
        else:
            max_distance = abs(self.max_agent.x - self.goal[0]) + abs(self.max_agent.y - self.goal[1])
            min_distance = abs(self.min_agent.x - self.goal[0]) + abs(self.min_agent.y - self.goal[1])
            return min_distance - max_distance

    def undo_move(self, move, agent):
        print(f"Undoing move {move} for agent at position ({agent.x}, {agent.y})")
        if move == 'U':
            agent.moveDown()
        elif move == 'D':
            agent.moveUp()
        elif move == 'L':
            agent.moveRight()
        elif move == 'R':
            agent.moveLeft()
        self.path[agent].pop()
        self.update_display()

class Minimax(GameSearch):
    def start_game(self, player):
        while not self.is_terminal_state():
            if player == 1:
                best_move = self.minimax(self.max_agent, 3, True)
                if best_move:
                    self.apply_move(best_move, self.max_agent)
                print(f"MAX moved: ({self.max_agent.x},{self.max_agent.y})")
                self.update_display()
                player = 2
            else:
                print("It is MIN's turn:")
                row = int(input("Enter the row: "))
                col = int(input("Enter the column: "))
                self.min_agent.x = row
                self.min_agent.y = col
                self.path[self.min_agent].append((self.min_agent.x, self.min_agent.y))
                self.update_display()
                player = 1
        
        if self.max_agent.x == self.goal[0] and self.max_agent.y == self.goal[1]:
            print("AI (MAX) wins!")
        else:
            print("Human (MIN) wins!")

class AlphaBeta(GameSearch):
    def start_game(self, player):
        while not self.is_terminal_state():
            if player == 1:
                best_move = self.alpha_beta(self.max_agent, 3, -math.inf, math.inf, True)
                if best_move:
                    self.apply_move(best_move, self.max_agent)
                print(f"MAX moved: ({self.max_agent.x},{self.max_agent.y})")
                self.update_display()
                player = 2
            else:
                print("It is MIN's turn:")
                row = int(input("Enter the row: "))
                col = int(input("Enter the column: "))
                self.min_agent.x = row
                self.min_agent.y = col
                self.path[self.min_agent].append((self.min_agent.x, self.min_agent.y))
                self.update_display()
                player = 1
        
        if self.max_agent.x == self.goal[0] and self.max_agent.y == self.goal[1]:
            print("AI (MAX) wins!")
        else:
            print("Human (MIN) wins!")
