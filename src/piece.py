import os

class Piece:
    
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.set_texture()
        self.texture_rect = texture_rect
        
    def set_texture(self, size=80):
        self.texture = os.path.join(
            f'assets/images/imgs-{size}px/{self.color}_{self.name}.png'
        )
    
    def add_move(self, move):
        self.moves.append(move)
        
    def clear_moves(self):
        self.moves = []
        
class Pawn(Piece):
    
    def __init__(self, color):
        #With color, we know which direction pawn can move
        super().__init__('pawn', color, value = 1.0)
        self.protected = False # if the piece is protected by another piece, for all except king
        self.dir = -1 if color == 'white' else 1 #Pygame module has increasing y-axis toward bottom

class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color, value = 3.0)
        self.protected = False # if the piece is protected by another piece, for all except king
        
class Bishop(Piece):
    
    def __init__(self, color):
        super().__init__('bishop', color, value = 3.0)
        self.protected = False # if the piece is protected by another piece, for all except king

class Rook(Piece):
    
    def __init__(self, color):
        super().__init__('rook', color, value = 5.0)
        self.protected = False # if the piece is protected by another piece, for all except king
        
class Queen(Piece):
    
    def __init__(self, color):
        super().__init__('queen', color, value = 9.0)
        self.protected = False # if the piece is protected by another piece, for all except king
        
class King(Piece):
    def __init__(self, color, xPos, yPos):
        self.left_rook = None
        self.right_rook = None
        self.x = xPos
        self.y = yPos
        self.in_check = False # whether the king is in check
        self.moved = False # whether the king has moved, for the purposes of castling
        self.checkmated = False # whether the king has been checkmated
        super().__init__('king', color, value = 1000000.0)

        
        
        

        
    