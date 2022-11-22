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

command_help = "help"
command_solution = "solution"
command_save = "save "
command_load = "load "
command_exit = "exit"
command_solve_exit = "exit and solve"

wrong_move_message = "that move is prohibited"
winning_message = "You Won!"

help_message = """
                \tw/a/s/d -- move the character '┼'\n
                \thelp -- display these tips\n
                \texit and solve -- exit the game and display the solution\n
                \texit -- exit the game WITHOUT displaying solution\n
                \tsolution -- display the solution and continue playing\n
                \tsave <filename> -- save the game to file named <filename>\n
                \tload <filename> -- load the game from file named <filename>\n
               """