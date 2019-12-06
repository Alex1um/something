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
                     border=1,
                     cls=None):
            self.w, self.h = sizex, sizey
            self.x, self.y = x, y
            self.color = color
            self.border_color = border_color
            self.border = border
            self.cls = cls

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

        def get_coords(self):
            return self.x, self.y

        def get_indexes(self):
            return self.x // self.w, self.y // self.h

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
        self.dir = None

        self.hero = (0, 0)
        self.crystals = set()
        self.monsters = set()
        self.block = set()
        self.meshes = []
        self.border_blocks = set()
        with open('map.area', 'r') as f:
            m = eval(f.read())
            for y in range(len(m)):
                for x in range(len(m[0])):
                    if m[y][x] == 2:
                        self.block.add((x, y))
                    elif m[y][x] == 1:
                        self.border_blocks.add((x, y))
                    elif m[y][x] == 3:
                        self.crystals.add((x, y))
                    elif m[y][x] == 4:
                        self.meshes.append((x, y))
                    elif m[y][x] == 5:
                        self.hero = (x, y)
                    elif m[y][x] == 6:
                        self.monsters.add((x, y))
        self.mesh_info = [[0, 0]] * len(self.meshes)
        print(self.mesh_info1)
        self.dirrections = {'up': (0, 1), 'down': (0, -1), 'left': (-1, 0), 'right': (1, 0), None: (0, 0)}
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y if cell_size_y is not None else cell_size_x
        self.width = cell_count_x * self.cell_size_x
        self.height = self.cell_size_y * cell_count_y
        self.x, self.y = x, y
        self.score = 0
        self.border_color = border_color
        self.border = border
        if cell is None:
            self.cells = [[self.Cell(self.cell_size_x,
                                     self.cell_size_y,
                                     i,
                                     j,
                                     cell_color,
                                     border_color,
                                     border,
                                     self)
                           for i in range(x, self.width + x, self.cell_size_x)]
                          for j in range(y, self.height + y, self.cell_size_y)]
        else:
            self.cells = [[cell(self.cell_size_x,
                                self.cell_size_y,
                                i,
                                j,
                                cell_color,
                                border_color,
                                border,
                                self)
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
                pos = col.get_indexes()
                if pos in self.border_blocks:
                    col.set_color((255, 255, 255))
                elif pos == self.hero:
                    col.set_color((255, 0, 0))
                elif pos in self.crystals:
                    col.set_color((0, 255, 0))
                elif pos in self.meshes:
                    col.set_color((245, 222, 179))
                elif pos in self.monsters:
                    col.set_color((0, 0, 255))
                elif pos in self.block:
                    col.set_color((30, 144, 255))
                col.paint(screen)
                col.set_color((0, 0, 0))

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

    def sed_dir(self, dir):
        self.dir = dir

    def make_move(self):
        x, y = self.hero
        xi, yi = self.dirrections[self.dir]
        nx, ny = x + xi, y + yi
        pos = (nx, ny)
        if -1 < nx < self.width // self.cell_size_x and -1 < ny < self.height // self.cell_size_y and pos not in self.border_blocks:
            self.hero = pos
            if pos in self.block:
                self.block.remove(pos)
            if pos in self.crystals:
                self.crystals.remove(pos)
                self.score += 100

    def move_meshes(self):
        # 0: count 1: time
        for i in range(len(self.meshes)):
            x, y = self.meshes[i]
            pos = (x, y + 1)
            if pos not in self.block and pos not in self.crystals and pos not in self.border_blocks:
                if self.mesh_info[i][0]:
                    self.meshes[i] = pos
                    self.mesh_info[i][0] += 1
                elif self.mesh_info[i][1] and time.time() - self.mesh_info[i][1] >= 2:
                    self.meshes[i] = pos
                    self.mesh_info[i][0] += 1
                else:
                    self.mesh_info[i][1] = time.time()
            else:
                if self.mesh_info[i][0]:
                    self.mesh_info[i][0] = 0

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


pygame.init()

sizex, sizey = 500, 800
frames = 10
base_color = (0, 0, 0)
screen = pygame.display.set_mode((sizex, sizey))
screen.fill(base_color)

pygame.display.flip()
clock = pygame.time.Clock()

# board = Board.init_with_cell_size(sizex - 100,
#                                   sizey - 200,
#                                   cell_size_x=50,
#                                   x=50,
#                                   y=100,
#                                   cell_color=(0, 0, 0),
#                                   border_color=(255, 255, 255),
#                                   border=1)
board = Board(10, 10)
while 1:
    screen.fill(base_color)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
        elif e.type == pygame.KEYDOWN:
            if e.dict['key'] == 273:  # down
                board.sed_dir('down')
            elif e.dict['key'] == 276:  # left
                board.sed_dir('left')
            elif e.dict['key'] == 274:  # up
                board.sed_dir('up')
            elif e.dict['key'] == 275:  # right:
                board.sed_dir('right')
        elif e.type == pygame.KEYUP:
            if e.dict['key'] == 273 and board.dir == 'down' or \
                    e.dict['key'] == 276 and board.dir == 'left' or\
                    e.dict['key'] == 274 and board.dir == 'up' or \
                    e.dict['key'] == 275 and board.dir == 'right':
                board.sed_dir(None)
    board.make_move()
    board.move_meshes()
    board.render(screen)
    pygame.display.flip()
    clock.tick(frames)
