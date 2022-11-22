import assets.globals as globals
import src.maze_generator as maze_generator

def GetMaze(maze_type, maze_size):
    if (maze_type.lower() == globals.spanning_name):
        maze = maze_generator.SpanningTreeMaze(maze_size[0], maze_size[1])
    elif (maze_type.lower() == globals.DFS_name):
        maze = maze_generator.DFSMaze(maze_size[0], maze_size[1])
    return maze

def PlayGame(maze: maze_generator.Maze):
    while not maze.status:
        print('\n')
        maze.ShowGame()
        move = input("enter your move(wasd) or 'help' for available commands':")
        if (move == globals.command_help):
            print(globals.help_message)
        elif (move == globals.command_solution):
            maze.ShowSolution()
        elif (move.startswith(globals.command_save)):
            maze.Save(move[5:])
        elif (move.startswith(globals.command_load)):
            maze.Load(move[5:])
        elif (move == globals.command_exit):
            break
        elif (move == globals.command_solve_exit):
            maze.ShowSolution()
            break
        elif not maze.Move(move):
            print(globals.wrong_move_message)
    if maze.status:
        maze.ShowSolution()
        print(globals.winning_message)


def ShowMaze(maze: maze_generator.Maze):
    maze.ShowSolution()
    print('\n\n')
    maze.Show()