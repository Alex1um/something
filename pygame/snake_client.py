import socket
import struct
import time
import pickle
import pygame
from threading import Thread


class Board:

    class Cell:

        def __init__(self,
                     sizex,
                     sizey,
                     x,
                     y,
                     color=(0, 0, 0),
                     border_color=(100, 100, 100),
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
                                 self.w - self.border,
                                 self.h - self.border
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
                                                self.h - self.border * 2 - 4), w)

        def draw_x(self, color, w=2):
            global screen
            pygame.draw.line(screen, color, (self.x + self.border + 2, self.y + self.border + 2),
                             (self.x + self.w - self.border * 2 - 4, self.y + self.h - self.border * 2 - 4), w)
            pygame.draw.line(screen, color, (self.x + self.w - self.border * 2 - 4, self.y + self.border + 2),
                             (self.x + self.border + 2, self.y + self.h - self.border * 2 - 4), w)

        def get_coords(self):
            return self.x, self.y

        def get_indexes(self):
            return self.x // self.w, self.y // self.h

    def __init__(self,
                 cell_count_x,
                 cell_count_y,
                 cell_size_x=50,
                 cell_size_y=None,
                 x=0,
                 y=0,
                 cell_color=(0, 0, 0),
                 border_color=(100, 100, 100),
                 border=2):
        self.toe = False
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y if cell_size_y is not None else cell_size_x
        self.width = cell_count_x * self.cell_size_x
        self.height = self.cell_size_y * cell_count_y
        self.x, self.y = x, y
        self.border_color = border_color
        self.border = border
        self.cell_count_x = cell_count_x
        self.cell_count_y = cell_count_y
        self.cells = [[self.Cell(self.cell_size_x,
                                 self.cell_size_y,
                                 i,
                                 j,
                                 cell_color,
                                 border_color,
                                 border)
                       for i in range(x, self.width + x, self.cell_size_x)]
                      for j in range(y, self.height + y, self.cell_size_y)]
        # self.snake = Snake(5, 5, 'up', 5, cell_count_x, cell_count_y, self)

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

    def set_print(self, col, color):
        col.set_color(color)
        col.paint(screen)
        col.set_color((0, 0, 0))

    def render(self, screen, points: tuple, id):
        for row in self.cells:
            for col in row:
                col.paint(screen)
        for snake in points[0]:
            for x, y in snake:
                self.set_print(self.cells[y][x], (255, 0, 0))
            else:
                self.set_print(self.cells[y][x], (100, 0, 0))
        for x, y in points[1]:
            col = self.cells[y][x]
            col.set_color((0, 255, 0))
            col.paint(screen)
            col.set_color((0, 0, 0))
        for x, y in points[0][id]:
            self.set_print(self.cells[y][x], (0, 0, 150))
        else:
            self.set_print(self.cells[y][x], (0, 0, 255))

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

    def __get_cell(self, mouse_pos):
        for row in self.cells:
            for col in row:
                if col.test_for_click(*mouse_pos):
                    return col
        return None

    def __on_click(self, cell: Cell):
        pass

    def get_click(self, mouse_pos):
        cell = self.__get_cell(mouse_pos)
        if cell:
            self.__on_click(cell)


def receiver(group, port=48666):
    addrinfo = socket.getaddrinfo(group, None)[0]
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(5)
    s.bind(('', port))

    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    if addrinfo[0] == socket.AF_INET: # IPv4
        mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Loop, printing any data we receive
    return s.recvfrom(1500)


con = socket.socket()
connected = False
con.settimeout(5)


pygame.init()
base_color = (0, 0, 0)
frames = 30
# sizex, sizey = 500, 500

clock = pygame.time.Clock()
id = None


def get_update():
    while True:
        try:
            res = con.recv(50000)
            id = int.from_bytes(res[-1:], 'little')
            res = pickle.loads(res)
            screen.fill(base_color)
            board.render(screen, res, id)
            pygame.display.flip()
        except Exception as f:
            print(f)


while 1:
    if id is None:
        s = input('Куда хотите подключиться?(ip:порт)\n'
                  'Если не знаете одну из частей, замените ее на *\n'
                  'Если не знаете, нажмите Enter\n').replace('*', '')
        s = s.split(':') if ':' in s else s.split()
        port = 48666
        try:
            if len(s) > 1:
                ip, port = s
                if port and ip:
                    con.connect((ip, int(port)))
                    cx, cy, s, id = map(int,
                                        con.recv(1024).decode('utf-8').split())
                    board = Board(cx, cy, s, border=1)
                    screen = pygame.display.set_mode((board.width, board.height))
                    pygame.display.flip()
                    Thread(target=get_update).start()
                    continue
            port, sender = receiver('225.0.0.250', port=int(port))
            con.connect((sender[0], int(port.decode('utf-8'))))
            cx, cy, s, id = map(int, con.recv(1024).decode('utf-8').split())
            board = Board(cx, cy, s, border=1)
            screen = pygame.display.set_mode((board.width, board.height))
            pygame.display.flip()
            Thread(target=get_update).start()
            continue
        except Exception as f:
            print(f)
    try:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.dict['key'] == pygame.key.key_code("UP"):  # up
                    con.send('up???'.encode('utf-8'))
                    break
                elif e.dict['key'] == pygame.key.key_code("LEFT"):  # down
                    con.send('left?'.encode('utf-8'))
                    break
                elif e.dict['key'] == pygame.key.key_code("DOWN"): # left
                    con.send('down?'.encode('utf-8'))
                    break
                elif e.dict['key'] == pygame.key.key_code("RIGHT"): # right:
                    con.send('right'.encode('utf-8'))
                    break
                elif e.dict['key'] == pygame.K_RETURN:  # enter
                    con.send('start'.encode('utf-8'))
                    break
        time.sleep(0.1)
    except Exception as f:
        con.close()
        del con
        id = None
        del board
pygame.quit()
