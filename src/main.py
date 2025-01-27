from window import *
from maze import *

def main():
    win = Window(800, 600)

    win.draw_line(Line(Point(1,1), Point(100,100)), fill_colour="red")

    test_cell = Cell(Point(200,200), Point(300,300), win)
    test_cell2 = Cell(Point(300,200), Point(400,300), win)

    test_cell.draw()
    test_cell2.draw()

    win.wait_for_close()

if __name__ == "__main__":
    main()