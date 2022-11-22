import src.maze_generator as maze_generator

def GetMaze(maze_type, maze_size):
    if (maze_type.lower() == "spanning_tree"):
        maze = maze_generator.SpanningTreeMaze(maze_size[0], maze_size[1])
    elif (maze_type.lower() == "dfs"):
        maze = maze_generator.DFSMaze(maze_size[0], maze_size[1])
    return maze
        
def PlayGame(maze: maze_generator.Maze):
    while not maze.status:
        print('\n')
        maze.ShowGame()
        move = input("enter your move(wasd) or 'help' for available commands':")
        if (move == "help"):
            print("\thelp -- display these tips")
            print("\texit and solve -- exit the game and display the solution")
            print("\texit -- exit the game WITHOUT displaying solution")
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
            break
        elif (move == "exit and solve"):
            maze.ShowSolution()
            break
        elif not maze.Move(move):
            print("that move is prohibited")
    if maze.status:
        maze.ShowSolution()
        print("You Won!")


def ShowMaze(maze: maze_generator.Maze):
    maze.ShowSolution()
    print('\n\n')
    maze.Show()