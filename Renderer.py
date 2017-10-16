from constants import *
from Managers import TextureManager
import pygame


class Renderer:

    def __init__(self, board, screen):
        self.screen = screen
        self.texture_manager = TextureManager()
        self.board = board
        self.arrow, self.back_arrow = board.arrow, board.back_arrow
        self.player = self.board.player

    def render(self):
        self.render_score()
        self.render_arrows()
        self.render_tiles()
        self.render_player_tiles()

    def render_tiles(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x, y = row * TILE_SIZE + (row + 1) + 5, col * TILE_SIZE + (col + 1) + 60
                tile = self.board.tiles[row][col]
                tile_texture = self.texture_manager.get_tile_texture(tile, TILE_SIZE)
                self.screen.blit(tile_texture, (x, y))

    def render_player_tiles(self):
        mx, my = pygame.mouse.get_pos()
        for i in range(STARTING_RANDOMS):
            x, y = self.player.tiles[i].x, self.player.tiles[i].y
            if self.player.tiles[i].being_dragged:
                mx -= DRAGGED_TILE_SIZE // 2
                my -= DRAGGED_TILE_SIZE // 2
                tile_texture = self.texture_manager.get_tile_texture(self.player.tiles[i], DRAGGED_TILE_SIZE)
                self.screen.blit(tile_texture, (mx, my))
            elif self.player.tiles[i].visible:
                tile_texture = self.texture_manager.get_tile_texture(self.player.tiles[i])
                self.screen.blit(tile_texture, (x, y))
                self.player.tiles[i].rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    def render_arrows(self):
        arrow_texture = self.texture_manager.get_arrow_texture(ARROW_SIZE)
        back_arrow_texture = self.texture_manager.get_back_arrow_texture(BACK_ARROW_SIZE)
        self.screen.blit(back_arrow_texture, (BACK_ARROW_X, BACK_ARROW_Y))
        self.screen.blit(arrow_texture, (ARROW_X, ARROW_Y))

    def render_score(self):
        font = pygame.font.SysFont(FONT, FONT_SIZE)
        label = font.render((str(self.player.points) + " Points"), True, (0, 0, 0))
        self.screen.blit(label, (40, 35))
