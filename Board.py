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
            print("False")
            return False
        self.words_list = set()
        self.check_horizontal_words(changed_tiles)
        self.check_vertical_words(changed_tiles)
        for word in self.words_list:
            if len(self.words_list) == 0 or not self.checker.check_word(word.lower()):
                print("False")
                return False
        print(self.words_list)
        print("True")
        return True

    def check_horizontal_words(self, changed_tiles):
        for loc in changed_tiles:
            potential_word = ""
            row = int(loc[0:loc.index(",")])
            col = int(loc[loc.index(",") + 1:])
            last_letter = None
            next_letter = None
            while last_letter != ' ' and self.tile_exists_at(row, col - 1):
                last_letter = self.tiles[row][col - 1].letter
                col -= 1
            col += 1
            while next_letter != ' ':
                potential_word += self.tiles[row][col].letter
                next_letter = self.tiles[row][col + 1].letter
                col += 1
            if len(potential_word) > MIN_WORD_SIZE:
                self.words_list.add(potential_word)

    def check_vertical_words(self, changed_tiles):
        for loc in changed_tiles:
            potential_word = ""
            row = int(loc[0:loc.index(",")])
            col = int(loc[loc.index(",") + 1:])
            last_letter = None
            next_letter = None
            while last_letter != ' ' and self.tile_exists_at(row, col):
                last_letter = self.tiles[row - 1][col].letter
                row -= 1
            row += 1
            while next_letter != ' ' and self.tile_exists_at(row, col):
                potential_word += self.tiles[row][col].letter
                next_letter = self.tiles[row + 1][col].letter
                row += 1
            if len(potential_word) > MIN_WORD_SIZE:
                self.words_list.add(potential_word)

    def regenerate_randoms(self):
        for tile in self.player.tiles:
            if not tile.visible:
                tile.change_to(self.letter_generator.generate(1)[0].letter)
                tile.visible = True

    def revert(self, changed_tiles):
        for loc in changed_tiles:
            changed_tile_row = int(loc[0:loc.index(",")])
            changed_tile_col = int(loc[loc.index(",") + 1:])
            for row in self.tiles:
                for tile in row:
                    if tile.row == changed_tile_row and tile.col == changed_tile_col:
                        tile.change_to(' ')
        for tile in self.player.tiles:
            if not tile.visible:
                tile.visible = True

    def tile_exists_at(self, row, col):
        return BOARD_SIZE - 1 > row >= 0 and BOARD_SIZE - 1 > col >= 0
