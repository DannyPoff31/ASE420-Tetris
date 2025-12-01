"""
    Author: Nathaniel Brewer

    Settings state, child of abstract_state. Handles all things to do with settings
"""
import pygame
from .abstract_state import AbstractState

class Setting(AbstractState):
    def __init__(self, config, input, renderer):
        super().__init__(config, input, renderer)
        
        self.drawn = False

        self.controls = self.config.get_all_controls()
        
        # Sound settings
        self.sound_enabled = self.config.get_sound_setting('play_sounds')
        if self.sound_enabled is None:
            self.sound_enabled = True
        
        # Checkbox for sound
        self.sound_checkbox_rect = pygame.Rect(50, 370, 25, 25)
        
        # Track which control is being remapped
        self.remapping_action = None
        self.waiting_for_input = False

        # Buttons for each control mapping
        self.control_buttons = []
        self._create_control_buttons()
        
        # Action buttons - centered with spacing
        button_width = 150
        button_height = 40
        button_spacing = 10
        total_width = (button_width * 2) + button_spacing
        start_x = (self.config.window_width - total_width) // 2
        
        self.buttons = [
            {"label": "Save", "rect": pygame.Rect(start_x, 430, button_width, button_height)},
            {"label": "Back to Menu", "rect": pygame.Rect(start_x + button_width + button_spacing, 430, button_width, button_height), "action": "menu"},
        ]

    def _create_control_buttons(self):

        self.control_buttons = []
        y_offset = 80
        spacing = 40
        
        action_names = {
            'move_left': 'Move Left',
            'move_right': 'Move Right',
            'soft_drop': 'Soft Drop',
            'hard_drop': 'Hard Drop',
            'rotate': 'Rotate',
            'pause': 'Pause',
            'quit': 'Quit'
        }
        
        for action, display_name in action_names.items():
            button_rect = pygame.Rect(200, y_offset, 150, 30)
            self.control_buttons.append({
                'action': action,
                'display_name': display_name,
                'rect': button_rect
            })
            y_offset += spacing

    def cleanup(self):
        self.renderer.clear()
        self.startup()

    def startup(self):
        self.drawn = False
        self.remapping_action = None
        self.waiting_for_input = False
        self.controls = self.config.get_all_controls()
        self.sound_enabled = self.config.get_sound_setting('play_sounds')
        if self.sound_enabled is None:
            self.sound_enabled = True

    def restart(self):
        self.startup()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            # If waiting for key input to remap
            if self.waiting_for_input and event.type == pygame.KEYDOWN:
                # Remap the control
                self.controls[self.remapping_action] = event.key
                self.waiting_for_input = False
                self.remapping_action = None
                self.drawn = False  # Redraw to show new mapping
                self.config.play_click_sound()
                continue
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.waiting_for_input:
                mouse_pos = event.pos
                
                # Check sound checkbox
                if self.sound_checkbox_rect.collidepoint(mouse_pos):
                    self.sound_enabled = not self.sound_enabled
                    self.drawn = False  # Redraw to show new state
                    self.config.play_click_sound()
                    continue
                
                # Check control buttons
                for control_btn in self.control_buttons:
                    if control_btn['rect'].collidepoint(mouse_pos):
                        self.remapping_action = control_btn['action']
                        self.waiting_for_input = True
                        self.drawn = False  # Redraw to show waiting state
                        self.config.play_click_sound()
                        break
                
                # Check action buttons (Save, Back)
                for button in self.buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        self.config.play_click_sound()
                        if button["label"] == "Save":
                            self._save_controls()
                            continue
                        elif "action" in button:
                            return button["action"]
        
        if not self.drawn:
            self.draw()
            self.drawn = True
        return 'settings'

    def _save_controls(self):
        # Save controls to config file
        self.config.save_controls(self.controls)
        
        # Save sound setting
        self.config.set_sound_setting('play_sounds', self.sound_enabled)
        
        # Reload input mappings
        self.input.reload_key_mappings()

    def _get_key_name(self, key_code):
        # Convert pygame key code to readable name
        return pygame.key.name(key_code).upper()

    def draw(self):
        # Clear screen
        self.renderer.clear()
        
        # Draw title
        font_large = pygame.font.Font(None, 48)
        title_surface = font_large.render("Controls", True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(self.config.window_width // 2, 30))
        self.renderer.screen.blit(title_surface, title_rect)
        
        # Draw control mappings in two columns
        font = pygame.font.Font(None, 28)
        
        for control_btn in self.control_buttons:
            action = control_btn['action']
            display_name = control_btn['display_name']
            rect = control_btn['rect']
            
            # Draw action name (left column)
            action_surface = font.render(display_name + ":", True, (0, 0, 0))
            action_rect = action_surface.get_rect(right=rect.left - 10, centery=rect.centery)
            self.renderer.screen.blit(action_surface, action_rect)
            
            # Draw key button (right column)
            if self.waiting_for_input and self.remapping_action == action:
                # Highlight button when waiting for input
                pygame.draw.rect(self.renderer.screen, (255, 200, 0), rect)
                key_text = "Press Key..."
                text_color = (0, 0, 0)
            else:
                # Normal button
                pygame.draw.rect(self.renderer.screen, (100, 100, 100), rect)
                pygame.draw.rect(self.renderer.screen, (255, 255, 255), rect, 2)
                key_text = self._get_key_name(self.controls[action])
                text_color = (255, 255, 255)
            
            key_surface = font.render(key_text, True, text_color)
            key_rect = key_surface.get_rect(center=rect.center)
            self.renderer.screen.blit(key_surface, key_rect)
        
        # Draw sound settings section
        sound_y = 370
        sound_label = font.render("Enable Sound:", True, (0, 0, 0))
        sound_label_rect = sound_label.get_rect(left=50, centery=sound_y + 12)
        self.renderer.screen.blit(sound_label, sound_label_rect)
        
        # Draw checkbox
        checkbox_rect = pygame.Rect(200, sound_y, 25, 25)
        self.sound_checkbox_rect = checkbox_rect  # Update for click detection
        
        # Checkbox border
        pygame.draw.rect(self.renderer.screen, (0, 0, 0), checkbox_rect, 2)
        
        # Checkbox fill if enabled
        if self.sound_enabled:
            # Draw checkmark
            check_color = (0, 255, 0)
            pygame.draw.line(self.renderer.screen, check_color, 
                           (checkbox_rect.left + 5, checkbox_rect.centery), 
                           (checkbox_rect.centerx, checkbox_rect.bottom - 5), 3)
            pygame.draw.line(self.renderer.screen, check_color, 
                           (checkbox_rect.centerx, checkbox_rect.bottom - 5), 
                           (checkbox_rect.right - 5, checkbox_rect.top + 5), 3)
        
        # Draw action buttons (Save, Back)
        for button in self.buttons:
            pygame.draw.rect(self.renderer.screen, (70, 70, 70), button["rect"])
            pygame.draw.rect(self.renderer.screen, (255, 255, 255), button["rect"], 2)
            
            label_surface = font.render(button["label"], True, (255, 255, 255))
            label_rect = label_surface.get_rect(center=button["rect"].center)
            self.renderer.screen.blit(label_surface, label_rect)
        
        pygame.display.flip()

