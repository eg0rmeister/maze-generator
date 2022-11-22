import pickle
import random

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


def getWall(walls: int) -> str:
    """
     Input is binary number NESW.
     First bit says if there is wall to the north.
     Second bit says if there is wall to the east.
     Third bit says if there is wall to the south.
     Fourth bit says if there is wall to the west.
     Returns corresponding wall type.
    """

    if (walls == 0):
        return ' '
    else:
        return wall_s  # █


def getPath(walls: int) -> str:
    """
     Input is binary number NESW.
     First bit says if there is path to the north.
     Second bit says if there is path to the east.
     Third bit says if there is path to the south.
     Fourth bit says if there is path to the west.
     Returns path symbol connecting corresponding parts.
    """
    
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
    if (walls == 0b1000):
        return N_s
    if (walls == 0b1001):
        return NW_s
    if (walls == 0b1010):
        return NS_s
    if (walls == 0b1100):
        return NE_s


class Maze:
    """Base class for all mazes"""

    _width = 0

    def GetWidth(self) -> int:
        """Returns width of maze"""
        return self._width

    width = property(GetWidth)

    _height = 0

    def GetHeight(self) -> int:
        """Returns height of maze"""
        return self._height

    height = property(GetHeight)

    def __init__(self, width=1, height=1) -> None:
        self.Generate(width, height)

    def Generate(self, width=1, height=1) -> None:
        """
         Generates a maze full of walls.
         Also initializes start position, end position,
         player position, width, height, solution.
         Checks width and height for correctness,
         raising exception if any of them is less, than 1
        """

        if width < 1 or height < 1:
            raise Exception("Maze cannot have a dimension of less than 1")
        self._start = (1, 1)
        self._end = (2 * height - 1, 2 * width - 1)
        self._player_position = list(self._start)
        self._solution = None
        self._height = height
        self._width = width
        self._cells = [[2 for i in range(2 * self.width + 1)]]
        for i in range(2 * self.height - 1):
            self._cells.append([2])
            for j in range(2 * self.width - 1):
                self._cells[-1].append(1 if i & 1 or j & 1 else 0)
            self._cells[-1].append(2)
        self._cells.append([2 for i in range(2 * self.width + 1)])

    def Save(self, filename: str) -> None:
        """Saves the maze state to the file"""

        with open(filename, "wb+") as file:
            pickle.dump(self, file)

    def Load(self, filename: str) -> None:
        """Loads the maze state from the file """

        with open(filename, "rb") as file:
            temp = pickle.load(file)
        self._cells = temp._cells
        self._end = temp._end
        self._height = temp._height
        self._player_position = temp._player_position
        self._solution = temp._solution
        self._start = temp._start
        self._width = temp._width

    def Resize(self, width: int, height: int, generate=True) -> None:
        """Regenerates the maze with new dimensions"""

        self.Generate(width, height, generate)

    def ShowGame(self) -> None:
        """Prints the current state of the game to the console"""

        for i in range(2 * self.height + 1):
            for j in range(2 * self.width + 1):
                if self._cells[i][j] == 0:
                    if self._player_position[0] == i and self._player_position[1] == j:
                        print(player_s, end='')
                    else:
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

    def Show(self) -> None:
        """Prints the maze to the console"""

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

    def Solve(self) -> tuple:
        """
         Returns the sequence of moves required to do to beat the maze, 
         tries to find saved solution, if there isn't any, uses DFS to solve it.
        """

        if self._solution == None:
            visited = set([self._start])
            stack = [self._start]
            stack_len = 1
            while stack_len != 0:
                to_north = (stack[-1][0] - 2, stack[-1][1])
                to_east = (stack[-1][0], stack[-1][1] + 2)
                to_south = (stack[-1][0] + 2, stack[-1][1])
                to_west = (stack[-1][0], stack[-1][1] - 2)
                if (to_north[0] > 0 and
                        to_north not in visited and
                        self._cells[stack[-1][0] - 1][stack[-1][1]] == 0):
                    to_visit = to_north
                elif (to_east[1] < 2 * self.width and
                      to_east not in visited and
                      self._cells[stack[-1][0]][stack[-1][1] + 1] == 0):
                    to_visit = to_east
                elif (to_south[0] < 2 * self.height and
                      to_south not in visited and
                      self._cells[stack[-1][0] + 1][stack[-1][1]] == 0):
                    to_visit = to_south
                elif (to_west[1] > 0 and
                      to_west not in visited and
                      self._cells[stack[-1][0]][stack[-1][1] - 1] == 0):
                    to_visit = to_west
                else:
                    stack.pop()
                    stack_len -= 1
                    continue
                stack_len += 1
                stack.append(to_visit)
                visited.add(stack[-1])
                if stack[-1] == self._end:
                    solution = tuple(((i[0] + 1) >> 1, (i[1] + 1) >> 1)
                                     for i in stack)
                    self._solution = solution
                    return solution
            raise Exception("No solution")
        else:
            return self._solution

    def ShowSolution(self) -> None:
        """Prints the solution of the maze to the console"""

        solution = [(i[0] * 2 - 1, i[1] * 2 - 1) for i in self.Solve()]
        for i in range(len(solution) - 1):
            solution.insert(2 * i + 1, (solution[2 * i][0] // 2 + solution[2 * i + 1][0] // 2 + 1,
                                        solution[2 * i][1] // 2 + solution[2 * i + 1][1] // 2 + 1))
        solution = tuple(solution)
        indexes = dict(((solution[i], i) for i in range(len(solution))))
        for i in range(2 * self.height + 1):
            for j in range(2 * self.width + 1):
                if self._cells[i][j] == 0:
                    if (i, j) in solution:
                        index = indexes[(i, j)]
                        top = ((index > 0 and
                                (i - 1, j) == solution[index-1]) or
                               (index < len(solution) - 1 and
                                (i - 1, j) == solution[index+1]))
                        right = ((index > 0 and
                                  (i, j + 1) == solution[index-1]) or
                                 (index < len(solution) - 1 and
                                  (i, j + 1) == solution[index+1]))
                        bottom = ((index > 0 and
                                   (i + 1, j) == solution[index-1]) or
                                  (index < len(solution) - 1 and
                                   (i + 1, j) == solution[index+1]))
                        left = ((index > 0 and
                                 (i, j - 1) == solution[index-1]) or
                                (index < len(solution) - 1 and
                                 (i, j - 1) == solution[index+1]))
                        print(getPath((top << 3) +
                                      (right << 2) +
                                      (bottom << 1) +
                                      (left << 0)), end='')
                    else:
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

    def GameStatus(self) -> bool:
        """Returns True if player is on the end tile"""

        return (self._player_position[0] == self._end[0] and
                self._player_position[1] == self._end[1])

    status = property(GameStatus)

    def Move(self, move: str) -> bool:
        """Changes player position according to the input"""

        if move.lower() == 'w':
            if (self._player_position[0] != 1 and
                    self._cells[self._player_position[0] - 1][self._player_position[1]] == 0):
                self._player_position[0] -= 2
                return True
            return False
        if move.lower() == 'd':
            if (self._player_position[1] != 2 * self.width - 1 and
                    self._cells[self._player_position[0]][self._player_position[1] + 1] == 0):
                self._player_position[1] += 2
                return True
            return False
        if move.lower() == 's':
            if (self._player_position[0] != 2 * self.height - 1 and
                    self._cells[self._player_position[0] + 1][self._player_position[1]] == 0):
                self._player_position[0] += 2
                return True
            return False
        if move.lower() == 'a':
            if (self._player_position[1] != 1 and
                    self._cells[self._player_position[0]][self._player_position[1] - 1] == 0):
                self._player_position[1] -= 2
                return True
            return False
        return False


class DFSMaze(Maze):
    """Maze using DFS to generate"""

    def Generate(self, width=0, height=0) -> None:
        """Generates maze using DFS"""

        super().Generate(width, height)
        visited = set([self._start])
        stack = [self._start]
        stack_len = 1
        while stack_len != 0:
            if stack[-1] == self._end:
                self._solution = tuple(((i[0] + 1) >> 1, (i[1] + 1) >> 1)
                                       for i in stack)
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


class SpanningTreeMaze(Maze):
    """Maze using minimal spanning tree method to generate"""

    class __ref:
        """Class for referencing other instanves of it"""
        __refs = None

        def __init__(self, refs=None):
            self.__refs = refs

        def GetRef(self):
            """
             Returns the 'root of the reference tree' --
             first instance of __ref, that references to None on the reference path
            """
            if self.__refs == None:
                return self
            else:
                return self.__refs.ref

        def SetRef(self, newRef):
            """
             Makes the 'root of the reference tree' reference
             to newRef instead of None
            """
            if (self.__refs == None):
                self.__refs = newRef
            else:
                self.__refs.ref = newRef
                self.__refs = newRef

        ref = property(GetRef, SetRef)

    def Generate(self, width=1, height=1) -> None:
        """Generates new maze by making the minimal spanning tree of cells"""
        
        super().Generate(width, height)
        walls = []
        cells = dict()
        for i in range(1, 2 * self.height):
            for j in range(1, 2 * self.width):
                if ((i & 1) ^ (j & 1)):
                    walls.append((i, j))
                elif (((i & 1) & (j & 1))):
                    cells[(i, j)] = self.__ref()
        random.shuffle(walls)
        for wall in walls:
            if wall[0] & 1:
                if (
                    cells[(wall[0], wall[1] - 1)].ref !=
                    cells[(wall[0], wall[1] + 1)].ref
                ):
                    self._cells[wall[0]][wall[1]] = 0
                    cells[(wall[0], wall[1] - 1)].ref = (
                        cells[(wall[0], wall[1] + 1)].ref)
            else:
                if (
                    cells[(wall[0] - 1, wall[1])].ref !=
                    cells[(wall[0] + 1, wall[1])].ref
                ):
                    self._cells[wall[0]][wall[1]] = 0
                    cells[(wall[0] - 1, wall[1])].ref = (
                        cells[(wall[0] + 1, wall[1])].ref)
        self._cells[0][1] = 0
        self._cells[2 * self.height][2 * self.width - 1] = 0
