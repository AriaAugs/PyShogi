import constants


diagonal_moves = [(y * x, z * x) for x in range(1, 9) for y in [1, -1] for z in [-1, 1]]
gold_moves = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (0, -1)]


class piece():
    def __init__(self):
        self.moveset = None
        self.promoted = False
        self.owner = None
        self.image = None
    
    def capture(self):
        self.promoted = False
        if self.owner == constants.player1:
            self.owner = constants.player2
        else:
            self.owner = constants.player1
    
    def promote(self):
        self.promoted = True

    def get_moves(self):
        return self.moveset[(self.type, self.promoted)]
    
class pawn(piece):
    def __init__(self):
        super.__init__()
        self.moveset[False] = [(0, 1)]
        self.moveset[True] = gold_moves
        self.image