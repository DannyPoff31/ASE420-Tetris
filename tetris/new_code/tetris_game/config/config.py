"""
    Author: Nathaniel Brewer

    Json based config file that will load a default config file for settings and controls
    can be edited by the user to change settings and saved
"""

import json
import pygame # type: ignore (ignores the "could not resolve" error)
import shutil
import os

from ..gamemodes.abstract_gamemode import AbstractGamemode

class Config:
    def __init__(self):

        self.default_config_file = "config/default_settings.json"
        self.user_config_file = "config/user_settings.json"
        self.sound_dir = "assets/sound"
        self.img_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'img')

        self._check_for_config()
        self._load_user_settings()

        self.window_width = self.get_graphics_setting('window_width')
        self.window_height = self.get_graphics_setting('window_height')
        
        self.fps = self.get_graphics_setting('fps')

        self.counter = 0

        self.load_sounds()

        # Get sound setting, default to True if not set
        self.play_sounds = self.get_sound_setting("play_sounds")
        if self.play_sounds is None:
            self.play_sounds = True

        # The amount the counter will increase. 
        self.level = 1

        # Create default gamemode
        self.pending_gamemode = None

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
        pygame.mixer.init()
        
        # Load click sound
        click_sound_path = os.path.join(self.sound_dir, 'clickSound.wav')
        if os.path.exists(click_sound_path):
            self.click_sound = pygame.mixer.Sound(click_sound_path)
        else:
            self.click_sound = None
        
        bgm_path = os.path.join(self.img_dir, 'bgm.mp3')
        if os.path.exists(bgm_path):
            pygame.mixer.music.load(bgm_path)
            self.bgm_loaded = True
        else:
            self.bgm_loaded = False
        block_sound_path = os.path.join(self.img_dir, 'blockSound.wav')
        if os.path.exists(block_sound_path):
            self.block_sound = pygame.mixer.Sound(block_sound_path)
        else:
            self.block_sound = None
        
        bomb_sound_path = os.path.join(self.img_dir, 'bombSound.mp3')
        if os.path.exists(bomb_sound_path):
            self.bomb_sound = pygame.mixer.Sound(bomb_sound_path)
        else:
            self.bomb_sound = None

    def get_sound_setting(self, setting):
        return self.settings.get('sound', {}).get(setting)
    
    def set_sound_setting(self, setting, value):
        # Update sound setting
        if 'sound' not in self.settings:
            self.settings['sound'] = {}
        self.settings['sound'][setting] = value
        
        # Update the play_sounds variable immediately
        if setting == 'play_sounds':
            old_value = self.play_sounds
            self.play_sounds = value
            
            if old_value != value:
                if value:
                    if self.bgm_loaded:
                        pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.stop()
        
        # Write to file
        with open(self.user_config_file, 'w') as file:
            json.dump(self.settings, file, indent=2)

    def play_click_sound(self):
        # Play the click sound effect
        if self.click_sound is not None and self.play_sounds:
            self.click_sound.play()
    
    def play_bgm(self):
        # Play background music in loop
        if self.bgm_loaded and self.play_sounds:
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
    
    def stop_bgm(self):
        # Stop background music
        pygame.mixer.music.stop()
    
    def play_block_sound(self):
        if self.block_sound is not None and self.play_sounds:
            self.block_sound.play()
    
    def play_bomb_sound(self):
        if self.bomb_sound is not None and self.play_sounds:
            self.bomb_sound.play()
    