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
        # Keep track of the kings. 0-index is white king, 1-index is black king
        self.kings = []
        self._add_pieces('white')
        self._add_pieces('black')
        self.last_pawn_move = None
        
    def getKingPositions(self): 
        return [[self.kings[0].x, self.kings[0].y], [self.kings[1].x, self.kings[1].y]]
    
    def move(self, piece, move):
        print(f"Attempting to move {piece.name} from {move.initial.row},{move.initial.col} to {move.final.row},{move.final.col}")
        initial = move.initial
        final = move.final 
        
        # Handle en-passant FIRST, before any other moves
        if isinstance(piece, Pawn):
            if move.is_enpassant:
                print(f"En passant capture detected!")
                print(f"Initial row {move.initial.row} and initial col {move.initial.col}, final row {move.final.row} and col {move.final.col} of move ")
                # Clear the captured pawn's square
                print(f"Last pawn move: {self.last_pawn_move.initial.row, self.last_pawn_move.initial.col, self.last_pawn_move.final.row, self.last_pawn_move.final.col}")
                print(f"Last general move: {self.last_move}")
                self.squares[initial.row][final.col].piece = None
                print(f"Square cleared: {self.squares[initial.row][final.col].piece}")
                print(self.squares[initial.row][final.col])
        
        # console board move update 
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        piece.moved = True
        
        # Check for adjacent kings if this is a king move
        if isinstance(piece, King):
            # Possible adjacent squares relative to the final position
            adjacent_squares = [
                (final.row-1, final.col-1), (final.row-1, final.col), (final.row-1, final.col+1),
                (final.row, final.col-1),                              (final.row, final.col+1),
                (final.row+1, final.col-1), (final.row+1, final.col), (final.row+1, final.col+1)
            ]
            
            # Check each adjacent square for enemy king
            for row, col in adjacent_squares:
                if Square.in_range(row, col):  # Make sure square is on board
                    square = self.squares[row][col]
                    if square.has_piece() and isinstance(square.piece, King) and square.piece.color != piece.color:
                        print("Invalid move: Kings cannot be adjacent")
                        return False
        
        
            
        print(f"Move completed for {piece.name}")
        
        # pawn promotion
        if piece.name == 'pawn':
            self.check_promotion(piece, final)
            self.moved = True
        
        if type(piece) == King:
            # castling
            if self.castling(initial, final):
                if final.col > initial.col:  # king-side castling
                    rook_initial = Square(initial.row, 7)
                    rook_final = Square(initial.row, 5)
                    
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
        
        
        # move 
        if type(piece) == Pawn:
            piece.moved = True
            self.last_pawn_move = move
        else:
            self.last_pawn_move = None
        
        piece.moved = True
        
        # clear valid moves
        piece.clear_moves()
        self.last_move = move
        
    
    def valid_move(self, piece, move):
        print(f"Checking if move is valid for {piece.name}")
        print(f"Available moves: {len(piece.moves)}")
        return move in piece.moves
    
    def check_promotion(self, piece, final):
        '''
            Checks if the piece is eligible for promotion
            Later need to implement optional promotion to different pieces 
        '''
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)
    
    def castling(self, initial, final):
        '''
        Checks if the castling move is theoretically possible
        Returns False if:
        It's not a castling move (king doesn't move 2 squares)
        '''
        return abs(initial.col - final.col) == 2
    
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
    
    def is_enpassant_possible(self):
        '''Check if en passant is possible based on the last move, which must be a pawn move for two squares
           Does not guarantee that en passant can be performed, as the current pawn must also be adjacent to the last_pawn_move
        '''
        if not self.last_pawn_move:
            return False
            
        piece = self.squares[self.last_pawn_move.final.row][self.last_pawn_move.final.col].piece
        
        # Check if last move was a pawn moving two squares
        if isinstance(piece, Pawn):
            return abs(self.last_pawn_move.final.row - self.last_pawn_move.initial.row) == 2
            
        return False
    
    def is_stalemate(self, king):
        '''
            Returns True if there is a stalemate, False if otherwise
            Conditions for stalemate
            1. King is not in check
            2. No legal moves for any piece of the same color
        '''
        if king.in_check:
            return False
        
        # Check for any legal moves for all pieces of the same color
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_team_piece(king.color):
                    piece = self.squares[row][col].piece
                    # Calculate legal moves for this piece
                    self.calc_moves(piece, row, col, bool=True)
                    # If any piece has legal moves, it's not checkmate
                    if piece.moves:
                        return False

        return True
    
    def is_checkmate(self, king):
        '''
            Returns True if there is a checkmate, False if otherwise
            Conditions for checkmate:
            1. King is in check
            2. No legal moves for any piece of the same color
        '''
        if not king.in_check:
            return False
        
        # Check for any legal moves for all pieces of the same color
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_team_piece(king.color):
                    piece = self.squares[row][col].piece
                    # Calculate legal moves for this piece
                    self.calc_moves(piece, row, col, bool=True)
                    # If any piece has legal moves, it's not checkmate
                    if piece.moves:
                        return False

        # If we get here, king is in check and no pieces have legal moves
        king.checkmated = True
        return True

        
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
        king = King(color, row_other, 4)
        self.squares[row_other][4] = Square(row_other, 4, king)
        king.left_rook, king.right_rook = self.squares[row_other][0].piece, self.squares[row_other][7].piece
        self.kings.append(king)
        print(self.kings[-1].x, self.kings[-1].y)
        

    def calc_moves(self, piece, row, col, bool=True):
        print(f"Board: Calculating moves for {piece.name} at {row},{col}")  # Debug print
        
        # Create calc moves instance
        calc = Calc_Moves(self)
        
        # Calculate all possible moves for the specific piece
        calc.calc_moves(piece, row, col, bool)
        
        print(f"Board: Found {len(piece.moves)} moves")  # Debug print
    
    