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

