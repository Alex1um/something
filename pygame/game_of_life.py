import pygame
import random
import time

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
            pygame.draw.ellipse(screen, color, (self.x + self.border + 2,
                                                self.y + self.border + 2,
                                                self.w - self.border * 2 - 4,
                                                self.h - self.border * 2 - 4),
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
            self.on_click(cell)


class Life(Board):

    class Cell(Board.Cell):

        def __init__(self,
                     sizex,
                     sizey,
                     x,
                     y,
                     color=(0, 0, 0),
                     border_color=(255, 255, 255),
                     border=1):
            super().__init__(
                sizex,
                sizey,
                x,
                y,
                color=color,
                border_color=border_color,
                border=border)
            self.alive = 0

        def paint(self, screen):
            if self.alive:
                self.set_color((0, 255, 0))
            else:
                self.set_color((0, 0, 0))
            super().paint(screen)

    def __init__(self,
                 cell_count_x,
                 cell_count_y,
                 cell_size_x=50,
                 cell_size_y=None,
                 x=0,
                 y=0,
                 cell_color=(0, 0, 0),
                 border_color=(255, 255, 255),
                 border=2):
        super().__init__(cell_count_x,
                         cell_count_y,
                         cell_size_x=cell_size_x,
                         cell_size_y=cell_size_y,
                         x=x,
                         y=y,
                         cell_color=cell_color,
                         border_color=border_color,
                         border=border,
                         cell=self.Cell)
        self.enabled = False

    def on_click(self, cell: Cell):
        cell.set_color((0, abs(255 - cell.color[1]), 0))
        cell.alive = not cell.alive

    def next_move(self):
        if self.enabled:
            ly = len(self.cells)
            lx = len(self.cells[0])
            new_lst = [[0] * lx for _ in ' ' * ly]
            cx, cy = self.width // self.cell_size_x, self.height // self.cell_size_y
            for y in range(ly):
                for x in range(lx):
                    cells_around = 0
                    if self.cells[y - 1][x].alive:
                        cells_around += 1
                    if self.cells[y - 1][x - 1].alive:
                        cells_around += 1
                    if self.cells[y - 1][(x + 1) % cx].alive:
                        cells_around += 1
                    if self.cells[(y + 1) % cy][x].alive:
                        cells_around += 1
                    if self.cells[(y + 1) % cy][x - 1].alive:
                        cells_around += 1
                    if self.cells[(y + 1) % cy][(x + 1) % cx].alive:
                        cells_around += 1
                    if self.cells[y][x - 1].alive:
                        cells_around += 1
                    if self.cells[y][(x + 1) % cx].alive:
                        cells_around += 1

                    if not (t := self.cells[y][x].alive):
                        if cells_around in B:
                            new_lst[y][x] = t + 1
                        else:
                            self.cells[y][x].alive = 0
                    elif self.cells[y][x].alive < C:
                        if cells_around in S:
                            new_lst[y][x] = t + 1
                        else:
                            self.cells[y][x].alive = 0
                    else:
                        self.cells[y][x].alive = 0
            for y in range(ly):
                for x in range(lx):
                    self.cells[y][x].alive = new_lst[y][x]


rulestring = "B13/S2/C21"
try:
    B = set(map(int, list(rulestring.split('/')[0][1:])))
except IndexError:
    B = set([-1])
try:
    S = set(map(int, list(rulestring.split('/')[1][1:])))
except IndexError:
    S = set([-1])
try:
    C = int(rulestring.split('/')[2][1:])
except Exception:
    C = -1
print(B, S, C)
pygame.init()

sizex, sizey = 600, 600
frames = 30
base_color = (0, 0, 0)
screen = pygame.display.set_mode((sizex, sizey))
screen.fill(base_color)

pygame.display.flip()
clock = pygame.time.Clock()

life = Life.init_with_cell_size(600,
                                  600,
                                  cell_size_x=5,
                                  cell_color=(0, 0, 0),
                                  border_color=(255, 255, 255),
                                  border=-1)

while 1:
    screen.fill(base_color)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.dict['button'] == 1:
                life.get_click(e.dict['pos'])
            elif e.dict['button'] == 3:
                life.enabled = not life.enabled
            elif e.dict['button'] == 4:
                if frames > 2:
                    frames -= 1
            elif e.dict['button'] == 5:
                frames += 1
        elif e.type == pygame.KEYDOWN and e.dict['key'] == 32:
            life.enabled = not life.enabled
    life.next_move()
    life.render(screen)
    pygame.display.flip()
    clock.tick(frames)
