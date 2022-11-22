import sys

import src.user_interaction as ui

if (sys.argv[4].lower() == "play"):
    print("hey")
    ui.PlayGame(ui.GetMaze(sys.argv[1], (int(sys.argv[2]), int(sys.argv[3]))))
elif (sys.argv[4].lower().strip() == "show"):
    ui.ShowMaze(ui.GetMaze(sys.argv[1], (int(sys.argv[2]), int(sys.argv[3]))))
    