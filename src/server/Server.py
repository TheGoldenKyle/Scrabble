import socket
import time

class Server:
    host = '127.0.0.1'
    port = 5005
    running = True

    clients = []
    board = []

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        self.board = self.buildBoard()
        self.run()

    def run(self):
        print("Server Started")
        player = 0
        while self.running:
            data, ip = self.socket.recvfrom(1024)
            if ip in self.clients:
                message = data.decode()
                if self.clients[player] == ip:
                    if message is not "":
                        print("Player: " + str(player) + " | BOARD: " + message)
                        self.unpackString(message)
                    player = (player + 1) % 2
                    self.socket.sendto(data, (self.host, self.clients[player][1]))
            elif len(self.clients) < 2:
                self.clients.append(ip)
                print("Connection established with " + str(ip) + " PLAYER: " + str(len(self.clients)))
            time.sleep(0.1)
        self.socket.close()

    def buildBoard(self):
        tiles = []
        for row in range(11):
            row_tiles = list()
            for col in range(11):
                row_tiles.append(' ')
            tiles.append(row_tiles)
        return tiles

    def unpackString(self, string):
        assert len(string) == 121
        for i in range(11):
            for k in range(11):
                self.board[i][k] = string[i * 11:k]



s = Server()