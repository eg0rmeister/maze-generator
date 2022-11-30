import keyboard
import os

import assets.globals as globals
import src.maze_generator as maze_generator


def GetMaze(maze_type, maze_size):
    """Returns maze of given type and size"""
    if (maze_type.lower() == globals.spanning_name):
        maze = maze_generator.SpanningTreeMaze(maze_size[0], maze_size[1])
    elif (maze_type.lower() == globals.DFS_name):
        maze = maze_generator.DFSMaze(maze_size[0], maze_size[1])
    return maze


def clearScreen():
    """Clears screen"""
    os.system(globals.clear_command)

def PlayGame(maze: maze_generator.Maze):
    """Handles playing the game itself"""
    def PlayCallback(name):
        """Keyboard release handler"""
        nonlocal hook
        clearScreen()
        if (name == None or name.name == globals.command_help):
            print(globals.help_message)
        elif (name.name == globals.command_solution):
            maze.ShowSolution()
        elif (name.name == globals.command_save):
            maze.Save(globals.saving_location)
            print(globals.saving_message)
        elif (name.name == globals.command_load):
            maze.Load(globals.saving_location)
            print(globals.loading_message)
        elif not maze.Move(name.name):
            print(globals.wrong_move_message)
        if maze.status:
            maze.ShowSolution()
            print(globals.winning_message)
            keyboard.unhook(hook)
            return
        maze.ShowGame()
        print(globals.tip)
    hook = keyboard.on_release(PlayCallback)
    clearScreen()
    print(globals.help_message)
    maze.ShowGame()
    keyboard.wait(globals.command_exit)
    


def ShowMaze(maze: maze_generator.Maze):
    """Shows the maze and its solution"""
    maze.ShowSolution()
    print('\n\n')
    maze.Show()
