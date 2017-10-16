from Entities import Tile
import pygame
import time
from constants import *
import random


class WordManager:

    def __init__(self):
        file = open('resources/dictionary.txt', 'r')
        self.words = list(file.read().split())

    def check_word(self, string):
        return string in self.words

    def find_applicable_words(self, letters):  # Find all words that can be made using a set of letters
        letters = list(letters)
        applicable_words = set()
        for word in self.words:
            has_extras = False
            word_list = list(word)
            letters_temp = letters[:]
            for letter in word_list:
                if letter not in letters_temp:
                    has_extras = True
                else:
                    letters_temp.remove(letter)
            if not has_extras:
                applicable_words.add(word)
        return applicable_words

    def find_best_word(self, words):
        max_points = 0
        best_word = ""

        for word in words:
            points = 0
            for letter in word:
                value = LETTER_VALUES[letter.upper()]
                points += int(value)
            if points > max_points:
                max_points = points
                best_word = word
        return best_word

    def calculate_points(self, words_list):
        points = 0
        for word in words_list:
            for x in range(0, len(word)):
                points += LETTER_VALUES[word[x]]
        return points


class TextureManager:

    def __init__(self):
        self.full_texture = pygame.image.load(TILE_TEXTURE)
        self.texture_cache = dict()  # Cache for loaded textures
        time.sleep(2)

    def get_tile_texture(self, tile, size=79):
        letter = tile.letter
        if (letter, size) not in self.texture_cache.keys():
            a, b = self.get_coordinates(letter)
            print("Added letter ({0}, {1}) to cache!".format(letter, size))
            self.texture_cache[(letter, size)] = self.full_texture.subsurface((a, b, 79, 79))
            if size != 79:
                self.texture_cache[(letter, size)] = pygame.transform.scale(self.texture_cache[(letter, size)], (size, size))
        return self.texture_cache[(letter, size)]

    def get_arrow_texture(self, size=79):
        if ('arrow', size) not in self.texture_cache.keys():
            self.texture_cache[('arrow', size)] = pygame.image.load(ARROW_IMAGE).convert_alpha()
            if size != ARROW_SIZE:
                self.texture_cache[('arrow', size)] = pygame.transform.scale(self.texture_cache[('arrow', size)], (size, size))
        return self.texture_cache[('arrow', size)]

    def get_back_arrow_texture(self, size=55):
        if ('back_arrow', size) not in self.texture_cache.keys():
            self.texture_cache[('back_arrow', size)] = pygame.image.load(BACK_ARROW_IMAGE).convert_alpha()
            if size != BACK_ARROW_SIZE:
                self.texture_cache[('back_arrow', size)] = pygame.transform.scale(self.texture_cache[('back_arrow', size)], (size, size))
        return self.texture_cache[('back_arrow', size)]

    def get_coordinates(self, letter):
        letter_coordinates = LETTER_LOCATIONS[letter]
        comma = letter_coordinates.index(',')
        x, y = letter_coordinates[0:comma], letter_coordinates[comma + 1:]
        return int(x), int(y)


class LetterManager:

    alphabet = list(LETTERS)

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

