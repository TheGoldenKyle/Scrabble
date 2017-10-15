import random
from Managers import WordManager
from Entities import Tile
from constants import *


class LetterGenerator:

    alphabet = list("AAAAAAAAABBCCDDDDEEEEEEEEEEEEFFGGGHHIIIIIIIIIJKLLLLMMNNNNNNOOOOOOOOPPQRRRRRRSSSSTTTTTTUUUUVVWWXUUZ")

    def __init__(self):
        self.word_manager = WordManager()

    def generate(self, num_letters):
        if len(self.alphabet) > 0:
            tiles = list()
            for _ in range(0, num_letters):
                letter = random.choice(self.alphabet)
                tiles.append(Tile(letter))
                self.alphabet.remove(letter)
            print(self.word_manager.find_applicable_words(self.tiles_to_string(tiles).lower()))
            return tiles

    def generate_starting(self, num_letters):
        tiles = self.generate(num_letters)
        while len(self.word_manager.find_applicable_words(self.tiles_to_string(tiles).lower())) < MIN_STARTING_WORDS:
            tiles = self.generate(num_letters)
        return tiles

    def tiles_to_string(self, tiles):
        string = ""
        for tile in tiles:
            string += str(tile.letter)
        return string

    def create_player_tiles(self, num_randoms):
        randoms = self.generate_starting(num_randoms)
        for i in range(num_randoms):
            x, y = i * 81 + 6, 9 * 83 + 65
            randoms[i].x, randoms[i].y = x, y
            randoms[i].starting_x, randoms[i].starting_y = x, y
        return randoms


