import constants

import pygame

diagonal_moves = [(y * x, z * x) for x in range(1, 9) for y in [1, -1] for z in [-1, 1]]
gold_moves = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (0, -1)]


class piece():
    def __init__(self, moveset):
        self._moveset = moveset
        self.promoted = False
        self.owner = None
        self.image = None
        self.rect = pygame.rect
        self.sprite = pygame.sprite.Sprite
        self.game = None
    
    def capture(self):
        self.promoted = False
        if self.owner == constants.player1:
            self.owner = constants.player2
        else:
            self.owner = constants.player1
    
    def promote(self):
        self.promoted = True

    # getting the values
    @property
    def moveset(self):
        return self._moveset

    # setting the values
    @moveset.setter
    def moveset(self, moveset):
        self._moveset = moveset

    # deleting the values
    @moveset.deleter
    def moveset(self):
        del self._moveset

    
class pawn(piece):
    def __init__(self, moveset):
        super.__init__()

