import os


# symbols for drawing
N_s = chr(9589)  # ╵
E_s = chr(9590)  # ╶
S_s = chr(9591)  # ╷
W_s = chr(9588)  # ╴

NE_s = chr(9492)  # └
NS_s = chr(9474)  # │
NW_s = chr(9496)  # ┘
ES_s = chr(9484)  # ┌
EW_s = chr(9472)  # ─
SW_s = chr(9488)  # ┐

player_s = chr(9532)  # ┼

wall_s = chr(0x2588)  # █

DFS_name = "dfs"
spanning_name = "spanning_tree"

arg_play = "play"
arg_show = "show"

command_help = "h"
command_solution = "1"
command_save = "f"
command_load = "r"
command_exit = "escape"

wrong_move_message = "that move is prohibited"
winning_message = "You Won! press escape to exit or r to start over"

win_status = 1
exit_status = 0

help_message = """
                \tw/a/s/d -- move the character '┼'\n
                \th -- display these tips\n
                \tescape -- exit the game WITHOUT displaying solution\n
                \t1 -- display the solution and continue playing\n
                \tf -- save the game\n
                \tr -- load the game\n
               """

tip = "use wasd to move or h to display help message"
loading_tip = "enter load location"
saving_tip = "enter save location"

if os.name == 'nt':
    clear_command = "cls"
elif os.name == 'posix':
    clear_command = "clear"