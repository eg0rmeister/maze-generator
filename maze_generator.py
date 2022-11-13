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
    _width = 0
    def get_width(self):
        return self._width
    width = property(get_width)
    
    _height = 0
    def get_height(self):
        return self._height
    height = property(get_height)
    
    def __init__(self, width, height):
        if (width < 2 or height < 2):
            raise Exception
        self._height = height
        self._width = width
        self._cells = [[2 for i in range(2 * self.width + 1)]]
        for i in range(2 * self.height - 1):
            self._cells.append([2])
            for j in range(2 * self.width - 1):
                self._cells[-1].append(1 if i & 1 or j & 1 else 0)
            self._cells[-1].append(2)
        self._cells.append([2 for i in range(2 * self.width + 1)])
    
    def GenerateMaze(self):
        raise NotImplementedError
    
    def ShowMaze(self):
        for i in range(2 * self.height + 1):
            for j in range(2 * self.width + 1):
                if self._cells[i][j] == 0:
                    print(' ', end='')
                else:
                    top = 0
                    right = 0
                    bottom = 0
                    left = 0
                    if i != 0:
                        top = self._cells[i - 1][j] != 0
                    if j != 2 * self.width:
                        right = self._cells[i][j + 1] != 0
                    if i != 2 * self.height:
                        bottom = self._cells[i + 1][j] != 0
                    if j != 0:
                        left = self._cells[i][j - 1] != 0
                    print(getWall((top << 3) +
                                  (right << 2) +
                                  (bottom << 1) +
                                  (left << 0)), end='')
            print()
                    
class DFSMaze(Maze):
    def GenerateMaze(self):
        visited = set((1, 1))
        stack = [(1, 1)]
        stack_len = 1
        while stack_len != 0:
            can_visit = []
            to_north = (stack[-1][0] - 2, stack[-1][1])
            to_east = (stack[-1][0], stack[-1][1] + 2)
            to_south = (stack[-1][0] + 2, stack[-1][1])
            to_west = (stack[-1][0], stack[-1][1] - 2)
            
            if (to_north[0] > 0 and to_north not in visited):
                can_visit.append(to_north)
            if (to_east[1] < 2 * self.width and to_east not in visited):
                can_visit.append(to_east)
            if (to_south[0] < 2 * self.height and to_south not in visited):
                can_visit.append(to_south)
            if (to_west[1] > 0 and to_west not in visited):
                can_visit.append(to_west)
            if len(can_visit) == 0:
                stack.pop()
                stack_len -= 1
            else:
                to_visit = random.choice(can_visit)
                if (to_visit == to_north):
                    self._cells[stack[-1][0] - 1][stack[-1][1]] = 0
                if (to_visit == to_east):
                    self._cells[stack[-1][0]][stack[-1][1] + 1] = 0
                if (to_visit == to_south):
                    self._cells[stack[-1][0] + 1][stack[-1][1]] = 0
                if (to_visit == to_west):
                    self._cells[stack[-1][0]][stack[-1][1] - 1] = 0
                stack_len += 1
                stack.append(to_visit)
                visited.add(stack[-1])
        self._cells[0][1] = 0
        self._cells[2 * self.height][2 * self.width - 1] = 0
