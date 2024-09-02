import pygame

class gameWindow():
    # TODO - remove default argument
    def __init__(self, game_state = None):
        # initialize Pygame
        if not pygame.get_init():
            pygame.init()
        # game to dsiplay/control
        # TODO - replace this with the actual game state
        # the demo game_state is an array of arrays
        # each sub-array contains the color and Rectangle object
        # for each rectangle to draw
        self.game_state = [
            ["red", pygame.Rect(0, 0, 40, 40)],
            ["green", pygame.Rect(300, 300, 60, 60)]
        ]
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
                # if the left mouse button is pressed
                for rects in self.game_state:
                    rect = rects[1]
                    if rect.collidepoint(event.pos):
                        # drag 'r1' if the mouse is over the rectangle
                        self.drag_item = rect
                        self.drag_rollback = rect.copy()
            if event.button == 3 and self.drag_item != None:
                # if the right mouse button is pressed and we're dragging something,
                # rollback 'r1' to where it was before we started dragging it
                for idx in range(len(self.game_state)):
                    if self.drag_item is self.game_state[idx][1]:
                        self.game_state[idx][1] = self.drag_rollback
                        self.drag_item = None
                        self.drag_rollback = None
        if event.type == pygame.MOUSEBUTTONUP:
            # if the mouse is released, leave the rectangle where it is
            self.drag_item = None
            self.drag_rollback = None
        if self.drag_item != None:
            # if we're dragging something, center it on the mouse
            self.drag_item.center = pygame.mouse.get_pos()
        
    def render(self, screen):
        screen.fill("black")
        for rects in self.game_state:
            screen.fill(rects[0], rects[1])
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