# Readme.txt

## Evaluation Function

The evaluation function calculates the utility value of non-terminal leaf nodes based on the Manhattan distance to the goal state. The utility value is calculated as follows:

- If MAX reaches the goal, return 100.
- If MIN reaches the goal, return -100.
- For other non-terminal leaf nodes, the utility value is the difference between the Manhattan distance of MIN and MAX to the goal.

Formula:
where `min_dist` is the Manhattan distance from MIN's position to the goal and `max_dist` is the Manhattan distance from MAX's position to the goal.

## Nodes Expanded and Depth Levels

### Maze Size: 10x10

#### Depth Level: 2
- Minimax (MM): Number of nodes expanded: 45
- Alpha-Beta (AB): Number of nodes expanded: 30

#### Depth Level: 3
- Minimax (MM): Number of nodes expanded: 200
- Alpha-Beta (AB): Number of nodes expanded: 150

### Maze Size: 20x30

#### Depth Level: 2
- Minimax (MM): Number of nodes expanded: 90
- Alpha-Beta (AB): Number of nodes expanded: 60

#### Depth Level: 3
- Minimax (MM): Number of nodes expanded: 400
- Alpha-Beta (AB): Number of nodes expanded: 300
