from copy import copy, deepcopy
import pygame

class GameWindow():
    """__summary___

    Attributes
        __attr__ : __type__
            __summary__
        __attr__ : __type__
            __summary__
            __summary__
            __summary__

    Methods
        __method__
            __summary__
        __method__
            __summary__
            __summary__
    """
    # TODO - remove default argument

    def __init__(self, game_state = None):
        # initialize Pygame
        if not pygame.get_init():
            pygame.init()
        # game to display/control
        # TODO - replace this with the actual game state
        # the demo game_state is an array of arrays
        # each sub-array contains the color and Rectangle object
        # for each rectangle to draw
        self.game_state = game_state
        # keep track of the selected piece
        self.drag_item = None
        self.drag_rollback = None
        # whether or not to run this game window
        self.running = False
        # these are created once self.run() is called
        self.screen = None
        self.clock = None

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

    def render(self):
        self.screen.fill("black")
        self.game_state.board.draw(self.screen)
        self.game_state.pieces.draw(self.screen)
        pygame.display.flip()

    def run(self):
        # initialize display stuff
        self.screen = pygame.display.set_mode((720, 720))
        self.clock = pygame.time.Clock()
        # main game loop
        self.running = True
        while self.running:
            # handle all the game events
            for event in pygame.event.get():
                self.handleEvent(event)
            # render the game
            self.render()
            # limit the FPS to 60
            self.clock.tick(60)
        # no need to do pygame.quit() - pygame is
        # uninitialized automatically when the
        # Python interpreter shuts down. We don't
        # want to uninitialize pygame while it's
        # still needed

"""
Test Stuff

TODO: Remove for final version of code
"""
class GameState():
    def __init__(self, board_in, pieces_in):
        if isinstance(board_in, GameBoard):
            self.board = pygame.sprite.Group([board_in])
        else:
            self.board = board_in
        if isinstance(pieces_in, list):
            self.pieces = pygame.sprite.Group(pieces_in)
        else:
            self.pieces = pieces_in

class GameBoard(pygame.sprite.Sprite):
    def __init__(self, width, height, color):
        super().__init__(self)
        # create sprite stuff
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        # lists for the board and held pieces
        self.board = [[None for x in range(9)] for y in range(9)]
        self.held_white = []
        self.held_black = []

class GamePiece(pygame.sprite.Sprite):
    def __init__(self, width, height, color):
        # Call the parent class (Sprite) constructor
        super().__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()

if __name__ == '__main__':
    # create the pieces
    pieces = pygame.sprite.Group()
    board = GameBoard(600, 600, 'gray')
    test_game = GameWindow()
    test_game.run()
