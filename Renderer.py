from constants import *
from Managers import TextureManager
from Entities import Arrow
import pygame


class Renderer:

    def __init__(self, board, screen):
        self.screen = screen
        self.texture_manager = TextureManager()
        self.arrow = Arrow()
        self.board = board
        self.player = self.board.player
        self.points_font = pygame.font.SysFont(FONT, FONT_SIZE)

    def render(self):
        self.render_tiles()
        self.render_player_tiles(self.board.player)
        self.render_arrow()
        self.render_score()

    def render_tiles(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x, y = row * TILE_SIZE + (row + 1) + 5, col * TILE_SIZE + (col + 1) + 60
                tile = self.board.tiles[row][col]
                tile_texture = self.texture_manager.get_tile_texture(tile, TILE_SIZE)
                self.screen.blit(tile_texture, (x, y))

    def render_player_tiles(self, player):
        mx, my = pygame.mouse.get_pos()
        for i in range(STARTING_RANDOMS):
            x, y = player.tiles[i].x, player.tiles[i].y
            if player.tiles[i].being_dragged:
                mx -= DRAGGED_TILE_SIZE // 2
                my -= DRAGGED_TILE_SIZE // 2
                tile_texture = self.texture_manager.get_tile_texture(player.tiles[i], DRAGGED_TILE_SIZE)
                self.screen.blit(tile_texture, (mx, my))
            elif player.tiles[i].visible:
                tile_texture = self.texture_manager.get_tile_texture(player.tiles[i])
                self.screen.blit(tile_texture, (x, y))
                player.tiles[i].rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    def render_arrow(self):
        x, y = 8*81 + 6, 9*83 + 65
        arrow_texture = self.texture_manager.get_arrow_texture()
        self.screen.blit(arrow_texture, (x, y))
        self.arrow.set_rect(x, y)

    def render_score(self):
        label = self.points_font.render((str(self.player.points) + " Points"), True, (0, 0, 0))
        self.screen.blit(label, (40, 35))