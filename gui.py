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
        self.game = game_state
        # keep track of the selected piece
        self.drag_item = None
        self.rollback_pos = None
        # whether or not to run this game window
        self.running = False
        # these are created once self.run() is called
        self.screen = None
        self.clock = None

    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # if the left mouse button was pressed, check if we clicked on a piece
                for piece in self.game.pieces:
                    if piece.rect.collidepoint(event.pos):
                        # we clicked on a piece, start dragging it
                        self.drag_item = piece
                        self.rollback_pos = piece.rect.center
            if event.button == 3 and self.drag_item is not None:
                # if the right mouse button is pressed and we're dragging something,
                self.drag_item.rect.center = self.rollback_pos
                self.drag_item = None
        if event.type == pygame.MOUSEBUTTONUP:
            # if the mouse was released, try snapping the piece to the grid
            pos = self.game.board.on_square(self.drag_item.rect)
            if pos is not None:
                self.game.board.snap_piece(self.drag_item.rect, pos)
            else:
                # the piece is off the grid - roll it back instead
                self.drag_item.rect.center = self.rollback_pos
            self.drag_item = None
            self.rollback_pos = None
        if self.drag_item is not None:
            # if we're dragging something, center it on the mouse
            self.drag_item.rect.center = pygame.mouse.get_pos()

    def render(self):
        # clear the screen, draw the board, draw the pieces, then flip the display
        self.screen.fill("black")
        self.game.board_group.draw(self.screen)
        self.game.pieces_group.draw(self.screen)
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
        # sprite groups for stuff
        # these are needed for drwaing all the sprites
        self.board_group = pygame.sprite.Group(board_in)
        self.pieces_group = pygame.sprite.Group(pieces_in)
        # references to the board and pieces
        # we want these so we can easily access them from the GUI
        self.board = board_in
        self.pieces = pieces_in

class GameBoard(pygame.sprite.Sprite):
    def __init__(self, board_size, color):
        # Call the parent class (Sprite) constructor
        # We could use super().__init__(), but this is more explicit
        # and avoid any issues from super() accidentally getting the wrong class
        pygame.sprite.Sprite.__init__(self)
        # create sprite stuff
        self.image = pygame.Surface(board_size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        # lists for the board and held pieces
        self.board = [[None for x in range(9)] for y in range(9)]
        self.held_white = []
        self.held_black = []
        # create an array of collision points to help check for piece placement
        self.grid = {}
        grid_rect = pygame.Rect(0, 0, board_size[0]/9, board_size[1]/9)
        for x in range(9):
            for y in range(9):
                grid_rect.topleft = (x*board_size[0]/9, y*board_size[1]/9)
                self.grid[(x, y)] = grid_rect.center

    def on_square(self, rect):
        # check to see if a rect is on a grid cell
        # this is done by checking if the rect collides with the center of the grid cell
        for key, pos in self.grid.items():
            if rect.collidepoint(pos):
                return key
        return None

    def snap_piece(self, rect, pos):
        # set a piece's position such that it is centered within a given grid cell
        x, y = pos
        grid_rect = pygame.Rect(0, 0, self.rect.width/9, self.rect.height/9)
        grid_rect.topleft = (x*self.rect.width/9, y*self.rect.height/9)
        rect.center = grid_rect.center

    def add_piece(self, piece, pos):
        # add a piece to the board and set its position
        x, y = pos
        self.board[x][y] = piece
        self.snap_piece(piece.rect, pos)

class GamePiece(pygame.sprite.Sprite):
    def __init__(self, piece_size, color):
        # Call the parent class (Sprite) constructor
        # We could use super().__init__(), but this is more explicit
        # and avoid any issues from super() accidentally getting the wrong class
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface(piece_size)
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()

if __name__ == '__main__':
    pieces = []
    pieces.append(GamePiece((60, 60), 'red'))
    pieces.append(GamePiece((60, 60), 'yellow'))
    pieces.append(GamePiece((60, 60), 'purple'))
    pieces.append(GamePiece((60, 60), 'blue'))
    pieces.append(GamePiece((60, 60), 'orange'))
    board = GameBoard((600, 600), 'gray')
    for i, p in enumerate(pieces):
        board.add_piece(p, (i%9, i//9))
    game = GameState(board, pieces)
    test_game = GameWindow(game)
    test_game.run()
