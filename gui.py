import pygame

class gameWindow():
    # TODO - remove default argument
    def __init__(self, game_state = None):
        # initialize Pygame - this is safe to do multiple times
        pygame.init()
        # initialize display stuff
        self.screen = pygame.display.set_mode((720, 720))
        self.clock = pygame.time.Clock()
        # game to dsiplay/control
        self.game_state = {
            'r1': pygame.Rect(0, 0, 40, 40),
            'r2': pygame.Rect(300, 300, 60, 60)
        }
        # keep track of the selected piece
        self.selected = None
        # whether or not to run this game window
        self.running = False
    
    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pgame.MOUSEBUTTONDOWN:
            
        if event.type == pygame.MOUSEBUTTONUP:

    
    def run(self):
        self.running = True
        while self.running:
            # handle all the game events
            for event in pygame.event.get():
                self.handleEvent(event)
            screen.fill("purple")

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()


if __name__ == '__main__':
    # using this for testing purposes only
    pass