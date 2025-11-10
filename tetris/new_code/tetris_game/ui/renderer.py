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
        self.font = pygame.font.SysFont('Comic Sans', 25, True, False)

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
    
    def draw_score(self, score):
        # Calculate position to the right of the board
        score_x = self.xStart + (self.block_pixel_size * 9) + 30  # 10 = board width, 30 = padding
        score_y = self.yStart + 20
        
        # Render "SCORE" label
        label_text = self.font.render('SCORE', True, BLACK)
        self.screen.blit(label_text, (score_x, score_y))
        
        # Render the actual score value below the label
        score_text = self.font.render(str(score), True, BLACK)
        self.screen.blit(score_text, (score_x, score_y + 35))

    def _render_buttons(self, buttons):
        self.screen.fill(WHITE)
        for button in buttons:
            pygame.draw.rect(self.screen, (0, 128, 255), button["rect"])
            text = self.font.render(button["label"], True, (255, 255, 255))
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
            pygame.display.flip()

    def render_menu(self, buttons):
        self._render_buttons(buttons)

    def render_gameover(self, buttons):
        self._render_buttons(buttons)

    def render_pause(self, buttons):
        self._render_buttons(buttons)

    def clear(self):
        self.screen.fill(WHITE)
        return