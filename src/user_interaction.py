import keyboard
import os

import assets.globals as globals
import src.maze_generator as maze_generator


def GetMaze(maze_type, maze_size):
    if (maze_type.lower() == globals.spanning_name):
        maze = maze_generator.SpanningTreeMaze(maze_size[0], maze_size[1])
    elif (maze_type.lower() == globals.DFS_name):
        maze = maze_generator.DFSMaze(maze_size[0], maze_size[1])
    return maze


def clearScreen():
    os.system(globals.clear_command)

def PlayGame(maze: maze_generator.Maze):
    def UnhookInput(message):
        nonlocal hook
        keyboard.unhook(hook)
        ret = keyboard.record('enter',)
        print('\r')
        hook = keyboard.on_release(Callback)
        return ret
    
    def Callback(name):
        nonlocal hook
        clearScreen()
        if (name.name == globals.command_help):
            print(globals.help_message)
        elif (name.name == globals.command_solution):
            maze.ShowSolution()
        elif (name.name == globals.command_save):
            maze.Save(UnhookInput(globals.saving_tip))
        elif (name.name == globals.command_load):
            maze.Load(UnhookInput(globals.loading_tip))
        elif not maze.Move(name.name):
            print(globals.wrong_move_message)
        if maze.status:
            maze.ShowSolution()
            print(globals.winning_message)
            keyboard.unhook(hook)
            return
        maze.ShowGame()
        print(globals.tip)
    hook = keyboard.on_release(Callback)
    clearScreen()
    print(globals.help_message)
    maze.ShowGame()
    keyboard.wait(globals.command_exit)
    


def ShowMaze(maze: maze_generator.Maze):
    maze.ShowSolution()
    print('\n\n')
    maze.Show()
