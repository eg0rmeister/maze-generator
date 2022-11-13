import random


# bit representation is used to deduce the neighbours of the cell
# ES - 1st, 2nd bits of the description cell
# if the bit is 0, there is no wall between cells

# symbols for drawing
N_s = chr(9589) # ╵
E_s = chr(9590) # ╶
S_s = chr(9591) # ╷
W_s = chr(9588) # ╴

NE_s = chr(9492) # └
NS_s = chr(9474) # │
NW_s = chr(9496) # ┘
ES_s = chr(9484) # ┌
EW_s = chr(9472) # ─
SW_s = chr(9488) # ┐

NES_s = chr(9500) # ├
NEW_s = chr(9524) # ┴
NSW_s = chr(9508) # ┤
ESW_s = chr(9516) # ┬

NESW_s = chr(9532) # ┼

def getWall(walls):
    # input is binary number NESW
    # first bit says if there is wall to the north
    # second bit says if there is wall to the east
    # third bit says if there is wall to the south
    # fourth bit says if there is wall to the west

    if (walls == 0b0000):
        return ' '
    if (walls == 0b0001):
        return W_s
    if (walls == 0b0010):
        return S_s
    if (walls == 0b0011):
        return SW_s
    if (walls == 0b0100):
        return E_s
    if (walls == 0b0101):
        return EW_s
    if (walls == 0b0110):
        return ES_s
    if (walls == 0b0111):
        return ESW_s
    if (walls == 0b1000):
        return N_s
    if (walls == 0b1001):
        return NW_s
    if (walls == 0b1010):
        return NS_s
    if (walls == 0b1011):
        return NSW_s
    if (walls == 0b1100):
        return NE_s
    if (walls == 0b1101):
        return NEW_s
    if (walls == 0b1110):
        return NES_s
    if (walls == 0b1111):
        return NESW_s

class Maze:
    __width = 0
    def get_width(self):
        return self.__width
    width = property(get_width)
    
    __height = 0
    def get_height(self):
        return self.__height
    height = property(lambda self: self.__height)
    
    def __init__(self, width, height):
        if (width < 2 or height < 2):
            raise Exception
        self.__height = height
        self.__width = width
    
    def GenerateMaze(self):
        raise NotImplementedError
    
    def ShowMaze(self):
        raise NotImplementedError
