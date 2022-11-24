import sys

import assets.globals as globals
import src.user_interaction as ui

if (len(sys.argv) < 5):
    print(globals.wrong_start_message)
elif (sys.argv[4].lower().strip() == globals.arg_play):
    ui.PlayGame(ui.GetMaze(sys.argv[1], (int(sys.argv[2]), int(sys.argv[3]))))
elif (sys.argv[4].lower().strip() == globals.arg_show):
    ui.ShowMaze(ui.GetMaze(sys.argv[1], (int(sys.argv[2]), int(sys.argv[3]))))
else:
    print(globals.wrong_start_message)
    