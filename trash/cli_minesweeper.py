import random


class MineSweeper:

    h: int
    w: int
    mines: int
    map: list
    opened: int
    unmines: int
    cmines: int
    game: bool

    def __init__(self, h: int, w: int, mines: int):
        self.h = h - 1
        self.w = w - 1
        self.mines = mines
        self.unmines = mines
        self.cmines = mines
        self.opened = w * h - mines
        self.map = [0] * h
        self.restart()
        self.game = False

    def restart(self):
        for j in range(self.h + 1):
            self.map[j] = list(Cell(j, i) for i in range(self.w + 1))
        self.unmines = self.mines
        self.cmines = self.mines
        self.opened = ((self.w + 1) * (self.h + 1)) - self.mines
        self.close_all()
        self.game = False

    def place_things(self, nx, ny):
        setted_mines = 0
        while setted_mines < self.mines:
            x, y = random.randint(0, self.w), random.randint(0, self.h)
            if self.map[y][x] == 0 and (x != ny or y != nx):
                self.map[y][x] += 9
                setted_mines += 1
        # setting hints
        for x in range(self.w + 1):
            for y in range(self.h + 1):
                if self.map[y][x] == 9:
                    Cell.check_around(self,
                                      y,
                                      x,
                                      lambda x: x < 9, lambda x: x.__iadd__(1))
        self.game = True

    def print_map(self):
        if self.opened == 0:
            self.win()
        print(f'  --height: {self.h + 1} -- width: {self.w + 1} --')
        print(f'--mines:  {self.unmines} -- cells left: {self.opened}--')
        for x in range(self.h + 1):
            print(*([self.h - x, ' ' * (len(str(self.h)) - len(str(self.h - x))) + '|'] + [
                ' ' * (len(str(i))) + str(e) for i, e in enumerate(self.map[x])]))
        print('y ' + ' ' * len(str(self.h)) + '#', *[
            '-' + '-' * len(str(i)) for i in range(self.w + 1)], sep='-')
        print(' ' * len(str(self.h)) + '  x', *range(self.w + 1))
        print(f'введите help для помощи')

    def __str__(self):
        return self.print_map()

    def open_all(self):
        for x in range(self.w + 1):
            for y in range(self.h + 1):
                self.map[y][x].visible = str(self.map[y][x].type)

    def close_all(self):
        for x in range(self.w + 1):
            for y in range(self.h + 1):
                self.map[y][x].visible = '*'
                self.map[y][x].opened = False

    def win(self):
        print('------------------')
        print('-------U WIN------')
        print('------------------')
        input('Press any key to reset\n')
        self.restart()

    def lose(self):
        print('------------------')
        print('------U LOSE------')
        print('------------------')
        self.open_all()
        self.print_map()
        input('Press any key to reset\n')
        self.restart()


class Cell:
    opened: bool = False
    visible: str = '*'
    type: int = 0
    x: int
    y: int

    def __init__(self, x, y, opened=False,
                 type=0,
                 visible='*'):
        self.opened = opened
        self.type = type
        self.visible = visible
        self.x = x
        self.y = y

    def open(self, area):
        if not area.game:
            area.place_things(self.x, self.y)
        if not self.opened and self.visible != '?':
            area.opened -= 1
            self.opened = True
            self.visible = str(self.type)
            if self.type == 0:
                self.check_around(area,
                                  self.x,
                                  self.y,
                                  lambda x: x.type < 9 and not x.opened,
                                  lambda x: x.open(area))
            elif self.type == 9:
                area.opened += 1
                area.lose()
        elif self.opened:
            self.smart_click(area)

    def smart_click(self, area):
        flagged = 0

        def incf(a):
            nonlocal flagged
            if a.visible == 'F':
                flagged += 1
            return False

        def nothing(a):
            pass

        self.check_around(area, self.x, self.y, incf, nothing)
        if flagged == self.type:
            self.check_around(area,
                              self.x,
                              self.y,
                              lambda x: not x.opened and x.visible != 'F',
                              lambda x: x.open(area))

    def flag(self, area):
        if not self.opened:
            if self.visible == '*':
                self.visible = 'F'
                area.unmines -= 1
                if self.type == 9:
                    area.cmines -= 1
            elif self.visible == '?':
                self.visible = '*'
            elif self.visible == 'F':
                self.visible = '?'
                area.unmines += 1
                if self.type == 9:
                    area.cmines += 1
            if area.cmines == 0:
                area.win()

    def __add__(self, other):
        return Cell(self.opened, self.type + other)

    def info(self):
        return f'vis: {self.visible}; type: {self.type}; opened: {self.opened}'

    def __str__(self):
        return f'{self.visible}'

    def __eq__(self, other):
        return self.type == other

    def __iadd__(self, other):
        self.type += other
        return self

    def __lt__(self, other):
        return self.type < other

    def __ge__(self, other):
        return self.type > other

    @staticmethod
    def check_around(area, x, y, cell_condition=lambda x: True, action=lambda x: x):
        if y > 0:
            if cell_condition(area.map[x][y - 1]):
                action(area.map[x][y - 1])
            if x > 0 and cell_condition(area.map[x - 1][y - 1]):
                action(area.map[x - 1][y - 1])
            if x < area.h and cell_condition(area.map[x + 1][y - 1]):
                action(area.map[x + 1][y - 1])
        if y < area.w:
            if cell_condition(area.map[x][y + 1]):
                action(area.map[x][y + 1])
            if x > 0 and cell_condition(area.map[x - 1][y + 1]):
                action(area.map[x - 1][y + 1])
            if x < area.h and cell_condition(area.map[x + 1][y + 1]):
                action(area.map[x + 1][y + 1])
        if x > 0 and cell_condition(area.map[x - 1][y]):
            action(area.map[x - 1][y])
        if x < area.h and cell_condition(area.map[x + 1][y]):
            action(area.map[x + 1][y])


a = MineSweeper(10, 10, 25)
a.restart()
a.print_map()
while True:
    try:
        command = input()
        if command == 'help':
            print('''>resize {height > 0} {width > 0} {mines < height * width}-
- изменение размеров поля
>reset - пересоздание поля
>l {x} {y} - открыть клетку(так же работает "умный клик", т.е если поп-
робовать открыть открытую клетку и ее число совпадает с количеством фла-
гов вокруг нее, то остальные клетки откроются(как нажатие двумя клавиш-
ами мыши одновременно в оригинале)
>r {x} {y} - поставить F/?(знаки сменяются при повторном действии)''')
        else:
            if command == 'reset':
                a.restart()
            else:
                command, params = (lambda x: (x[0], list(map(int, x[1::]))))(command.split())
                if command == 'resize':
                    if params[2] < params[0] * params[1] and sum(params[1:]) > 1 and all(params):
                        a = MineSweeper(*params)
                    else:
                        print('error')
                elif command == 'l':
                    a.map[a.h - params[1]][params[0]].open(a)
                elif command == 'r':
                    a.map[a.h - params[1]][params[0]].flag(a)
            a.print_map()
    except Exception:
        print('Error')
