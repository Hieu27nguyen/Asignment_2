# MazeRunner.py

import sys
import random
import pyamaze as maze
from GameSearch import GameSearch

def main(player, search_method, size):
    m_size = (10, 10) if size == 10 else (20, 30)
    m = maze.maze(*m_size)
    m.CreateMaze(loopPercent=100, theme=maze.COLOR.light)

    # Ensure random positions are within the maze bounds
    def random_open_position():
        while True:
            pos = (random.randint(1, m.rows), random.randint(1, m.cols))
            if m.maze_map[pos]['E'] or m.maze_map[pos]['W'] or m.maze_map[pos]['N'] or m.maze_map[pos]['S']:
                return pos

    max_pos = random_open_position()
    min_pos = random_open_position()
    goal_pos = random_open_position()

    max_player = maze.agent(m, max_pos[0], max_pos[1], shape='arrow', footprints=True)
    min_player = maze.agent(m, min_pos[0], min_pos[1], shape='square', footprints=True, color=maze.COLOR.red)

    game = GameSearch(m, max_pos, min_pos, goal_pos)

    if search_method == 'MM':
        print("Using Minimax")
        eval, max_path = game.minimax(depth=3, player=max_pos, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
    elif search_method == 'AB':
        print("Using Minimax with Alpha-Beta Pruning")
        eval, max_path = game.minimax(depth=3, player=max_pos, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)

    max_moves = ''.join(max_path)
    min_moves = ''.join(random.choices(['N', 'E', 'S', 'W'], k=10))  # Random moves for MIN player

    m.tracePath({max_player: max_moves})
    m.tracePath({min_player: min_moves})
    m.run()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: MazeRunner.py [player] [searchmethod] [size]")
        sys.exit(1)

    player = int(sys.argv[1])
    search_method = sys.argv[2]
    size = int(sys.argv[3])

    main(player, search_method, size)
