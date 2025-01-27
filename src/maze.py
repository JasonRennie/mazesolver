from window import *

class Cell():
    def __init__(self, point1, point2, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = point1.x
        self._x2 = point2.x
        self._y1 = point1.y
        self._y2 = point2.y
        self._win = win

    def draw(self):
        x1, x2, y1, y2 = self._x1, self._x2, self._y1, self._y2
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "black")
        if self.has_left_wall:
            self._win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "black")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "black")
        if self.has_top_wall:
            self._win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "black")

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
    def __init__(self):
        pass
