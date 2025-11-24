"""
    Author: Nathaniel Brewer

    Json based config file that will load a default config file for settings and controls
    can be edited by the user to change settings and saved
"""


import json
import pygame # type: ignore (ignores the "could not resolve" error)
import shutil
import os

class Config:
    def __init__(self):

        self.default_config_file = "config/default_settings.json"
        self.user_config_file = "config/user_settings.json"
        self.sound_dir = "assets/sound"

        self._check_for_config()
        self._load_user_settings()

        self.window_width = self.get_graphics_setting('window_width')
        self.window_height = self.get_graphics_setting('window_height')
        
        self.fps = self.get_graphics_setting('fps')

        self.counter = 0

<<<<<<< Updated upstream
=======
        self.load_sounds()

        self.play_sounds = self.get_sound_setting("play_sounds")

        # The amount the counter will increase. 
        self.level = 1
>>>>>>> Stashed changes

    # On creation of the config object it wi
    def _check_for_config(self):
        os.makedirs("config", exist_ok=True)

        if not os.path.exists(self.default_config_file):
            self._create_default_config()

        if not os.path.exists(self.user_config_file):
            shutil.copy2(self.default_config_file, self.user_config_file)
        
    def _create_default_config(self):
        default_settings = {
            "graphics": {
                "window_width" : 400,
                "window_height" : 500,
                "fps": 25
            },
              "sound": {
                "play_sounds": True
            },
            "controls": {
                "move_left": pygame.K_LEFT,
                "move_right": pygame.K_RIGHT,
                "soft_drop": pygame.K_DOWN,
                "hard_drop": pygame.K_SPACE,
                "rotate": pygame.K_UP,
                "quit": pygame.K_q,
                "pause": pygame.K_ESCAPE
            }
        }

        with open(self.default_config_file, 'w') as file:
            json.dump(default_settings, file, indent=2)

    def _restore_from_default(self):
        self._create_default_config()
        shutil.copy2(self.default_config_file, self.user_config_file)
    
    def _load_user_settings(self):
        try:
            with open(self.user_config_file, 'r') as file:
                self.settings = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            self._restore_from_default()
            with open(self.user_config_file, 'r') as file:
                self.settings = json.load(file)
    
    """
        Controls
    """

    def get_all_controls(self):
        return self.settings.get('controls', {})

    def get_control(self, action):
        return self.settings.get('controls', {}).get(action)
    
    def save_controls(self, controls_dict):
        # Update the settings dictionary
        for action, key_code in controls_dict.items():
            self.settings['controls'][action] = key_code
        
        # Write to file
        with open(self.user_config_file, 'w') as file:
            json.dump(self.settings, file, indent=2)
    
    def get_graphics_setting(self, setting):
        return self.settings.get('graphics', {}).get(setting)
    
    """
        Sound
    """

    def load_sounds(self):
        # Load click sound
        click_sound_path = os.path.join(self.sound_dir, 'clickSound.wav')
        if os.path.exists(click_sound_path):
            pygame.mixer.init()
            self.click_sound = pygame.mixer.Sound(click_sound_path)
        else:
            self.click_sound = None

    def get_sound_setting(self, setting):
        return self.settings.get('sound', {}).get(setting)
    
    def set_sound_setting(self, setting, value):
        # Update sound setting
        if 'sound' not in self.settings:
            self.settings['sound'] = {}
        self.settings['sound'][setting] = value
        
        # Update the play_sounds variable immediately
        if setting == 'play_sounds':
            self.play_sounds = value
        
        # Write to file
        with open(self.user_config_file, 'w') as file:
            json.dump(self.settings, file, indent=2)

    def play_click_sound(self):
        # Play the click sound effect
        if self.click_sound is not None and self.play_sounds is True:
            self.click_sound.play()
    