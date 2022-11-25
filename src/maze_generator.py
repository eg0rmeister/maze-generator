import pickle
import random

import assets.globals as globals


def GetWall(walls: int) -> str:
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
        return globals.wall_s  # █


def GetPath(walls: int) -> str:
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
        return globals.W_s
    if (walls == 0b0010):
        return globals.S_s
    if (walls == 0b0011):
        return globals.SW_s
    if (walls == 0b0100):
        return globals.E_s
    if (walls == 0b0101):
        return globals.EW_s
    if (walls == 0b0110):
        return globals.ES_s
    if (walls == 0b1000):
        return globals.N_s
    if (walls == 0b1001):
        return globals.NW_s
    if (walls == 0b1010):
        return globals.NS_s
    if (walls == 0b1100):
        return globals.NE_s


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

    def GetSimpleWall(self, x, y):
        """Returns wall symbol for specific position of the maze"""

        top = 0
        right = 0
        bottom = 0
        left = 0
        if x != 0:
            top = self._cells[x - 1][y] != 0
        if y != 2 * self.width:
            right = self._cells[x][y + 1] != 0
        if x != 2 * self.height:
            bottom = self._cells[x + 1][y] != 0
        if y != 0:
            left = self._cells[x][y - 1] != 0
        return GetWall((top << 3) +
                       (right << 2) +
                       (bottom << 1) +
                       (left << 0))

    def ShowGame(self) -> None:
        """Prints the current state of the game to the console"""

        for i in range(2 * self.height + 1):
            for j in range(2 * self.width + 1):
                if self._cells[i][j] == 0:
                    if self._player_position[0] == i and self._player_position[1] == j:
                        print(globals.player_s, end='')
                    else:
                        print(' ', end='')
                else:
                    print(self.GetSimpleWall(i, j), end='')
            print()

    def Show(self) -> None:
        """Prints the maze to the console"""

        for i in range(2 * self.height + 1):
            for j in range(2 * self.width + 1):
                if self._cells[i][j] == 0:
                    print(' ', end='')
                else:
                    print(self.GetSimpleWall(i, j), end='')

            print()

    def GetWays(self, pos, visited):
        """
            Returns where you can go directly from given position
            without going anywhere already in visited. Does not care about walls.
        """

        to_north = (pos[0] - 2, pos[1])
        to_east = (pos[0], pos[1] + 2)
        to_south = (pos[0] + 2, pos[1])
        to_west = (pos[0], pos[1] - 2)
        can_visit = []

        if (to_north[0] > 0 and to_north not in visited):
            can_visit.append(to_north)
        if (to_east[1] < 2 * self.width and to_east not in visited):
            can_visit.append(to_east)
        if (to_south[0] < 2 * self.height and to_south not in visited):
            can_visit.append(to_south)
        if (to_west[1] > 0 and to_west not in visited):
            can_visit.append(to_west)
        return can_visit

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
                temp = True
                for cell in self.GetWays(stack[-1], visited):
                    if (self._cells[(stack[-1][0] + cell[0]) // 2]
                                   [(stack[-1][1] + cell[1]) //2] == 0):
                        to_visit = cell
                        temp = False
                        break
                if temp:
                    stack.pop()
                    stack_len -= 1
                    continue
                stack_len += 1
                stack.append(to_visit)
                visited.add(to_visit)
                if to_visit == self._end:
                    solution = tuple(((i[0] + 1) >> 1, (i[1] + 1) >> 1)
                                     for i in stack)
                    self._solution = solution
                    return solution
            raise Exception("No solution")
        else:
            return self._solution

    def GetSolutionCell(self, x, y, solution, indexes):
        """
            Returns solution cell symbol if cell in solution
            or empty cell symbol instead
        """

        if (x, y) in solution:
            index = indexes[(x, y)]
            top = ((index > 0 and
                    (x - 1, y) == solution[index-1]) or
                   (index < len(solution) - 1 and
                    (x - 1, y) == solution[index+1]))
            right = ((index > 0 and
                      (x, y + 1) == solution[index-1]) or
                     (index < len(solution) - 1 and
                      (x, y + 1) == solution[index+1]))
            bottom = ((index > 0 and
                       (x + 1, y) == solution[index-1]) or
                      (index < len(solution) - 1 and
                       (x + 1, y) == solution[index+1]))
            left = ((index > 0 and
                     (x, y - 1) == solution[index-1]) or
                    (index < len(solution) - 1 and
                     (x, y - 1) == solution[index+1]))
            return GetPath((top << 3) + (right << 2) + (bottom << 1) +
                           (left << 0))
        return ' '

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
                    print(self.GetSolutionCell(i, j, solution, indexes),
                          end='')
                else:
                    print(self.GetSimpleWall(i, j), end='')
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
            can_visit = self.GetWays(stack[-1], visited)
            if len(can_visit) == 0:
                stack.pop()
                stack_len -= 1

            else:
                to_visit = random.choice(can_visit)
                self._cells[(stack[-1][0] + to_visit[0]) //
                            2][(stack[-1][1] + to_visit[1])//2] = 0
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

    def Unseparate(self, wall, cells):
        """Deletes wall if two cells it separates are in different groups"""
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
            self.Unseparate(wall, cells)
        self._cells[0][1] = 0
        self._cells[2 * self.height][2 * self.width - 1] = 0
