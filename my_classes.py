import socket
import pickle


# create player(only for client, server need to know only few parameters)
class Player:
    def __init__(self, start_x, start_y, size, color, my_id):
        self.x = int(start_x)
        self.y = int(start_y)
        self.color = color
        self.vel = 7
        self.size = size
        self.id = my_id
        self.score = 0

    # info for server
    def get_info(self):
        return self.x, self.y, self.score

    # check for collisions with circle objects
    def collision_with_circle(self, target, radius):
        x1 = self.x
        x2 = self.x + self.size
        y1 = self.y
        y2 = self.y + self.size
        a1 = target[0] - radius
        a2 = target[0] + radius
        b1 = target[1] - radius
        b2 = target[1] + radius

        if y1 < b1 < y2 or y1 < b2 < y2:
            if x1 < a1 < x2 or x1 < a2 < x2:
                return True

        return False


# talkin with server
class Network:
    # creat socket for client
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = ('127.0.0.1', 60065)

    # try connect to server, send urs info, and wait for info about other players(and bullets)
    def hello(self, my_color, start_pos):
        # players, myID
        self.client_socket.connect(self.address)
        data = pickle.dumps(['hello', my_color, start_pos])
        self.client_socket.send(data)
        data = pickle.loads(self.client_socket.recv(1024 * 8))
        return data[0], data[1]

    # send to server urs and yours bullet position, wait info about others
    def refresh(self, data):
        # players
        data = pickle.dumps(data)
        self.client_socket.send(data)
        return pickle.loads(self.client_socket.recv(1024 * 8))

    # close connection with server
    def bye_bye(self):
        self.client_socket.close()


# info about cannon and her bullet
class Cannon:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.radius = 20
        self.color = (90, 90, 90)
        self.bull_x = self.x
        self.bull_y = self.y
        self.bull_r = 10
        self.bull_c = (0, 0, 0)
        self.bull_vel = 5

    # try to catch player
    def chase_target(self, player):
        if player.x + player.size / 2 < self.bull_x:
            self.bull_x -= self.bull_vel
        else:
            self.bull_x += self.bull_vel
        if player.y + player.size / 2 < self.bull_y:
            self.bull_y -= self.bull_vel
        else:
            self.bull_y += self.bull_vel

    # info for server(all object is stupid, but its work with pickles, cool!)
    def get_cannon(self):
        return self
