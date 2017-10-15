from Entities import *
from Managers import *
from LetterGenerator import *


class Board:

    def __init__(self, player):
        self.player = player
        self.letter_generator = LetterGenerator()
        self.checker = WordManager()
        self.tiles = self.create_tiles()
        self.frame_count = 0
        self.words_list = set()

    def create_tiles(self):
        tiles = list()
        for row in range(BOARD_SIZE):
            row_tiles = list()
            for col in range(BOARD_SIZE):
                x, y = row * TILE_SIZE + (row + 1) + 5, col * TILE_SIZE + (col + 1) + 60
                tile = Tile(' ', row, col)
                tile.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                row_tiles.append(tile)
            tiles.append(row_tiles)
        return tiles

    def check_if_good_move(self, changed_tiles):
        if len(changed_tiles) < MIN_WORD_SIZE:
            return False
        self.words_list = set()
        self.check_horizontal_words(changed_tiles)
        self.check_vertical_words(changed_tiles)
        for word in self.words_list:
            if len(self.words_list) == 0 or not self.checker.check_word(word.lower()):
                return False
        return True

    def check_horizontal_words(self, changed_tiles):
        for loc in changed_tiles:
            row, col = loc[0], loc[1]
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
                self.words_list.add(potential_word)

    def check_vertical_words(self, changed_tiles):
        for loc in changed_tiles:
            row, col = loc[0], loc[1]
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
                self.words_list.add(potential_word)

    def letter_at(self, row, col):
        if self.tile_exists_at(row, col):
            return self.tiles[row][col].letter
        else:
            return ' '

    def regenerate_randoms(self):
        for tile in self.player.tiles:
            if not tile.visible:
                tile.change_to(self.letter_generator.generate(1)[0].letter)
                tile.visible = True

    def revert(self, changed_tiles):
        for changed_tile_row, changed_tile_col in changed_tiles:
            for row in self.tiles:
                for tile in row:
                    if tile.row == changed_tile_row and tile.col == changed_tile_col:
                        tile.change_to(' ')
        for tile in self.player.tiles:
            if not tile.visible:
                tile.visible = True

    def tile_exists_at(self, row, col):
        return BOARD_SIZE > row >= 0 and BOARD_SIZE > col >= 0
