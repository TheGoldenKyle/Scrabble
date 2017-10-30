import pygame

from src.game.constants import *
from src.helpers.Managers import TextureManager


class Renderer:

    def __init__(self, board, screen):
        self.screen = screen
        self.texture_manager = TextureManager()
        self.board = board
        self.arrow, self.back_arrow = board.arrow, board.back_arrow
        self.player = self.board.player
        self.arrow_click, self.back_arrow_click = False, False

    def render(self):
        """
        Calls each render function
        :return: None
        """
        self.render_score()
        self.render_arrows()
        self.render_tiles()
        self.render_player_tiles()

    def render_tiles(self):
        """
        Renders the board tiles (not including the tiles the player hasn't placed
        :return: None
        """
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                x, y = col * TILE_SIZE + (col + 1) + 5, row * TILE_SIZE + (row + 1) + 60
                tile = self.board.tiles[row][col]
                tile_texture = self.texture_manager.get_texture(tile.letter, TILE_SIZE)
                self.screen.blit(tile_texture, (x, y))

    def render_player_tiles(self):
        """
        Renders player's unplaced tiles.
        :return: None
        """
        mx, my = pygame.mouse.get_pos()
        for i in range(STARTING_RANDOMS):
            x, y = self.player.tiles[i].x, self.player.tiles[i].y
            if self.player.tiles[i].being_dragged:
                mx -= DRAGGED_TILE_SIZE // 2
                my -= DRAGGED_TILE_SIZE // 2
                tile_texture = self.texture_manager.get_texture(self.player.tiles[i].letter, DRAGGED_TILE_SIZE)
                self.screen.blit(tile_texture, (mx, my))
            elif self.player.tiles[i].visible:
                tile_texture = self.texture_manager.get_texture(self.player.tiles[i].letter)
                self.screen.blit(tile_texture, (x, y))
                self.player.tiles[i].rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    def render_arrows(self):
        """
        Renders next move button (bottom right), and reset move button (top right)
        :return: None
        """
        if self.arrow_click:
            arrow_texture = self.texture_manager.get_texture('arrow_clicked', ARROW_SIZE)
        else:
            arrow_texture = self.texture_manager.get_texture('arrow', ARROW_SIZE)

        if self.back_arrow_click:
            back_arrow_texture = self.texture_manager.get_texture('back_arrow_clicked', BACK_ARROW_SIZE)
        else:
            back_arrow_texture = self.texture_manager.get_texture('back_arrow', BACK_ARROW_SIZE)

        self.screen.blit(back_arrow_texture, (BACK_ARROW_X, BACK_ARROW_Y))
        self.screen.blit(arrow_texture, (ARROW_X, ARROW_Y))

    def render_score(self):
        """
        Renders the player's score
        :return: None
        """
        font = pygame.font.SysFont(FONT, FONT_SIZE)
        label = font.render((str(self.player.points) + " Points"), True, (0, 0, 0))
        self.screen.blit(label, (40, 35))
