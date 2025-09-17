import pygame

class Input:
    def __init__(self):
        self = self
        # Create key vars for settings
        self.rotate = pygame.K_UP
        self.goLeft = pygame.K_LEFT
        self.goRight = pygame.K_RIGHT
        self.fastDrop = pygame.K_DOWN
        self.instantDrop = pygame.K_SPACE
        self.quit = pygame.K_q #This will change to pause

    #This will handle all the keystrokes and eventlly be 
    def event_handler(self, piece, board):

        for event in pygame.event.get():
            if event.type == quit:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == self.rotate:
                    piece.rotate(board)
                if event.key == self.goLeft:
                    piece.go_side(-1, board)
                if event.key == self.goRight:
                    piece.go_side(1, board)
                if event.key == self.fastDrop:
                    pressing_down = True
                    return True
                if event.key == self.instantDrop:
                    piece.instant_drop(board)
                if event.key == self.quit:
                    return False # TEMP
                    #TODO: Figure out quiting/Pausing
        