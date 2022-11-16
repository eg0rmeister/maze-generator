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
        move = input("enter your move(wasd) or 'help' for available commands':")
        if (move == "help"):
            print("\thelp -- display these tips")
            print("\texit -- exit the game and display the solution")
            print("\tsolution -- display the solution and continue playing")
            print("\tsave <filename> -- save the game to file named <filename>")
            print("\tload <filename> -- load the game from file named <filename>")
        elif (move == "solution"):
            maze.ShowSolution()
        elif (move[:5] == "save "):
            maze.Save(move[5:])
        elif (move[:5] == "load "):
            maze.Load(move[5:])
        elif (move == "exit"):
            won = False
            break
        elif not maze.Move(move):
            print("that move is prohibited")
    maze.ShowSolution()
    if won:
        print("You Won!")
elif (sys.argv[4].lower() == "show"):
    maze.ShowSolution()
    print('\n\n')
    maze.Show()