import sys
import random
from pyamaze import maze, agent, COLOR
from GameSearch import Minimax, AlphaBeta

def main(player, search_method, size):
    if size == 10:
        m = maze(10, 10)
    else:
        m = maze(20, 30)

    m.CreateMaze(loopPercent=100)
    
    max_start = (random.randint(1, m.rows), random.randint(1, m.cols))
    min_start = (random.randint(1, m.rows), random.randint(1, m.cols))
    
    print(f"Max agent starting position: {max_start}")
    print(f"Min agent starting position: {min_start}")

    max_agent = agent(m, max_start[0], max_start[1], shape='arrow', footprints=True, color=COLOR.blue)
    min_agent = agent(m, min_start[0], min_start[1], shape='arrow', footprints=True, color=COLOR.red)
    
    if search_method == 'MM':
        game_search = Minimax(m, max_agent, min_agent, search_method, player)
    elif search_method == 'AB':
        game_search = AlphaBeta(m, max_agent, min_agent, search_method, player)
    else:
        print("Invalid search method. Please use 'MM' for Minimax or 'AB' for AlphaBeta.")
        sys.exit(1)
    
    print("Starting game...")
    game_search.start_game(player)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: MazeRunner.py [player] [searchmethod] [size]")
        sys.exit(1)
    
    try:
        player = int(sys.argv[1])
        if player not in [1, 2]:
            raise ValueError("Player must be 1 or 2.")
        
        search_method = sys.argv[2]
        if search_method not in ['MM', 'AB']:
            raise ValueError("Search method must be 'MM' for Minimax or 'AB' for AlphaBeta.")
        
        size = int(sys.argv[3])
        if size not in [10, 20, 30]:  # Assuming only these sizes are valid
            raise ValueError("Size must be 10, 20, or 30.")
        
        main(player, search_method, size)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
