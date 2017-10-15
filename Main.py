from Player import *
from Board import *
from pygame.locals import *
from pygame import time
from Renderer import Renderer
import _thread
import sys
import time


class Main:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Scrabble")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = pygame.image.load(BACKGROUND_IMAGE).convert_alpha()
        self.letter_generator = LetterGenerator()
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.player.tiles = self.letter_generator.create_player_tiles(STARTING_RANDOMS)
        self.board = Board(self.player)
        self.render_engine = Renderer(self.board, self.screen)
        self.running = True
        _thread.start_new_thread(self.start(), ())

    def start(self):
        player_dragging_tile = False
        tile_being_dragged = None
        changed_tiles = list()
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.end_process()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.check_turn(changed_tiles)
                    changed_tiles = list()
                if event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if player_dragging_tile:
                        for row in self.board.tiles:
                            for tile in row:
                                if tile.rect.colliderect(pygame.Rect(x, y, 1, 1)):
                                    changed_tiles.append(str(tile.row) + "," + str(tile.col))
                                    tile.change_to(tile_being_dragged.letter)
                                    tile.occupied = True
                                    tile_being_dragged.visible = False
                        tile_being_dragged.reset()
                        tile_being_dragged = None
                        player_dragging_tile = False
                    else:
                        for random_tile in self.player.tiles:
                            if random_tile.rect.collidepoint(x, y) and random_tile.visible:
                                        player_dragging_tile = True
                                        random_tile.being_dragged = True
                                        tile_being_dragged = random_tile
                                        time.sleep(0.5)
                        if self.render_engine.arrow.rect.collidepoint(x, y):
                            print("CLICK")
                            self.check_turn(changed_tiles)
                            changed_tiles = list()
            self.run()

    def run(self):
        self.clock.tick(60)
        self.screen.blit(self.background, (0, 0))
        self.render_engine.render()
        pygame.display.update()

    def end_process(self):
        self.running = False
        pygame.quit()
        sys.exit()

    def check_turn(self, changed_tiles):
        print("Checking Move")
        if self.board.check_if_good_move(changed_tiles):
            print("Good Move")
            print("WORDS", self.board.words_list)
            print("POINTS", self.board.checker.calculate_points(self.board.words_list))
            self.player.points += self.board.checker.calculate_points(self.board.words_list)
            self.board.regenerate_randoms()
        else:
            print("REVERT")
            self.board.revert(changed_tiles)

m = Main()