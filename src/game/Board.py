import pygame

from src.entities.Entities import Tile, Arrow, BackArrow
from src.game.constants import *
from src.helpers.Managers import WordManager, LetterManager


class Board:

    def __init__(self, player):
        self.player = player
        self.letter_generator = LetterManager()
        self.word_manager = WordManager()
        self.arrow, self.back_arrow = Arrow(), BackArrow()
        self.tiles = self.create_tiles()
        self.frame_count = 0
        self.word_list = set()

    def create_tiles(self):
        """
        Creates all tile objects for the game-board, minus the players tiles.
        Sets all tiles to blank by default

        :return: Returns a square, 2D list of each Tile object in their respective
                 spot on the board.
        """
        tiles = []
        for row in range(BOARD_SIZE):
            row_tiles = list()
            for col in range(BOARD_SIZE):
                x, y = col * TILE_SIZE + (col + 1) + 5, row * TILE_SIZE + (row + 1) + 60
                tile = Tile(' ', row, col)
                tile.x, tile.y = x, y
                tile.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                row_tiles.append(tile)
            tiles.append(row_tiles)
        return tiles

    def check_if_good_move(self, changed_tiles, turn):
        """
        Checks if the game-board, when the next-turn arrow is pressed, is a valid game-board.

        :param changed_tiles: List of Tuples of (row, col) of each tile that has been changed
                              since the last turn
        :param turn: Turn number of game
        :return: Returns True iff the game-board is a valid board, else returns False.
        """
        if len(changed_tiles) < MIN_WORD_SIZE:
            return False
        if turn != 1 and not self.touching_other_letters(changed_tiles):
            return False
        self.word_list = self.get_words(changed_tiles)
        if len(self.word_list) == 0:
            return False
        for word in self.word_list:
            if not self.word_manager.check_word(word.lower()):
                return False
        return True

    def get_words(self, changed_tiles):
        words = set()
        words |= self.check_horizontal_words(changed_tiles)
        words |= self.check_vertical_words(changed_tiles)
        return words

    def touching_other_letters(self, changed_tiles):
        """
        Given a coordinate of a changed tile, determines whether that tile is touching previously
        placed letters. (All words in Scrabble must be an extension of a previous word on
        every turn except the first)

        :param changed_tiles: List of Tuples of (row, col) of each tile that has been changed
                              since the last turn
        :return: Returns whether Tile at (row, col) is touching a previously placed tile.
        """
        for row, col in changed_tiles:
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if (i, j) not in changed_tiles and self.tile_exists_at(i, j) \
                     and self.tiles[i][j].letter != ' ':
                        return True
        return False

    def check_horizontal_words(self, changed_tiles):
        """
        Determines whether each newly placed tile is part of a word horizontally, from
        left to right.

        :param changed_tiles: List of Tuples of (row, col) of each tile that has been changed
                              since the last turn
        :return: Returns whether each tile creates a valid word, horizontally.
        """
        words = set()
        for row, col in changed_tiles:
            potential_word = ""
            last_letter, next_letter = None, None
            while last_letter != ' ':
                last_letter = self.letter_at(row, col - 1)
                col -= 1
            col += 1
            while next_letter != ' ':
                potential_word += self.tiles[row][col].letter
                next_letter = self.letter_at(row, col + 1)
                col += 1
            if len(potential_word) >= MIN_WORD_SIZE:
                words.add(potential_word)
        return words

    def check_vertical_words(self, changed_tiles):
        """
        Determines whether each newly placed tile is part of a word vertically,
        from top to bottom.

        :param changed_tiles: List of Tuples of (row, col) of each tile that has been changed
                              since the last turn
        :return: Returns whether each tile creates a valid word, vertically.
        """
        words = set()
        for row, col in changed_tiles:
            potential_word = ""
            last_letter, next_letter = None, None
            while last_letter != ' ':
                last_letter = self.letter_at(row - 1, col)
                row -= 1
            row += 1
            while next_letter != ' ':
                potential_word += self.tiles[row][col].letter
                next_letter = self.letter_at(row + 1, col)
                row += 1
            if len(potential_word) >= MIN_WORD_SIZE:
                words.add(potential_word)
        return words

    def letter_at(self, row, col):
        """
        Returns the letter at position (row, col), or returns a blank string.

        :param row: Row of tile to find the letter of. BOARD_SIZE > row >= 0
        :param col: Column of tile to find the letter of. BOARD_SIZE > col >= 0

        :return: Returns the letter at the specified position. If there is no
                 letter, or a tile does not exist at the specified location,
                 return an empty string of length 1.
        """
        if self.tile_exists_at(row, col):
            return self.tiles[row][col].letter
        else:
            return ' '

    def regenerate_randoms(self):
        """
        Randomly generates a new letter from the list of available letters,
        list(LETTERS), and applies it to all player tiles that were used in the
        previous turn, and sets them to visible.

        :return: None
        """
        for tile in self.player.tiles:
            if not tile.visible:
                tile.change_to(self.letter_generator.generate(1)[0].letter)
                tile.visible = True

    def revert(self, changed_tiles):
        """
        Reverts the board to the state it was at the beginning of the turn.

        :param changed_tiles: List of Tuples of (row, col) of each tile that has been changed
                              since the last turn
        :return: None
        """
        for row, col in changed_tiles:
            self.tiles[row][col].change_to(' ')
        for tile in self.player.tiles:
            if not tile.visible:
                tile.visible = True

    def tile_exists_at(self, row, col):
        """
        Determines whether a tile exists at (row, col)

        :param row: Row to check. BOARD_SIZE > row >= 0
        :param col: Column to check. BOARD_SIZE > col >= 0

        :return: Returns True iff a tile exists at (row, col). False otherwise.
        """
        return BOARD_SIZE > row >= 0 and BOARD_SIZE > col >= 0
