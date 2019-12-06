import time
from threading import Thread
import random
import socket
from threading import Thread
import struct
import pickle


class Snake(Thread):
    dirrections = {
        'up???': (0, -1),
        'down?': (0, 1),
        'left?': (-1, 0),
        'right': (1, 0),
        'none': (0, 0)
    }

    def __init__(self, dirrection, length, maxx, maxy):
        super().__init__()
        ix, iy = get_random_pos()
        self.mx, self.my = maxx - 1, maxy - 1
        self.coords = [(ix, iy)] * length
        self.alive = False
        self.dirrection = dirrection

    def move(self):
        global set_snakes
        if self.alive and self.dirrection != 'none':
            cx, cy = self.coords[-1]
            dx, dy = self.dirrections[self.dirrection]
            new_cords = self.move_f(cx + dx, cy + dy)
            if new_cords in set_snakes:
                self.destroy()
                return
            elif new_cords in fruits:
                set_fruit(new_cords)
            else:
                self.coords.pop(0)
            self.coords.append(new_cords)
    
    def move_f(self, x, y):
        new_ix, new_iy = x, y
        if new_ix < 0:
            new_ix = self.mx
        elif new_ix > self.mx:
            new_ix = 0
        if new_iy < 0:
            new_iy = self.my
        elif new_iy > self.my:
            new_iy = 0
        return new_ix, new_iy
    
    def destroy(self):
        for pos in self.coords:
            fruits.add(pos)
        self.coords = [get_random_pos()]
        self.dirrection = 'none'
        self.alive = False

    def change_dirrection(self, dir):
        if dir == 'start' and not self.alive:
            self.alive = True
            self.dirrection = 'none'
        elif dir != 'start' and\
                (self.dirrection == 'left?' and dir != 'right' or
                 self.dirrection == 'right' and dir != 'left?' or
                 self.dirrection == 'up???' and dir != 'down?' or
                 self.dirrection == 'down?' and dir != 'up???' or
                 self.dirrection == 'none'):
            self.dirrection = dir

    def __str__(self):
        return str(self.coords)


def set_fruit(item):
    global set_snakes
    if fruits and item is not None:
        fruits.remove(item)
    if len(fruits) < fruit_count:
        fruits.add(get_random_pos())


def get_random_pos():
    cd = (random.randint(0, cell_count_x - 1), random.randint(0, cell_count_y - 1))
    while cd in fruits or cd in set_snakes:
        cd = (random.randint(0, cell_count_x - 1), random.randint(0, cell_count_y - 1))
    return cd


def get_set_snakes():
    asd = []
    for snake in snakes:
        if snake.alive:
            asd.extend(snake.coords)
    return set(asd)


class Connection(Thread):

    def __init__(self, conn, adr, cls):
        self.cls = cls
        self.conn, self.adr = conn, adr
        snakes.append(Snake('none', 1, cell_count_x, cell_count_y))
        self.snake = len(snakes) - 1
        self.send(f'{cell_count_x}\t{cell_count_y}\t{cell_size}\t{self.snake}'.encode('utf-8'))
        super().__init__()

    def run(self):
        while True:
            try:
                data = self.conn.recv(5).decode('utf-8')
                snakes[self.snake].change_dirrection(data)
            except Exception as f:
                snakes.pop(self.snake)
                for connection in self.cls.connections[self.snake:]:
                    connection.snake -= 1
                self.conn.close()
                self.cls.connections.remove(self)
                del self
                print('run', f)
                break

    def send(self, s):
        try:
            self.conn.send(s)
        except Exception as f:
            print('send', f)

    def sendall(self, *args):
        try:
            self.conn.sendall(b'\t'.join(args))
        except Exception as f:
            print('sendall', f)


def snakes_send():
    asd = []
    for snake in snakes:
        asd.append(snake.coords)
    return pickle.dumps((asd, fruits))


class Program:

    def __init__(self, port):
        self.socket = socket.socket()
        if not port:
            port = '48666'
        self.socket.bind(("", int(port)))
        self.socket.listen(10)
        self.connections = []
        self.port = port
        Thread(target=self.sender, args=['225.0.0.250']).start()
        print('Система запущена успешно и готова принимать подключения')

    def sender(self, group):
        data = self.port.encode('utf-8')
        MYTTL = 1
        addrinfo = socket.getaddrinfo(group, None)[0]
        s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
        ttl_bin = struct.pack('@i', MYTTL)
        if addrinfo[0] == socket.AF_INET:  # IPv4
            s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)
        while True:
            s.sendto(data, (addrinfo[4][0], int(self.port)))
            time.sleep(2)

    def receive_connections(self):
        while 1:
            conn, adr = self.socket.accept()
            try:
                conn.settimeout(10000)
                self.connections.append(Connection(conn, adr, self))
                self.connections[-1].start()
                print(f'Новое соединение: {adr[0]}:{adr[1]} - {time.strftime("%d.%m.%Y %H:%M:%S")}')
                print('Текущие пользователи:', *self.connections)
            except Exception as f:
                print('receive_conns', f)
            time.sleep(0.05)

    def run(self):
        global set_snakes
        Thread(target=self.receive_connections).start()
        while 1:
            for snake in snakes:
                snake.move()
            set_snakes = get_set_snakes()
            ss = snakes_send()
            for con in self.connections:
                con.sendall(ss, bytes([con.snake]))
            time.sleep(0.1)


set_snakes = []
snakes = []
fruits = set()
cell_count_x = 150
cell_count_y = 70
fruit_count = cell_count_x * cell_count_y // 100
for i in range(fruit_count): set_fruit(None)
set_fruit(None)
cell_size = 10
port = input('Введите порт, если не знаете, нажмите Enter\n')
a = Program(port)
a.run()
