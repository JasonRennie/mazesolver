import time
from window import *
import random

class Cell():
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win
        self._visited = False

    def draw(self, x1, y1, x2, y2):
        if not self._win:
            return
        
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "black")
        else:
            self._win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "white")
        if self.has_left_wall:
            self._win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "black")
        else:
            self._win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "white")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "black")
        else:
            self._win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "white")
        if self.has_top_wall:
            self._win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "black")
        else:
            self._win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "white")

    def draw_move(self, to_cell, undo=False):
        colour = "red"
        if undo:
            colour = "gray"

        x1 = (self._x1+self._x2)/2
        y1 = (self._y1+self._y2)/2
        x2 = (to_cell._x1+to_cell._x2)/2
        y2 = (to_cell._y1+to_cell._y2)/2
        self._win.draw_line(Line(Point(x1,y1), Point(x2,y2)), colour)


class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            new_col = []
            for j in range(self._num_rows):
                new_col.append(Cell(self._win))
            self._cells.append(new_col)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
                

    def _draw_cell(self, i, j):
        if not self._win:
            return
        
        topleft = Point(
            self._x1 + i*self._cell_size_x,
            self._y1 + j*self._cell_size_y
        )
        bottomright = Point(
            self._x1 + (i+1)*self._cell_size_x,
            self._y1 + (j+1)*self._cell_size_y
        )
        
        self._cells[i][j].draw(topleft.x, topleft.y, bottomright.x, bottomright.y)
        self._animate()


    def _animate(self):
        if not self._win:
            return
        self._win.redraw()
        time.sleep(0.05)


    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[self._num_cols-1][self._num_rows-1].has_bottom_wall = False

        self._draw_cell(0, 0)
        self._draw_cell(self._num_cols-1, self._num_rows-1)

    
    def is_valid_cell(self, i, j):
        max_x = len(self._cells)-1
        max_y = len(self._cells[0])-1
        return (0 <= i <= max_x and 
                0 <= j <= max_y and 
                not self._cells[i][j]._visited)
    

    def _break_walls_r(self, i, j):
        self._cells[i][j]._visited = True
        while True:
            to_visit = []
            # right, down, left, up
            dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

            for d in dirs:
                if self.is_valid_cell(i+d[0], j+d[1]):
                    to_visit.append(d)
            
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            
            random_dir = to_visit[random.randrange(0, len(to_visit))]
            new_i, new_j = i+random_dir[0], j+random_dir[1]

            if random_dir == dirs[0]:
                self._cells[i][j].has_right_wall = False
                self._cells[new_i][new_j].has_left_wall = False
            elif random_dir == dirs[1]:
                self._cells[i][j].has_bottom_wall = False
                self._cells[new_i][new_j].has_top_wall = False
            elif random_dir == dirs[2]:
                self._cells[i][j].has_left_wall = False
                self._cells[new_i][new_j].has_right_wall = False
            elif random_dir == dirs[3]:
                self._cells[i][j].has_top_wall = False
                self._cells[new_i][new_j].has_bottom_wall = False

            self._break_walls_r(new_i, new_j)

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell._visited = False


    def path_is_clear(self, i, j, d):
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        new_i, new_j = i+d[0], j+d[1]

        if d == dirs[0]:
            return (self._cells[i][j].has_right_wall == False and
                    self._cells[new_i][new_j].has_left_wall == False)
        elif d == dirs[1]:
            return (self._cells[i][j].has_bottom_wall == False and
                    self._cells[new_i][new_j].has_top_wall == False)
        elif d == dirs[2]:
            return (self._cells[i][j].has_left_wall == False and
                    self._cells[new_i][new_j].has_right_wall == False)
        elif d == dirs[3]:
            return (self._cells[i][j].has_top_wall == False and
                    self._cells[new_i][new_j].has_bottom_wall == False)

    
    def solve(self):
        return self._solve_r(0, 0)


    def _solve_r(self, i, j):
        print(i, j)
        self._animate()
        self._cells[i][j]._visited = True
        if i==self._num_cols-1 and j==self._num_rows-1:
            return True
        
        # Solve maze
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for d in dirs:
            new_i, new_j = i+d[0], j+d[1]
            print(f"- {new_i} {new_j} {self.is_valid_cell(new_i, new_j)} {self.path_is_clear(i, j, d)}")
            if self.is_valid_cell(new_i, new_j) and self.path_is_clear(i, j, d):
                self._cells[i][j].draw_move(self._cells[new_i][new_j])
                solved = self._solve_r(new_i, new_j)
                if solved:
                    return True
                self._cells[i][j].draw_move(self._cells[new_i][new_j], undo=True)
        return False
