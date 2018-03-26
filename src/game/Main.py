import _thread
import sys
import threading
import socket
import time

import pygame
from pygame.locals import *
from logging import Logger

from src.entities.Player import Player
from src.game.Board import Board
from src.game.Renderer import Renderer
from src.game.constants import *
from src.helpers.Managers import LetterManager


class Main:

    host = '127.0.0.1'
    port = 0
    server = ('127.0.0.1', 5005)

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Scrabble")
        self.logger = Logger("GAME")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = self.load_background()
        self.letter_generator = LetterManager()
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.player.tiles = self.letter_generator.create_player_tiles(STARTING_RANDOMS)
        self.board = Board(self.player, self.logger)
        self.render_engine = Renderer(self.board, self.screen)
        self.running = True
        self.turn = 1
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        self.socket.setblocking(0)
        self.port = self.socket.getsockname()[1]
        #self.rT = threading.Thread(target=self.receive)
        #self.rT.start()
        _thread.start_new_thread(self.start(), ())

    def start(self):
        player_dragging_tile = False
        tile_being_dragged = None
        changed_tiles = []
        next_arrow_click, revert_arrow_click = False, False
        self.socket.sendto("".encode(), self.server)
        while self.running:
            try:
                data, ip = self.socket.recvfrom(1024)
                message = data.decode()
                print("hello")
                if len(message) == BOARD_SIZE * BOARD_SIZE:
                    print("hi")
                    self.unpackString(message)
            except:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.end_process()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.check_turn(changed_tiles)
                        changed_tiles = []
                    if event.type == MOUSEBUTTONDOWN:
                        x, y = event.pos
                        if player_dragging_tile:
                            for row in self.board.tiles:
                                for tile in row:
                                    if tile.rect.colliderect(pygame.Rect(x, y, 1, 1)):
                                        changed_tiles.append((tile.row, tile.col))
                                        tile.change_to(tile_being_dragged.letter)
                                        tile.occupied = True
                                        tile_being_dragged.visible = False
                                        self.logger.critical("'{0}' dropped at location: ({1}, {2})".format(
                                                                                             tile_being_dragged.letter,
                                                                                             tile.row, tile.col))
                            tile_being_dragged.reset()
                            tile_being_dragged = None
                            player_dragging_tile = False
                        else:
                            for random_tile in self.player.tiles:
                                if random_tile.rect.collidepoint(x, y) and random_tile.visible:
                                            player_dragging_tile = True
                                            random_tile.being_dragged = True
                                            tile_being_dragged = random_tile
                            if self.render_engine.arrow.rect.collidepoint(x, y):
                                next_arrow_click = True
                                self.render_engine.arrow_click = True
                            elif self.render_engine.back_arrow.rect.collidepoint(x, y):
                                revert_arrow_click = True
                                self.render_engine.back_arrow_click = True
                    if event.type == MOUSEBUTTONUP:
                        x, y = event.pos
                        if next_arrow_click and self.render_engine.arrow.rect.collidepoint(x, y):
                            self.next_turn(changed_tiles)
                            changed_tiles = []
                        elif revert_arrow_click and self.render_engine.back_arrow.rect.collidepoint(x, y):
                            self.board.revert(changed_tiles)
                            changed_tiles = []
                            self.render_engine.back_arrow_click = False
            self.run()

    def receive(self):
        while self.running:
            try:
                while True:
                    print("hello")
                    data, ip = self.socket.recvfrom(1024)
                    message = data.decode()
                    if len(message) == BOARD_SIZE * BOARD_SIZE:
                        self.unpackString(message)
                    time.sleep(0.1)
            except:
                time.sleep(0.05)

    def run(self):
        """
        Calls the render_engine to render the next frame and then updates the display.
        :return: None
        """
        self.clock.tick(60)
        self.screen.blit(self.background, (0, 0))
        self.render_engine.render()
        pygame.display.update()

    def end_process(self):
        """
        Exits game window and ends game process.
        :return: None
        """
        self.running = False
        pygame.quit()
        sys.exit()

    def next_turn(self, changed_tiles):
        """
        Moves the game to the next turn, if the previous turn was valid.

        :param changed_tiles: List of Tuples of (row, col) of each tile that has been changed
                              since the last turn
        :return: None
        """
        if self.check_turn(changed_tiles):
            self.turn += 1
            self.sendBoard()
        self.render_engine.arrow_click = False

    def check_turn(self, changed_tiles):
        """
        Checks if the current turn is a valid turn.

        :param changed_tiles: List of Tuples of (row, col) of each tile that has been changed
                              since the last turn
        :return: True iff the current turn is a valid turn. Else return False.
        """
        good_move = False
        if self.board.check_if_good_move(changed_tiles, self.turn):
            self.player.points += self.board.word_manager.calculate_points(self.board.word_list)
            self.board.regenerate_randoms()
            good_move = True
        else:
            self.board.revert(changed_tiles)
        return good_move

    def load_background(self):
        """
        Loads the background image and resizes it to match the dimensions of the window

        :return: Returns the resized background image texture
        """
        background = pygame.image.load(BACKGROUND_IMAGE).convert_alpha()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        return background

    def unpackString(self, string):
        for row in range(11):
            for col in range(11):
                self.board.tiles[row][col].change_to(string[row*11 + col])

    def packString(self):
        message = ""
        for row in range(11):
            for col in range(11):
                message += self.board.tiles[row][col].letter
        return message

    def sendBoard(self):
        self.socket.sendto(self.packString().encode(), self.server)

Main()
