from const import *
from square import Square
from piece import *
from move import Move
import copy
from calc_moves import *

class Board:
    
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
    
    def move(self, piece, move):
        print(f"Attempting to move {piece.name} from {move.initial.row},{move.initial.col} to {move.final.row},{move.final.col}")
        
        initial = move.initial
        final = move.final 
        
        # console board move update 
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        
        print(f"Move completed for {piece.name}")
        
        # pawn promotion
        if piece.name == 'pawn':
            self.check_promotion(piece, final)
        
        
        if type(piece) == King:
            # castling
            if self.castling(initial, final):
                if final.col > initial.col:  # king-side castling
                    rook_initial = Square(initial.row, 7)
                    rook_final = Square(initial.row, 5)
                    #NEED TO CHECK IF THE SQUARES IN-BTWN ARE BEING ATTACKED
                
                else:  # queen-side castling
                    rook_initial = Square(initial.row, 0)
                    rook_final = Square(initial.row, 3)
            
                rook = self.squares[rook_initial.row][rook_initial.col].piece
                self.squares[rook_initial.row][rook_initial.col].piece = None
                self.squares[rook_final.row][rook_final.col].piece = rook
                rook.moved = True
            
            else:
                piece.x = final.col
                piece.y = final.row
            piece.moved = True
        
        
        # move 
        if type(piece) == Pawn:
            piece.moved = True
        
        piece.moved = True
        
        # clear valid moves
        piece.clear_moves()
        self.last_move = move
        
    
    def valid_move(self, piece, move):
        print(f"Checking if move is valid for {piece.name}")
        print(f"Available moves: {len(piece.moves)}")
        is_valid = move in piece.moves
        print(f"Move is {'valid' if is_valid else 'invalid'}")
        return is_valid
    
    def check_promotion(self, piece, final):
        '''
            Checks if the piece is eligible for promotion
            Later implement optional promotion to different pieces 
        '''
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)
    
    def castling(self, initial, final):
        '''
            Checks if the castling move is possible, but not necessarily checking if it's valid
        '''
        return abs(initial.col - final.col) == 2
    
    def illegal(self, piece, move, ignore = True):
        '''
            Returns whether a move is illegal, False is not illegal
            1) THe king is already in check
            2) The piece is pinned, and moving it puts the king in check
        '''
        return self.pinned(piece, move)
            
    
    def pinned(self, piece, move): 
        '''
            Is the king in check after proposed move? 
            Do not allow "pinned" pieces to move
            False means not pinned, True means pinned
        '''        
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)
        for row in range(ROWS): 
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool = False)
                    for m in p.moves:                        
                        if type(m.final.piece) == King:
                            return True
        return False
    
    def is_king_in_check(self, king):
        '''
            Checks if the king is under attack, and returns the position of the pieces attacking it
        '''
        attacking = []
        # Check if any enemy piece can attack the king
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if piece and piece.color != king.color:  # if it's an enemy piece
                    self.calc_moves(piece, row, col, bool=False)  # calculate its moves
                    for move in piece.moves:
                        if type(move.final.piece) == King:
                            attacking.append([row, col])
        if attacking:
            king.in_check = True
        else:
            king.in_check = False
        return attacking    
        
    def _create(self):
        '''
            Creates the board
        '''        
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
        
    def _add_pieces(self, color):        
        '''
            Adds pieces to the board
        '''
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)
        
        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
            
        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
        
        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
        
        #rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))
        
        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        
        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color, row_other, 4))
        

    def calc_moves(self, piece, row, col, bool=True):
        print(f"Board: Calculating moves for {piece.name} at {row},{col}")  # Debug print
        
        # Create calc moves instance
        calc = Calc_Moves(self)
        
        # Calculate all possible moves for the specific piece
        calc.calc_moves(piece, row, col, bool)
        
        print(f"Board: Found {len(piece.moves)} moves")  # Debug print
    
    