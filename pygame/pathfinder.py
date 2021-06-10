import pygame
import random
import time
from threading import Thread

class Board:

    class Cell:

        def __init__(self,
                     sizex,
                     sizey,
                     x,
                     y,
                     color=(0, 0, 0),
                     border_color=(255, 255, 255),
                     border=1):
            self.w, self.h = sizex, sizey
            self.x, self.y = x, y
            self.color = color
            self.border_color = border_color
            self.border = border

        def paint(self, screen):
            pygame.draw.rect(screen,
                             self.color,
                             (
                                 self.x + self.border,
                                 self.y + self.border,
                                 self.w - self.border * 2,
                                 self.h - self.border * 2
                             )
                             )
            pygame.draw.rect(screen,
                             self.border_color,
                             (
                                 self.x,
                                 self.y,
                                 self.w,
                                 self.h
                             ),
                             self.border
                             )

        def test_for_click(self, x, y):
            return self.x <= x <= self.x + self.w and\
                   self.y <= y <= self.y + self.h

        def set_geometry(self, x, y, w, h):
            self.x, self.y = x, y
            self.w, self.h = w, h

        def __str__(self):
            return f'({self.x}, {self.y})'

        def set_color(self, color):
            self.color = color

        def set_border_color(self, border_color):
            self.border_color = border_color

        def draw_o(self, color, w=2):
            global screen
            pygame.draw.rect(screen, color, (self.x + self.border,
                                                self.y + self.border,
                                                self.w - self.border * 2 - 1,
                                                self.h - self.border * 2 - 1),
                                w)

    def __init__(self,
                 cell_count_x,
                 cell_count_y,
                 cell_size_x=50,
                 cell_size_y=None,
                 x=0,
                 y=0,
                 cell_color=(0, 0, 0),
                 border_color=(255, 255, 255),
                 border=2,
                 cell=None):
        self.toe = False
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y if cell_size_y is not None else cell_size_x
        self.width = cell_count_x * self.cell_size_x
        self.height = self.cell_size_y * cell_count_y
        self.x, self.y = x, y
        self.border_color = border_color
        self.border = border
        if cell is None:
            self.cells = [[self.Cell(self.cell_size_x,
                                     self.cell_size_y,
                                     i,
                                     j,
                                     cell_color,
                                     border_color,
                                     border)
                           for i in range(x, self.width + x, self.cell_size_x)]
                          for j in range(y, self.height + y, self.cell_size_y)]
        else:
            self.cells = [[cell(self.cell_size_x,
                                     self.cell_size_y,
                                     i,
                                     j,
                                     cell_color,
                                     border_color,
                                     border)
                           for i in range(x, self.width + x, self.cell_size_x)]
                          for j in range(y, self.height + y, self.cell_size_y)]

    @classmethod
    def init_with_cell_count(cls,
                             size_x,
                             size_y,
                             count_x,
                             count_y,
                             x=0,
                             y=0,
                             cell_color=(0, 0, 0),
                             border_color=(255, 255, 255),
                             border=2):
        cells_x = size_x // count_x
        cells_y = size_y // count_y
        return cls(cells_x,
                   cells_y,
                   count_x,
                   count_y,
                   x,
                   y,
                   cell_color,
                   border_color,
                   border)

    @classmethod
    def init_with_cell_size(cls, size_x,
                            size_y,
                            cell_size_x,
                            cell_size_y=None,
                            x=0,
                            y=0,
                            cell_color=(0, 0, 0),
                            border_color=(255, 255, 255),
                            border=2):
        return cls(size_x // cell_size_x,
                   size_y // cell_size_y if cell_size_y is not None else size_y // cell_size_x,
                   cell_size_x,
                   cell_size_y,
                   x,
                   y,
                   cell_color,
                   border_color,
                   border)

    def render(self, screen):
        for row in self.cells:
            for col in row:
                col.paint(screen)

    def set_view(self, x, y, cell_size_x, cell_size_y=None):
        self.x, self.y = x, y
        ix, iy = x, y
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y if cell_size_y is not None else cell_size_x
        for row in self.cells:
            ix = x
            for col in row:
                col.set_geometry(ix,
                                 iy,
                                 self.cell_size_x,
                                 self.cell_size_y)
                ix += self.cell_size_x
            iy += self.cell_size_y

    def get_cell(self, mouse_pos):
        for row in self.cells:
            for col in row:
                if col.test_for_click(*mouse_pos):
                    return col
        return None

    def on_click(self, cell: Cell):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            Thread(target=self.on_click, args=[cell]).start()
            # self.on_click(cell)


