import pygame
from constants import *


class Tile(pygame.sprite.Sprite):

        def __init__(self, letter, row=-1, col=-1):
            super().__init__()
            self.visible = True
            self.is_occupied = False
            self.starting_x, self.starting_y = 0, 0
            self.x, self.y = 0, 0
            self.row, self.col = row, col
            self.letter = letter
            self.value = LETTER_VALUES[letter]
            self.moved = False
            self.being_dragged = False

        def change_to(self, letter):
            """
            Changes a tile's letter to (param: letter), and updates it value
            to the value of (param: letter)

            :param letter: Letter to change the tile to.

            :return: Returns the previous letter of the Tile.
            """
            old_letter = self.letter
            self.letter = letter
            self.value = LETTER_VALUES[self.letter]
            return old_letter

        def reset(self):
            """
            Resets the tiles position to its starting position, and sets its
            being_dragged attribute to False.

            :return: None
            """
            self.x, self.y = self.starting_x, self.starting_y
            self.being_dragged = False


class Arrow(pygame.sprite.Sprite):

    def __init__(self, size=79):
        super().__init__()
        self.x, self.y = ARROW_X, ARROW_Y
        self.rect = pygame.Rect(self.x, self.y, size, size)


class BackArrow(pygame.sprite.Sprite):

    def __init__(self, size=79):
        super().__init__()
        self.x, self.y = BACK_ARROW_X, BACK_ARROW_Y
        self.rect = pygame.Rect(self.x, self.y, size, size)
