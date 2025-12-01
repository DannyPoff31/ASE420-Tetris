"""
    Author: Nathaniel Brewer
    
    GameMode Selection State - Two phase selection:
    Phase 1: Choose between Classic and Special mode
    Phase 2: If Special, select which special pieces to include
"""
import pygame # type: ignore
from .abstract_state import AbstractState

from ..gamemodes.classic import Classic
from ..gamemodes.special_gamemode import Special

class GamemodeSelection(AbstractState):
    def __init__(self, config, input, renderer):
        super().__init__(config, input, renderer)
        self.next = 'game'

        self.drawn = False
        
        # Selection phases
        self.current_phase = 1  # 1 = mode selection, 2 = special piece selection
        
        # Mode selection
        self.selected_mode = None  # 'classic' or 'special'
        
        # Special piece selection (for phase 2)
        self.available_special_pieces = ['rocket']
        self.selected_special_pieces = []

        # Phase 1 buttons - Mode Selection (centered for 400px wide screen)
        button_width = 200
        button_x = (400 - button_width) // 2  # Center horizontally
        self.mode_buttons = [
            {"label": "Classic Mode", "rect": pygame.Rect(button_x, 150, button_width, 60), "action": "classic"},
            {"label": "Special Mode", "rect": pygame.Rect(button_x, 230, button_width, 60), "action": "special"},
            {"label": "Back to Menu", "rect": pygame.Rect(button_x, 310, button_width, 60), "action": "menu"}
        ]
        
        # Phase 2 buttons - Special Piece Selection (centered for 400px wide screen)
        self.piece_selection_buttons = []
        button_width = 200
        button_x = (400 - button_width) // 2  # Center horizontally
        self.confirm_button = {"label": "Confirm Selection", "rect": pygame.Rect(button_x, 400, button_width, 50), "action": "confirm"}
        self.back_button = {"label": "Back", "rect": pygame.Rect(button_x, 460, button_width, 50), "action": "back"}
        
        # Gamemode creation
        self.created_gamemode = None

        # Initialize piece selection buttons
        self._init_piece_selection_buttons()

    def _init_piece_selection_buttons(self):
        # Initialize the special piece selection buttons in a grid (centered for 400px wide screen)
        button_width = 120
        button_height = 80
        spacing = 20
        grid_width = button_width * 2 + spacing  # 2 columns
        start_x = (400 - grid_width) // 2  # Center the grid
        start_y = 100
        
        # generate all available special pieces to this menu
        for i, piece_type in enumerate(self.available_special_pieces):
            row = i // 2
            col = i % 2
            
            x = start_x + col * (button_width + spacing)
            y = start_y + row * (button_height + spacing)
            
            self.piece_selection_buttons.append({
                "label": piece_type.capitalize(),
                "rect": pygame.Rect(x, y, button_width, button_height),
                "piece_type": piece_type,
                "selected": False
            })

    def cleanup(self):
        self.renderer.clear()
        self.startup()

    def startup(self):
        self.drawn = False
        self.current_phase = 1
        self.selected_mode = None
        self.selected_special_pieces = []
        
        # Reset piece selection
        for button in self.piece_selection_buttons:
            button["selected"] = False

    def restart(self):
        self.startup()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                
                if self.current_phase == 1:
                    # Phase 1: Mode selection
                    result = self._handle_mode_selection(mouse_pos)
                    if result:
                        return result
                        
                elif self.current_phase == 2:
                    # Phase 2: Special piece selection
                    result = self._handle_piece_selection(mouse_pos)
                    if result:
                        return result
        
        # Redraw if needed
        if not self.drawn:
            self.draw()
            self.drawn = True
            
        return 'gamemode'

    def _handle_mode_selection(self, mouse_pos):
        # Handle phase 1 - mode selection
        for button in self.mode_buttons:
            if button["rect"].collidepoint(mouse_pos):
                self.config.play_click_sound()
                
                if button["action"] == "classic":
                    self.selected_mode = "classic"
                    self.selected_special_pieces = []
                    # Create Classic gamemode
                    gamemode = {'mode': 'classic', 'special_pieces': self.selected_special_pieces, 'include_classic': True}
                    self.created_gamemode = Classic(gamemode, self.config)
                    self.config.pending_gamemode = self.created_gamemode
                    return "game"
                    
                elif button["action"] == "special":
                    self.selected_mode = "special"
                    self.current_phase = 2
                    self.drawn = False  # Force redraw for phase 2
                    return None
                    
                elif button["action"] == "menu":
                    return "menu"
        return None

    def _handle_piece_selection(self, mouse_pos):
        # Handle phase 2 - special piece selection
        # Check piece toggle buttons
        for button in self.piece_selection_buttons:
            if button["rect"].collidepoint(mouse_pos):
                self.config.play_click_sound()
                
                # Toggle selection
                button["selected"] = not button["selected"]
                
                if button["selected"]:
                    if button["piece_type"] not in self.selected_special_pieces:
                        self.selected_special_pieces.append(button["piece_type"])
                else:
                    if button["piece_type"] in self.selected_special_pieces:
                        self.selected_special_pieces.remove(button["piece_type"])
                
                self.drawn = False  # Force redraw to show selection
                return None
        
        # Check confirm button
        if self.confirm_button["rect"].collidepoint(mouse_pos):
            if len(self.selected_special_pieces) > 0:
                gamemode = {'mode': 'special', 'special_pieces': self.selected_special_pieces, 'include_classic': True}
                self.created_gamemode = Special(gamemode, self.config)
                self.config.pending_gamemode = self.created_gamemode
                self.config.play_click_sound()
                return "game"
        
        # Check back button
        if self.back_button["rect"].collidepoint(mouse_pos):
            self.config.play_click_sound()
            self.current_phase = 1
            self.drawn = False
            return None
            
        return None

    def draw(self):
        # Draw the appropriate phase
        self.renderer.clear()
        
        if self.current_phase == 1:
            self._draw_mode_selection()
        elif self.current_phase == 2:
            self._draw_piece_selection()
        
        pygame.display.flip()

    def _draw_mode_selection(self):
        # Draw phase 1 - mode selection screen
        # Title
        font_large = pygame.font.SysFont('Comic Sans', 35, True, False)
        title = font_large.render("Select Game Mode", True, (0, 0, 0))
        title_rect = title.get_rect(center=(200, 80))  # Centered on 400px wide screen
        self.renderer.screen.blit(title, title_rect)
        
        # Draw buttons
        font = pygame.font.SysFont('Comic Sans', 25, True, False)
        for button in self.mode_buttons:
            # Button background
            pygame.draw.rect(self.renderer.screen, (101, 67, 33), button["rect"])
            pygame.draw.rect(self.renderer.screen, (0, 0, 0), button["rect"], 2)
            
            # Button text
            text = font.render(button["label"], True, (255, 255, 255))
            text_rect = text.get_rect(center=button["rect"].center)
            self.renderer.screen.blit(text, text_rect)

    def _draw_piece_selection(self):
        # Draw phase 2 - special piece selection screen

        # Title
        font_large = pygame.font.SysFont('Comic Sans', 30, True, False)
        title = font_large.render("Select Special Pieces", True, (0, 0, 0))
        title_rect = title.get_rect(center=(200, 40))  # Centered on 400px wide screen
        self.renderer.screen.blit(title, title_rect)
        
        # Instructions
        font_small = pygame.font.SysFont('Comic Sans', 18, False, False)
        instruction = font_small.render("Click to toggle pieces", True, (100, 100, 100))
        instruction_rect = instruction.get_rect(center=(200, 70))  # Centered on 400px wide screen
        self.renderer.screen.blit(instruction, instruction_rect)
        
        # Draw piece selection buttons
        font = pygame.font.SysFont('Comic Sans', 20, True, False)
        for button in self.piece_selection_buttons:
            # Button color based on selection
            if button["selected"]:
                color = (0, 200, 0)  # Green when selected
            else:
                color = (150, 150, 150)  # Gray when not selected
            
            # Button background
            pygame.draw.rect(self.renderer.screen, color, button["rect"])
            pygame.draw.rect(self.renderer.screen, (0, 0, 0), button["rect"], 3)
            
            # Button text
            text = font.render(button["label"], True, (255, 255, 255))
            text_rect = text.get_rect(center=button["rect"].center)
            self.renderer.screen.blit(text, text_rect)
            
            # Selection indicator
            if button["selected"]:
                checkmark = font.render("✓", True, (255, 255, 255))
                check_rect = checkmark.get_rect(topright=(button["rect"].right - 5, button["rect"].top + 5))
                self.renderer.screen.blit(checkmark, check_rect)
        
        # Draw confirm button (only enabled if at least one piece selected)
        if len(self.selected_special_pieces) > 0:
            confirm_color = (101, 67, 33)
        else:
            confirm_color = (100, 100, 100)
        
        pygame.draw.rect(self.renderer.screen, confirm_color, self.confirm_button["rect"])
        pygame.draw.rect(self.renderer.screen, (0, 0, 0), self.confirm_button["rect"], 2)
        text = font.render(self.confirm_button["label"], True, (255, 255, 255))
        text_rect = text.get_rect(center=self.confirm_button["rect"].center)
        self.renderer.screen.blit(text, text_rect)
        
        # Draw back button
        pygame.draw.rect(self.renderer.screen, (200, 100, 100), self.back_button["rect"])
        pygame.draw.rect(self.renderer.screen, (0, 0, 0), self.back_button["rect"], 2)
        text = font.render(self.back_button["label"], True, (255, 255, 255))
        text_rect = text.get_rect(center=self.back_button["rect"].center)
        self.renderer.screen.blit(text, text_rect)
        
        # Show count of selected pieces (centered)
        count_text = font_small.render(f"Selected: {len(self.selected_special_pieces)}", True, (0, 0, 0))
        count_rect = count_text.get_rect(center=(200, 365))  # Centered above buttons
        self.renderer.screen.blit(count_text, count_rect)
    
    def get_gamemode_config(self):
        # Return the configuration for the selected gamemode
        return {
            'mode': self.selected_mode,
            'pieces': self.selected_special_pieces if self.selected_mode == 'special' else []
        }