class Lines(Board):

    class Cell(Board.Cell):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.ball = None

        def paint(self, screen):
            super().paint(screen)
            if self.ball is not None:
                self.draw_o((255, 0, 0) if self.ball else (0, 0, 255), w=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, cell=self.Cell)
        self.run = True
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                if matrix[y][x]:
                    self.cells[y][x].ball = False
        self.red = None
        self.way = []
        self.way_index = 0
        self.cell = None

    def on_click(self, cell: Cell):
        if cell.ball is None:
            if self.red:
                a = self.has_path(self.red.x, self.red.y, cell.x, cell.y)
                if a:
                    self.red.ball = None
                    self.red = None
                    # self.cells[a[-1][1]][a[-1][0]].draw_o((255, 0, 0), 0) # teleport
                    for x, y in a:
                        self.render(screen)
                        self.cells[y][x].draw_o((255, 0, 0), 0)
                        pygame.display.flip()
                        time.sleep(0.05)
                    cell.ball = False
            else:
                cell.ball = False
        elif cell.ball:
            cell.ball = False
            self.red = None
        else:
            cell.ball = True
            self.red = cell
        self.render(screen)
        pygame.display.flip()

    def has_path(self, x1, y1, x2, y2):
        id1x = (x1 - self.x) // self.cell_size_x
        id1y = (y1 - self.y) // self.cell_size_y
        id2x = (x2 - self.x) // self.cell_size_x
        id2y = (y2 - self.y) // self.cell_size_y
        # right_way = []

        def find_way(way):
            # nonlocal right_way
            if way[-1] == (id2x, id2y):
                right_way = way
                return way
            else:
                x, y = way[-1]
                for x, y in (
                        (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    try:
                        if x > -1 and y > -1 and self.cells[y][x].ball is None and (x, y) not in way:
                            return find_way(way + [(x, y)])
                    except IndexError:
                        pass

        def find_way2():
            sy, sx = self.height // self.cell_size_y, self.width // self.cell_size_x
            num_map = [0] * sy
            for i in range(len(num_map)):
                num_map[i] = [-1] * sx
            nums = [(id1x, id1y)]
            num_map[id1y][id1x] = 0
            d = 0
            while nums:
                new_nums = []
                d += 1
                for x, y in nums:
                    for x1, y1 in (
                            (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if sx > x1 > -1 and sy > y1 > -1 and num_map[y1][x1] == -1 and self.cells[y1][x1].ball is None:
                            num_map[y1][x1] = d
                            new_nums.append((x1, y1))
                nums = new_nums
            way = [(id2x, id2y)]
            for i in range(num_map[id2y][id2x] - 1, -1, -1):
                x, y = way[-1]
                for x1, y1 in (
                    (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if sx > x1 > -1 and sy > y1 > -1 and num_map[y1][x1] == i:
                        way.append((x1, y1))
                        break
            if len(way) == 1:
                way = []
            return way[::-1]

        right_way = find_way2()
        # right_way = find_way([(id1x, id1y)])
        return right_way


pygame.init()

sizex, sizey = 700, 700
frames = 30
base_color = (0, 0, 0)
screen = pygame.display.set_mode((sizex, sizey))
screen.fill(base_color)

pygame.display.flip()
clock = pygame.time.Clock()

file = input()
with open(file, 'rb') as f:
    import pickle
    matrix = pickle.load(f)

# board = Lines.init_with_cell_count(sizex, sizey, len(matrix), len(matrix[0]), border=1)
board = Lines(len(matrix[0]), len(matrix), 14, 14, border=1)
board.render(screen)
pygame.display.flip()
end = False
while 1:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            end = True
            break
        elif e.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(e.dict['pos'])
    if end:
        break
    # screen.fill(base_color)

    board.render(screen)
    # pygame.display.flip()
    clock.tick(frames)
pygame.quit()