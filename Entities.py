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
            self.rect = None
            self.being_dragged = False

        def change_to(self, letter):
            old_letter = self.letter
            self.letter = letter
            self.value = LETTER_VALUES[self.letter]
            return old_letter

        def reset(self):
            self.x = self.starting_x
            self.y = self.starting_y
            self.being_dragged = False


class Arrow(pygame.sprite.Sprite):

    def __init__(self, size=79):
        super().__init__()
        self.rect, self.x, self.y, self.size = None, None, None, size

    def set_rect(self, x, y):
        self.x, self.y = x, y
        self.rect = pygame.Rect(x, y, self.size, self.size)