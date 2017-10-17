import pygame
import _thread
import sys
import time
from Player import Player
from Board import Board
from constants import *
from pygame.locals import *
from Renderer import Renderer
from Managers import LetterManager


class Main:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Scrabble")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = pygame.image.load(BACKGROUND_IMAGE).convert_alpha()
        self.letter_generator = LetterManager()
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.player.tiles = self.letter_generator.create_player_tiles(STARTING_RANDOMS)
        self.board = Board(self.player)
        self.render_engine = Renderer(self.board, self.screen)
        self.running = True
        self.turn = 1
        _thread.start_new_thread(self.start(), ())

    def start(self):
        player_dragging_tile = False
        tile_being_dragged = None
        changed_tiles = list()
        next_arrow_click, revert_arrow_click = False, False
        while self.running:
            for event in pygame.event.get():

                if event.type == QUIT:
                    self.end_process()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.check_turn(changed_tiles)
                    changed_tiles = list()
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
                        tile_being_dragged.reset()
                        tile_being_dragged = None
                        player_dragging_tile = False
                    else:
                        for random_tile in self.player.tiles:
                            if random_tile.rect.collidepoint(x, y) and random_tile.visible:
                                        player_dragging_tile = True
                                        random_tile.being_dragged = True
                                        tile_being_dragged = random_tile
                                        time.sleep(0.5)
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
                        changed_tiles = list()
                    elif revert_arrow_click and self.render_engine.back_arrow.rect.collidepoint(x, y):
                        self.board.revert(changed_tiles)
                        changed_tiles = list()
                        self.render_engine.back_arrow_click = False
            self.run()

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
        self.check_turn(changed_tiles)
        print(self.board.word_manager.find_applicable_words(self.letter_generator.tiles_to_string(self.player.tiles)))
        self.turn += 1
        self.render_engine.arrow_click = False

    def check_turn(self, changed_tiles):
        if self.board.check_if_good_move(changed_tiles, self.turn):
            self.player.points += self.board.word_manager.calculate_points(self.board.words_list)
            self.board.regenerate_randoms()
        else:
            self.board.revert(changed_tiles)


Main()
