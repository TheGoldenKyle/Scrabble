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
        self.turns = 0
        self.run()

    def run(self):
        print("Server Started")
        player = 0
        while self.running:
            data, ip = self.socket.recvfrom(1024)
            num_players = len(self.clients)
            if ip in self.clients:
                message = data.decode()
                if message is not "":
                    if message == "QUIT":
                        self.clients.remove(ip)
                        print("Player: " + str(player) + " left the game!")
                    elif self.clients[player] == ip:
                            print("Player: " + str(player) + " | BOARD: " + message)
                            player = (player + 1) % 2
                            self.unpackString(message)
                            self.relayTurn(message, player)
                            self.turns += 1
            elif num_players < 2:
                self.addPlayer(ip, num_players + 1)
            time.sleep(0.1)
        self.socket.close()

    def relayTurn(self, message, other_player):
        self.unpackString(message)
        data = ('-' + message).encode()
        self.socket.sendto(data, self.clients[other_player])

    def addPlayer(self, ip, num_players):
        self.clients.append(ip)
        print("Connection established with " + str(ip) + " PLAYER: " + str(len(self.clients)))
        if num_players == 1:
            self.socket.sendto('-'.encode(), ip)
        elif num_players == 2:
            board_data = self.packString()
            print("Sent gameboard to: " + str(ip))
            print(board_data.decode())
            self.socket.sendto(board_data, ip)

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
                self.board[i][k] = string[i * 11 + k]

    def packString(self):
        message = ""
        for row in range(11):
            for col in range(11):
                message += self.board[row][col]
        return message.encode()


s = Server()