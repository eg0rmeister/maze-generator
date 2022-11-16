import maze_generator
import sys
if (sys.argv[1].lower() == "spanning_tree"):
    maze = maze_generator.SpanningTreeMaze(int(sys.argv[2]), int(sys.argv[3]))
elif (sys.argv[1].lower() == "dfs"):
    maze = maze_generator.DFSMaze(int(sys.argv[2]), int(sys.argv[3]))
if (sys.argv[4] == "play"):
    won = True
    while not maze.status:
        print('\n')
        maze.ShowGame()
        move = input("enter your move(wasd) or 'exit' to exit:")
        if (move == "exit"):
            won = False
            break
        if not maze.Move(move):
            print("that move is prohibited")
    maze.ShowSolution()
    if won:
        print("You Won!")