import socket
from _thread import start_new_thread
import pickle

# wake up server
HOST = '94.73.237.132'
PORT = 5555
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()
print('listen')
# dicts of players and bullets
players = {}
cannons = {}
ID = 0


# talk with many clients
def threaded_clients(conn, id):
    # global caus i need change it # too lazy for one more parameter learning
    global players
    try:
        # loop for talking with client
        while True:
            # try get data(list waiting)
            data = pickle.loads(conn.recv(1024*8))
            if not data:
                break

            # client can send 'hello', but updating info more often
            # 'hello' give server client's color and position and waiting his ID
            if data[0] != 'hello':
                players[id]['x'], players[id]['y'], players[id]['score'] = data[0]
                cannons[id] = data[1]
                data = [players, cannons]
            else:
                players[id]['color'] = data[1]
                players[id]['x'], players[id]['y'] = data[2]
                data = [players, id]

            # sendin info back
            conn.send(pickle.dumps(data))

    # if client close connection delete his and his bullet info
    except Exception as e:
        print(e)
        del players[id]
        del cannons[id]
        conn.close()


# waiting for connections and register them
while True:
    host, addr = server_socket.accept()
    players[ID] = {'x': 0, 'y': 0, 'color': 0, 'id': ID, 'score': 0}
    start_new_thread(threaded_clients, (host, ID))

    ID += 1
