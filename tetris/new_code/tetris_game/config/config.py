#Json based config file that will load a default config file for settings and controls
# can be edited by the user to change settings and saved

import json
import pygame # type: ignore (ignores the "could not resolve" error)
import shutil
import os

class Config:
    def __init__(self):
        self.default_config_file = "config/default_settings.json"
        self.user_config_file = "config/user_settings.json"

        self._check_for_config()
        self._load_user_settings()

        self.window_width = self.get_graphics_setting('window_width')
        self.window_height = self.get_graphics_setting('window_height')
        
        self.fps = self.get_graphics_setting('fps')

        self.counter = 0


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
                "fps": 100000
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
    
    def get_all_controls(self):
        return self.settings.get('controls', {})

    def get_control(self, action):
        return self.settings.get('controls', {}).get(action)
    
    def get_graphics_setting(self, setting):
        return self.settings.get('graphics', {}).get(setting)