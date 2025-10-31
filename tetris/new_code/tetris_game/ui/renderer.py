import pygame # type: ignore (ignores the "could not resolve" error)

from ..main.constants import COLORS, BLACK, WHITE, GRAY

# StartX/Y position in the screen
xStart = 100
yStart = 60

# Block pixel size
block_pixel_size = 20

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.xStart = xStart
        self.yStart = yStart
        self.block_pixel_size = block_pixel_size
        self.font = font = pygame.font.SysFont('Comic Sans', 25, True, False)

    def render_board(self, board):
        self.screen.fill(WHITE)

        for i in range(board.height):
            for j in range(board.width):
                pygame.draw.rect(
                    self.screen, 
                    GRAY, 
                    [
                        self.xStart + self.block_pixel_size * j, 
                        self.yStart + self.block_pixel_size * i, 
                        self.block_pixel_size, 
                        self.block_pixel_size
                    ], 
                    1
                )
                if board.field[i][j] > 0:
                    pygame.draw.rect(
                        self.screen, 
                        COLORS[board.field[i][j]],
                        [
                            self.xStart + self.block_pixel_size * j + 1, 
                            self.yStart + self.block_pixel_size * i + 1, 
                            self.block_pixel_size - 2, 
                            self.block_pixel_size - 1
                        ]
                    )

    def draw_piece(self, piece):
        figure = piece.get_figure()
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in figure:
                    pygame.draw.rect(
                        self.screen,
                        COLORS[piece.color],
                        [
                            self.xStart + self.block_pixel_size * (j + piece.xShift) + 1,
                            self.yStart + self.block_pixel_size * (i + piece.yShift) + 1,
                            self.block_pixel_size - 2, 
                            self.block_pixel_size - 2
                        ]
                    )
    

    def clear():
        #TODO: clean unused attributes (states)
        return False