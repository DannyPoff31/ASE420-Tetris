import pygame

from constants import COLORS, BLACK, WHITE, GRAY

# StartX/Y position in the screen
xStart = 100
yStart = 60

# Block pixel size
blockPixelSize = 20

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.xStart = xStart
        self.yStart = yStart
        self.blockPixelSize = blockPixelSize
        self.font = font = pygame.font.SysFont('Comic Sans', 25, True, False)

    def renderBoard(self, board):
        self.screen.fill(WHITE)

        for i in range(board.height):
            for j in range(board.width):
                pygame.draw.rect(
                    self.screen, 
                    GRAY, 
                    [
                        self.xStart + self.blockPixelSize * j, 
                        self.yStart + self.blockPixelSize * i, 
                        self.blockPixelSize, 
                        self.blockPixelSize
                    ], 
                    1
                )
                if board.field[i][j] > 0:
                    pygame.draw.rect(
                        self.screen, 
                        COLORS[board.field[i][j]],
                        [
                            self.xStart + self.blockPixelSize * j + 1, 
                            self.yStart + self.blockPixelSize * i + 1, 
                            self.blockPixelSize - 2, 
                            self.blockPixelSize - 1
                        ]
                    )

    def drawPiece(self, piece):
        figure = piece.getFigure()
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in figure:
                    pygame.draw.rect(
                        self.screen,
                        COLORS[piece.color],
                        [
                            self.xStart + self.blockPixelSize * (j + piece.xShift) + 1,
                            self.yStart + self.blockPixelSize * (i + piece.yShift) + 1,
                            self.blockPixelSize - 2, 
                            self.blockPixelSize - 2
                        ]
                    )
    

    def clear():
        #TODO: clean unused attributes (states)
        return False