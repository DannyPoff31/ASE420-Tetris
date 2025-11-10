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

        screen_width = self.screen.get_width()
        score_y = 10  # Top margin
        right_margin = 10
        
        label_text = self.font.render('SCORE', True, BLACK)
        label_width = label_text.get_width()
        label_x = screen_width - label_width - right_margin
        self.screen.blit(label_text, (label_x, score_y))
        
        # Render the actual score value below the label (right aligned)
        score_text = self.font.render(str(score), True, BLACK)
        score_text_width = score_text.get_width()
        score_text_x = screen_width - score_text_width - right_margin
        self.screen.blit(score_text, (score_text_x, score_y + 35))

    def draw_next_piece(self, next_piece):
        preview_block_size = 15  # Smaller size for preview (75% of original)
        preview_box_size = preview_block_size * 4 + 4
        screen_width = self.screen.get_width()
        right_margin = 10
        preview_y = 10 + 35 + 35 + 30
        
        preview_x = screen_width - preview_box_size - right_margin
        
        # NEXT text
        label_text = self.font.render('NEXT', True, BLACK)
        label_width = label_text.get_width()
        label_x = screen_width - label_width - right_margin
        self.screen.blit(label_text, (label_x, preview_y))
        
        # Draw preview background
        pygame.draw.rect(
            self.screen,
            GRAY,
            [
                preview_x,
                preview_y + 30,
                preview_box_size,
                preview_box_size
            ],
            2
        )
        
        figure = next_piece.get_figure()
        if not figure:
            return
        

        min_j = 4
        max_j = -1
        min_i = 4
        max_i = -1
        
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in figure:
                    min_j = min(min_j, j)
                    max_j = max(max_j, j)
                    min_i = min(min_i, i)
                    max_i = max(max_i, i)
        
        piece_width = max_j - min_j + 1
        piece_height = max_i - min_i + 1
        
        offset_x = (4 - piece_width) // 2 - min_j
        offset_y = (4 - piece_height) // 2 - min_i
        
        # next piece
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in figure:
                    block_x = preview_x + 2 + preview_block_size * (j + offset_x)
                    block_y = preview_y + 32 + preview_block_size * (i + offset_y)
                    pygame.draw.rect(
                        self.screen,
                        COLORS[next_piece.color],
                        [
                            block_x,
                            block_y,
                            preview_block_size - 2,
                            preview_block_size - 2
                        ]
                    )

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

    def clear(self):
        self.screen.fill(WHITE)
        return