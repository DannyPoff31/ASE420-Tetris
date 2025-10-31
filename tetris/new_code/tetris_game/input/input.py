import pygame # type: ignore (ignores the "could not resolve" error)
 
from ..game.piece_action import PieceAction

class Input:
    def __init__(self, config):
        self.config = config
        self.key_to_action = {
            config.get_control('move_left') : PieceAction.MOVE_LEFT,
            config.get_control('move_right'): PieceAction.MOVE_RIGHT,
            config.get_control('soft_drop'): PieceAction.SOFT_DROP,
            config.get_control('hard_drop'): PieceAction.HARD_DROP,
            config.get_control('rotate'): PieceAction.ROTATE_CLOCKWISE,
            config.get_control('pause'): PieceAction.PAUSE,
            config.get_control('quit'): PieceAction.QUIT
        }

    def get_actions(self):
        actions = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                actions.append(PieceAction.QUIT)
            elif event.type == pygame.KEYDOWN:
                action = self.key_to_action.get(event.key)
                if action:
                    actions.append(action)
        
        return actions
    
    # Check if the down key is currently being held
    def is_down_pressed(self):
        keys = pygame.key.get_pressed()
        down_key = self.config.get_control('soft_drop')
        return keys[down_key]
