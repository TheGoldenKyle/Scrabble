import pygame
import time
import random
from constants import *
from Entities import Tile


class WordManager:

    def __init__(self):
        file = open('resources/dictionary.txt', 'r')
        self.words = list(file.read().split())

    def check_word(self, word):
        """
        Checks if string is a word in the loaded dictionary.

        :param word: String to check if in dictionary
        :return: Boolean if word is in dictionary
        """
        return word in self.words

    def find_applicable_words(self, letters):
        """
        Returns a list of all words from the loaded dictionary
        that can be made using a string of letters.

        :param letters: String of letters to use
        :return: Returns a list of words that can be created with given letters
        """
        letters = list(letters.lower())
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
        """
        Find the word in words that has the maximum point value according to
        point values in dict{LETTER_VALUES}

        :param words: List of words to compare
        :return: Returns the best word and its respective points
        """
        max_points = 0
        best_word = ""

        for word in words:
            points = self.calc_points_of_word(word)
            if points > max_points:
                max_points, best_word = points, word
        return best_word, max_points

    def calculate_points(self, words_list):
        """
        Given a list of words, this method will calculate the total points of all the words.

        :param words_list: A list containing words
        :return: Returns the total points of all words in words_list
        """
        points = 0
        for word in words_list:
            points += self.calc_points_of_word(word)
        return points

    def calc_points_of_word(self, word):
        """
        Calculates the points of a given word based on LETTER_VALUES in constants.py
        :param word: String to calculate points of
        :return: Number of points for word
        """
        points = 0
        for letter in word:
            points += LETTER_VALUES[letter]
        return points


class TextureManager:

    def __init__(self):
        self.full_texture = pygame.image.load(TILE_TEXTURE)
        self.texture_cache = {}
        time.sleep(2)

    def get_tile_texture(self, tile, size=79):
        """
        Will retrieve and add to cache or fetch from cache the texture associated with
        the tile's letter. Will resize the texture if needed

        :param tile: Tile object to return texture of
        :param size: Size to resize the tile texture to. By default size=79
        :return: Returns the texture of tile.
        """
        letter = tile.letter
        if (letter, size) not in self.texture_cache.keys():
            a, b = self.get_coordinates(letter)
            self.texture_cache[(letter, size)] = self.full_texture.subsurface((a, b, 79, 79))
            if size != 79:
                self.texture_cache[(letter, size)] = pygame.transform.scale(self.texture_cache[(letter, size)], (size, size))
        return self.texture_cache[(letter, size)]

    def get_arrow_textures(self, size=79):
        """
        Will retrieve and add to cache or fetch from cache the texture associated with
        the next turn arrow in the bottom right of the game board.

        :param size: Size to resize the arrow texture to, if not the default size of the texture file.
        :return: Returns the texture associated with the next turn arrow
        """
        if ('arrow', size) not in self.texture_cache.keys():
            self.texture_cache[('arrow', size)] = pygame.image.load(ARROW_IMAGE).convert_alpha()
            if size != ARROW_SIZE:
                self.texture_cache[('arrow', size)] = pygame.transform.scale(self.texture_cache[('arrow_clicked', size)], (size, size))
        if ('arrow_clicked', size) not in self.texture_cache.keys():
            self.texture_cache[('arrow_clicked', size)] = pygame.image.load(ARROW_CLICKED_IMAGE).convert_alpha()
            if size != ARROW_SIZE:
                self.texture_cache[('arrow_clicked', size)] = pygame.transform.scale(self.texture_cache[('arrow_clicked', size)], (size, size))
        return self.texture_cache[('arrow', size)], self.texture_cache[('arrow_clicked', size)]

    def get_back_arrow_textures(self, size=55):
        """
        Will retrieve and add to cache or fetch from cache the texture associated with
        the revert turn arrow in the top right of the game board.

        :param size: Size to resize the arrow texture to, if not the default size of the texture file.
        :return: Returns the texture associated with the revert turn arrow
        """
        if ('back_arrow', size) not in self.texture_cache.keys():
            self.texture_cache[('back_arrow', size)] = pygame.image.load(BACK_ARROW_IMAGE).convert_alpha()
            if size != BACK_ARROW_SIZE:
                self.texture_cache[('back_arrow', size)] = pygame.transform.scale(self.texture_cache[('back_arrow', size)], (size, size))
        if ('back_arrow_clicked', size) not in self.texture_cache.keys():
            self.texture_cache[('back_arrow_clicked', size)] = pygame.image.load(BACK_ARROW_CLICKED_IMAGE).convert_alpha()
            if size != BACK_ARROW_SIZE:
                self.texture_cache[('back_arrow_clicked', size)] = pygame.transform.scale(self.texture_cache[('back_arrow_clicked', size)], (size, size))
        return self.texture_cache[('back_arrow', size)], self.texture_cache[('back_arrow_clicked', size)]

    def get_coordinates(self, letter):
        """
        Returns the starting coordinates of an individual letter in "letters.png" so that each
        letter's texture can be retrieved from the master texture.

        :param letter: Character to return texture of
        :return: Returns Scrabble tile corresponding to letter
        """
        assert len(letter) == 1, 'A letter must be one character'
        letter_coordinates = LETTER_LOCATIONS[letter]
        comma = letter_coordinates.index(',')
        x, y = letter_coordinates[0:comma], letter_coordinates[comma + 1:]
        return int(x), int(y)


class LetterManager:

    alphabet = list(LETTERS)

    def __init__(self):
        self.word_manager = WordManager()

    def generate(self, num_letters):
        """
        Randomly generates a (num_letters) of Tiles that each has a randomly generated letter from
        list(alphabet), a LetterManager class variable, and returns a list of the created tiles.
        Limits the number of generations of each letter to how many occurrences it has in list(alphabet)

        :param num_letters: Number of Tiles to randomly generate
        :return: Returns a list of the randomly generated Tiles
        """
        if len(self.alphabet) > 0:
            tiles = list()
            for _ in range(0, num_letters):
                letter = random.choice(self.alphabet)
                tiles.append(Tile(letter))
                self.alphabet.remove(letter)
            print(self.word_manager.find_applicable_words(self.tiles_to_string(tiles).lower()))
            return tiles

    def generate_starting(self, num_letters):
        """
        Randomly generates a (num_letters) of Tiles that each has a randomly generated letter, however, ensures
        that there are at least MIN_STARTING_WORDS (in constants.py) that can be created with the generated Tiles.

        :param num_letters: Number of tiles to randomly generate
        :return: A list of randomly generated Tiles
        """
        tiles = self.generate(num_letters)
        while len(self.word_manager.find_applicable_words(self.tiles_to_string(tiles).lower())) < MIN_STARTING_WORDS:
            tiles = self.generate(num_letters)
        return tiles

    def tiles_to_string(self, tiles):
        """
        Given a list of tiles, returns a string of their respective letters.

        :param tiles: List of tiles to return the letters of
        :return: Returns a string of each tile's letter
        """
        string = ""
        for tile in tiles:
            string += tile.letter
        return string

    def create_player_tiles(self, num_randoms):
        """
        Creates a number (num_randoms) of Tiles, randomly generated using method generate_starting,
        and set their locations to the starting locations of player tiles.

        :param num_randoms: Number of player tiles to create
        :return: Returns a list of the player tiles created
        """
        randoms = self.generate_starting(num_randoms)
        for i in range(num_randoms):
            x, y = i * 81 + 6, 9 * 83 + 65
            randoms[i].x, randoms[i].y = x, y
            randoms[i].starting_x, randoms[i].starting_y = x, y
        return randoms

