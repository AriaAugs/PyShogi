from copy import copy, deepcopy
import pygame

class GameWindow():
    """Window that renders and controls the game.

    Pygame is automatically initialized if needed. No window is opened until
    `GameWindow.run()` is called.

    Args:
        game_state (gui.GameState): The game to display/control

    Attributes:
        game (gui.GameState): Game to render/control
        drag_item (gui.GamePiece): Piece (if any) being dragged by the user
        drag_back (tuple): The dragged piece's original position
        running (bool): Whether or not the game has been closed or otherwise ended
        screen (pygame.Surface): Surface to render the game on
        clock (pygame.time.Clock): Clock to limit framerate
    """

    def __init__(self, game_state):
        # initialize Pygame
        if not pygame.get_init():
            pygame.init()
        # game to display/control
        self.game = game_state
        # item we're dragging and its rollback position
        self.drag_item = None
        self.drag_back = None
        # whether or not to run this game window
        self.running = False
        # these are created once self.run() is called
        self.screen = None
        self.clock = None

    def _resize(self):
        # 11 H x 9 W
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        ideal_width = screen_height #(9 * screen_height) // 11
        ideal_height = screen_width #(11 * screen_width) // 9
        board_width = ideal_width
        board_height = ideal_height
        # check which dimension is the limiting factor
        if screen_height < ideal_height:
            # smught the game width-wise
            #board_width = ideal_width
            board_height = screen_height
        if screen_width < ideal_width:
            # smush the game height-wise
            board_width = screen_width
            #board_height = ideal_height
        # resize the board to take up the full height
        self.game.board.image = pygame.transform.scale(
            self.game.board.image, (board_width, board_height))
        self.game.board.rect = self.game.board.image.get_rect()
        self.game.board.rect.center = (screen_width // 2, screen_height // 2)
        # scale the pieces
        for piece in self.game.pieces:
            p_size = (90 * (board_width // 9)) // 100
            piece.image = pygame.transform.scale(piece.image, (p_size, p_size))
            piece.rect = piece.image.get_rect()
        # tell the board to resize its internal grid and fix the piece placement
        self.game.board.resize()

    def _handle_event(self, event):
        """Handle a given pygame event that has occured in this window

        The events we care about include: closing the window, clicking the mouse buttons,
        and releasing the mouse buttons. Any other events can be ignored.

        Args:
            event (pygame.Event): The event to handle
        """
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.VIDEORESIZE:
            self._resize()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # if the left mouse button was pressed, check if we clicked on a piece
                for piece in self.game.pieces:
                    if piece.rect.collidepoint(event.pos):
                        # we clicked on a piece, start dragging it
                        self.drag_item = piece
                        self.drag_back = piece.rect.center
            if event.button == 3 and self.drag_item is not None:
                # if the right mouse button is pressed and we're dragging something,
                self.drag_item.rect.center = self.drag_back
                self.drag_item = None
        if event.type == pygame.MOUSEBUTTONUP and self.drag_item is not None:
            # if the mouse was released, try snapping the piece to the grid
            pos = self.game.board.on_square(self.drag_item.rect)
            if pos is not None:
                x, y = pos
                if self.game.board.board[x][y] is None:
                    self.game.board.move_piece(self.drag_item, pos)
                #self.game.board.snap_piece(self.drag_item.rect, pos)
            else:
                # the piece is off the grid - roll it back instead
                self.drag_item.rect.center = self.drag_back
            self.drag_item = None
            self.drag_back = None
        if self.drag_item is not None:
            # if we're dragging something, center it on the mouse
            self.drag_item.rect.center = pygame.mouse.get_pos()

    def render(self):
        """Update the display to render the game on screen"""
        # clear the screen, draw the board, draw the pieces, then flip the display
        self.screen.fill("black")
        self.game.board_group.draw(self.screen)
        self.game.pieces_group.draw(self.screen)
        pygame.display.flip()

    def run(self):
        """Run the game"""
        # initialize display stuff
        self.screen = pygame.display.set_mode((720, 720), pygame.SHOWN | pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        # set everything on the display to the correct size
        self._resize()
        # main game loop
        self.running = True
        while self.running:
            # handle all the game events
            for event in pygame.event.get():
                self._handle_event(event)
            # render the game
            self.render()
            # limit the FPS to 60
            self.clock.tick(60)
        # no need to do pygame.quit() - pygame is
        # uninitialized automatically when the
        # Python interpreter shuts down. We don't
        # want to uninitialize pygame while it's
        # still needed

class GameState():
    """State of the game, including board and all pieces

    TODO: Remove this class from the GUI module

    Args:
        board_in (gui.GameBoard): The game board
        pieces_in (list of gui.GamePiece): All the pieces in the game

    Attributes:
        game (gui.GameState): Game to render/control
        board_group (pygame.sprite.Group): sprite group for the board
        pieces_group (pygame.sprite.Group): sprite group for the pieces
        board (gui.GameBoard): the game board
        pieces (list of gui.GamePiece): the pieces in the game
    """

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
    """The game board

    TODO: Remove this class from the GUI module

    Args:
        board_size (2-element tuple): initial size of the board
        color (string): color to draw the board

    Attributes:
        image (pygame.Surface): board's sprite
        rect (pygame.Rect): bounding rect of the board's sprite
        board (2D list): conceptual representation of the board spaces
        held_white (list): pieces captured by white but not placed yet
        held_black (list): pieces captured by black but not placed yet
        grid (dict): map of board positions to screen coordinates
    """

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
        self.gen_grid_points()

    def on_square(self, rect):
        """Check if a given rect is touching the center of a grid space

        Args:
            rect (pygame.Rect): the rect to check

        Returns:
            tuple: the grid location the rect is on
            None: returns None if the rect isn't on any grid cell
        """
        # check to see if a rect is on a grid cell
        # this is done by checking if the rect collides with the center of the grid cell
        for key, pos in self.grid.items():
            if rect.collidepoint(pos):
                return key
        return None

    def snap_piece(self, rect, pos):
        """Moves a given rect to the screen position associated with a given board position

        Args:
            rect (pygame.Rect): the bounding rect to move
            pos (tuple): the board position to move the rect to
        """
        # set a piece's position such that it is centered within a given grid cell
        x, y = pos
        rect.center = self.grid[(x, y)]

    def move_piece(self, piece, pos):
        """Move a piece to a new board position

        Args:
            piece (gui.GamePiece): the piece to move
            pos (tuple): board position to move the piece to
        """
        # clear the old pos
        for x, col in enumerate(self.board):
            for y, cell in enumerate(col):
                if cell is piece:
                    cell = None
        # set the new pos
        self.add_piece(piece, pos)

    def add_piece(self, piece, pos):
        """Place a piece on the board

        Args:
            piece (gui.GamePiece): the piece to place
            pos (tuple): board position to place the piece at
        """
        # add a piece to the board and set its position
        x, y = pos
        self.board[x][y] = piece
        self.snap_piece(piece.rect, pos)

    def gen_grid_points(self):
        """Generate the mapping of board positions to screen positions"""
        grid_width = self.rect.width // 9
        grid_height = self.rect.height // 9
        x_offset = self.rect.x
        y_offset = self.rect.y
        grid_rect = pygame.Rect(0, 0, grid_width, grid_height)
        for x in range(9):
            for y in range(9):
                grid_rect.topleft = ((x*grid_width)+x_offset, (y*grid_height)+y_offset)
                self.grid[(x, y)] = grid_rect.center

    def resize(self):
        """Resize the board and move all the pieces accordingly"""
        self.gen_grid_points()
        # move all the pieces to the right locations
        for x in range(9):
            for y in range(9):
                piece = self.board[x][y]
                if isinstance(piece, GamePiece):
                    self.snap_piece(piece.rect, (x, y))

class GamePiece(pygame.sprite.Sprite):
    """Pieces used in the game

    TODO: Remove this class from the GUI module

    Args:
        piece_size (2-element tuple): initial size of the piece
        color (string): color to draw the piece

    Attributes:
        image (pygame.Surface): piece's sprite
        rect (pygame.Rect): bounding rect of the piece's sprite
    """

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
