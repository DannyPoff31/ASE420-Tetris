import pygame # type: ignore (ignores the "could not resolve" error)
import os

from ..main.constants import COLORS, BLACK, WHITE, GRAY, LIGHT_BROWN, DARK_BROWN, SPECIAL_BLOCK_WIDTH, SPECIAL_BLOCK_HEIGHT
import random
import math

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
        
        # Load block images
        img_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'img')
        self.block_images = {}
        for i in range(1, 7):  # block1.png to block6.png
            img_path = os.path.join(img_dir, f'block{i}.png')
            if os.path.exists(img_path):
                img = pygame.image.load(img_path)
                # Scale image to block size
                self.block_images[i] = pygame.transform.scale(img, (block_pixel_size - 2, block_pixel_size - 2))
            else:
                # Fallback to color if image not found
                self.block_images[i] = None
        
        # Load click sound
        click_sound_path = os.path.join(img_dir, 'clickSound.wav')
        if os.path.exists(click_sound_path):
            self.click_sound = pygame.mixer.Sound(click_sound_path)
        else:
            self.click_sound = None
        
        # Load special block image
        bomb_block_path = os.path.join(img_dir, 'bombBlock.png')
        if os.path.exists(bomb_block_path):
            bomb_img = pygame.image.load(bomb_block_path)
            # Scale to 3x6 block size
            special_width = block_pixel_size * SPECIAL_BLOCK_WIDTH - 2
            special_height = block_pixel_size * SPECIAL_BLOCK_HEIGHT - 2
            self.special_block_image = pygame.transform.scale(bomb_img, (special_width, special_height))
        else:
            self.special_block_image = None
        
        # Particle system for line clearing effects
        self.particles = []
    
    def play_click_sound(self):
        """Play the click sound effect"""
        if self.click_sound is not None:
            self.click_sound.play()
    
    def create_line_clear_particles(self, line_y, board_width):
        """Create particles when a line is cleared"""
        # Calculate screen position of the cleared line
        screen_y = self.yStart + self.block_pixel_size * line_y + self.block_pixel_size // 2
        
        # Create particles for each block in the line
        for j in range(board_width):
            screen_x = self.xStart + self.block_pixel_size * j + self.block_pixel_size // 2
            
            # Create multiple particles per block
            for _ in range(5):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(2, 5)
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed
                
                # Random bright and colorful colors
                color = random.choice([
                    (255, 50, 50),    # Bright Red
                    (50, 255, 50),    # Bright Green
                    (50, 50, 255),    # Bright Blue
                    (255, 255, 50),   # Bright Yellow
                    (255, 50, 255),   # Bright Magenta
                    (50, 255, 255),   # Bright Cyan
                    (255, 150, 50),   # Bright Orange
                    (150, 50, 255),   # Bright Purple
                    (50, 255, 150),   # Bright Mint
                    (255, 200, 50),   # Bright Gold
                    (200, 50, 255),   # Bright Pink
                    (50, 200, 255),   # Bright Sky Blue
                ])
                
                lifetime = random.randint(25, 45)
                
                self.particles.append({
                    'x': screen_x,
                    'y': screen_y,
                    'vx': vx,
                    'vy': vy,
                    'color': color,
                    'lifetime': lifetime,
                    'age': 0,
                    'size': random.randint(3, 5)  # Slightly larger particles
                })
    
    def update_particles(self):
        """Update all particles"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.2  # Gravity
            particle['age'] += 1
            
            if particle['age'] >= particle['lifetime']:
                self.particles.remove(particle)
    
    def draw_particles(self):
        """Draw all particles"""
        for particle in self.particles:
            # Fade out as particle ages
            alpha = 255 * (1 - particle['age'] / particle['lifetime'])
            color = tuple(min(255, max(0, int(c * (1 - particle['age'] / particle['lifetime'])))) for c in particle['color'])
            
            pygame.draw.circle(
                self.screen,
                color,
                (int(particle['x']), int(particle['y'])),
                particle['size']
            )

    def render_board(self, board):
        self.screen.fill(LIGHT_BROWN)

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
                    color_index = board.field[i][j]
                    if color_index in self.block_images and self.block_images[color_index] is not None:
                        # Use image
                        self.screen.blit(
                            self.block_images[color_index],
                            (
                                self.xStart + self.block_pixel_size * j + 1,
                                self.yStart + self.block_pixel_size * i + 1
                            )
                        )
                    else:
                        # Fallback to color
                        pygame.draw.rect(
                            self.screen, 
                            COLORS[color_index],
                            [
                                self.xStart + self.block_pixel_size * j + 1, 
                                self.yStart + self.block_pixel_size * i + 1, 
                                self.block_pixel_size - 2, 
                                self.block_pixel_size - 1
                            ]
                        )

    def draw_piece(self, piece):
        # Special block render
        if piece.is_special:
            if self.special_block_image is not None:

                self.screen.blit(
                    self.special_block_image,
                    (
                        self.xStart + self.block_pixel_size * piece.xShift + 1,
                        self.yStart + self.block_pixel_size * piece.yShift + 1
                    )
                )
            else:
                for i in range(SPECIAL_BLOCK_HEIGHT):
                    for j in range(SPECIAL_BLOCK_WIDTH):
                        pygame.draw.rect(
                            self.screen,
                            (255, 0, 0),
                            [
                                self.xStart + self.block_pixel_size * (j + piece.xShift) + 1,
                                self.yStart + self.block_pixel_size * (i + piece.yShift) + 1,
                                self.block_pixel_size - 2,
                                self.block_pixel_size - 2
                            ]
                        )
            return
        
        # Normal
        figure = piece.get_figure()
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in figure:
                    color_index = piece.color
                    if color_index in self.block_images and self.block_images[color_index] is not None:
                        # Use image
                        self.screen.blit(
                            self.block_images[color_index],
                            (
                                self.xStart + self.block_pixel_size * (j + piece.xShift) + 1,
                                self.yStart + self.block_pixel_size * (i + piece.yShift) + 1
                            )
                        )
                    else:
                        # Fallback to color
                        pygame.draw.rect(
                            self.screen,
                            COLORS[color_index],
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
        preview_block_size = int(self.block_pixel_size * 0.75)  # 75% of block size
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
                    color_index = next_piece.color
                    if color_index in self.block_images and self.block_images[color_index] is not None:
                        # Scale image for preview size
                        preview_img = pygame.transform.scale(
                            self.block_images[color_index],
                            (preview_block_size - 2, preview_block_size - 2)
                        )
                        self.screen.blit(preview_img, (block_x, block_y))
                    else:
                        # Fallback to color
                        pygame.draw.rect(
                            self.screen,
                            COLORS[color_index],
                            [
                                block_x,
                                block_y,
                                preview_block_size - 2,
                                preview_block_size - 2
                            ]
                        )

    def _render_buttons(self, buttons):
        self.screen.fill(LIGHT_BROWN)
        for button in buttons:
            pygame.draw.rect(self.screen, DARK_BROWN, button["rect"])
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

    def draw_level(self, level):
        left_margin = 10
        level_y = 10  # Top margin
        
        # Render "LEVEL" label
        label_text = self.font.render('LEVEL', True, BLACK)
        self.screen.blit(label_text, (left_margin, level_y))
        
        # Render the actual level value below the label
        level_text = self.font.render(str(level), True, BLACK)
        self.screen.blit(level_text, (left_margin, level_y + 35))

    def clear(self):
        self.screen.fill(LIGHT_BROWN)
        self.particles = []  # Clear particles when clearing screen
        return