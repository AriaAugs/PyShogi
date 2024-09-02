import pygame

class gameWindow():
    # TODO - remove default argument
    def __init__(self, game_state = None):
        # initialize Pygame
        if not pygame.get_init():
            pygame.init()
        # game to dsiplay/control
        self.game_state = {
            'r1': ["red", pygame.Rect(0, 0, 40, 40)],
            'r2': ["green", pygame.Rect(300, 300, 60, 60)]
        }
        # keep track of the selected piece
        self.drag_item = None
        self.drag_rollback = None
        # whether or not to run this game window
        self.running = False
    
    def handleEvent(self, event):
        #print(event)
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.game_state['r1'][1].collidepoint(event.pos):
                    self.drag_item = self.game_state['r1'][1]
                    self.drag_rollback = pygame.Rect(self.drag_item)
            if event.button == 3 and self.drag_item != None:
                self.game_state['r1'][1] = self.drag_rollback
                self.drag_item = None
                self.drag_rollback = None
        if event.type == pygame.MOUSEBUTTONUP:
            self.drag_item = None
            self.drag_rollback = None
        if self.drag_item != None:
            self.drag_item.center = pygame.mouse.get_pos()
        

    def render(self, screen):
        screen.fill("black")
        keys = self.game_state.keys()
        for key in keys:
            item = self.game_state[key]
            screen.fill(item[0], item[1])
        pygame.display.flip()
    
    def run(self):
        # initialize display stuff
        screen = pygame.display.set_mode((720, 720))
        clock = pygame.time.Clock()
        # main game loop
        self.running = True
        while self.running:
            # handle all the game events
            for event in pygame.event.get():
                self.handleEvent(event)
            # render the game
            self.render(screen)
            # limit the FPS to 60
            clock.tick(60)
        # no need to do pygame.quit() - pygame is
        # uninitialized automatically when the
        # Python interpreter shuts down. We don't
        # want to uninitialize pygame while it's
        # still needed

if __name__ == '__main__':
    # using this for testing purposes only
    test_game = gameWindow()
    test_game.run()