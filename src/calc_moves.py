from square import Square
from move import Move
from piece import *

class Calc_Moves:
    def __init__(self, board):
        self.board = board
        self.squares = board.squares

    def calc_moves(self, piece, row, col, bool = True):
        '''
            Calculates all possible or valid moves for a piece on a square
        '''
        # Clear existing moves before calculating new ones
        piece.clear_moves()
        
        print(f"Calculating moves for {piece.name} at {row},{col}")
        
        def pawn_moves():
            steps = 1 if piece.moved else 2
            
            #vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1+steps))
            for legal_move_row in range(start, end, piece.dir):
                if Square.in_range(legal_move_row):
                    if self.squares[legal_move_row][col].isempty():
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(legal_move_row, col)
                        # create a new move
                        move = Move(initial, final)
                        
                        if bool:
                            # check if the move is pinned
                            if not self.board.pinned(piece, move):                        
                                # append new move
                                piece.add_move(move)     
                        else: 
                            piece.add_move(move)
                            
                    else: break
                else: break
            
            # diagonal moves    
            legal_move_row = row + piece.dir
            legal_move_cols = [col-1, col+1]
            for legal_move_col in legal_move_cols:
                if Square.in_range(legal_move_row, legal_move_col):
                    if self.squares[legal_move_row][legal_move_col].has_enemy_piece(piece.color):
                        # create initial and final move squares
                        initial = Square(row, col)
                        final_piece = self.squares[legal_move_row][legal_move_col].piece
                        final = Square(legal_move_row, legal_move_col, final_piece)
                        # create a new move
                        move = Move(initial, final)
                        
                        if bool:
                            # check if the move is pinned
                            if not self.board.pinned(piece, move):                        
                                # append new move
                                piece.add_move(move)     
                        else: 
                            piece.add_move(move)
                        
            # en passant moves
            if self.board.is_enpassant_possible():
                last_move = self.board.last_pawn_move # Must be a last_pawn_move if self.board.is_enpassant_possible
                if row == last_move.final.row:  # Same rank
                    if abs(col - last_move.final.col) == 1:  # Adjacent column, guarantees en passant can be performed
                        # Create en passant move
                        initial = Square(row, col)
                        final = Square(row + piece.dir, last_move.final.col)
                        # Add captured piece info to the move
                        move = Move(initial, final, is_enpassant = True) # If played, this would be an en passant 
                        
                        if bool:
                            if not self.board.pinned(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                            

        
        def knight_moves():
            possible_moves = [
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1),
            ]

            for possible_move in possible_moves:
                legal_move_x, legal_move_y = possible_move
                
                if Square.in_range(legal_move_x, legal_move_y):
                    if self.squares[legal_move_x][legal_move_y].isempty_or_enemy(piece.color):
                        #create squares of new move
                        initial = Square(row, col)
                        final_piece = self.squares[legal_move_x][legal_move_y].piece
                        final = Square(legal_move_x, legal_move_y, final_piece)

                        #create new move
                        move = Move(initial, final)
                        
                        if bool:
                            # check if the move is pinned
                            if not self.board.pinned(piece, move):                        
                                # append new move
                                piece.add_move(move)
                                 
                        else: 
                            piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                legal_move_row = row + row_incr 
                legal_move_col = col + col_incr
                
                while True:
                    if Square.in_range(legal_move_row, legal_move_col):
                        #create squares of the possible new move
                        initial = Square(row, col)
                        final_piece = self.squares[legal_move_row][legal_move_col].piece
                        final = Square(legal_move_row, legal_move_col, final_piece)
                        
                        #create a possible new move 
                        move = Move(initial, final)
                        
                        # empty
                        if self.squares[legal_move_row][legal_move_col].isempty():
                            if bool:
                            # check if the move is pinned
                                if not self.board.pinned(piece, move):                        
                                    # append new move
                                    piece.add_move(move)     
                            else: 
                                piece.add_move(move)
                        
                        # has enemy piece
                        elif self.squares[legal_move_row][legal_move_col].has_enemy_piece(piece.color):
                            if bool:
                            # check if the move is pinned
                                if not self.board.pinned(piece, move):                        
                                    # append new move
                                    piece.add_move(move)     
                            else: 
                                piece.add_move(move)
                            break
                        
                        #has team piece
                        elif self.squares[legal_move_row][legal_move_col].has_team_piece(piece.color):
                            break
                     
                    else: break
                        
                    # incrementing the increments 
                    legal_move_row, legal_move_col = legal_move_row + row_incr, legal_move_col + col_incr
        
        def king_moves():
            adjs = [
                (row-1, col+0),
                (row+1, col+0),
                (row-1, col+1),
                (row-1, col-1),
                (row+1, col+1),
                (row+0, col+1),
                (row+0, col-1),
                (row+1, col-1),
            ]
            
            for possible_move in adjs:
                legal_move_x, legal_move_y = possible_move
                
                if Square.in_range(legal_move_x, legal_move_y):
                    if self.squares[legal_move_x][legal_move_y].isempty_or_enemy(piece.color):
                        # Check for adjacent enemy king
                        adjacent_squares = [
                            (legal_move_x-1, legal_move_y-1), (legal_move_x-1, legal_move_y), (legal_move_x-1, legal_move_y+1),
                            (legal_move_x, legal_move_y-1),                                    (legal_move_x, legal_move_y+1),
                            (legal_move_x+1, legal_move_y-1), (legal_move_x+1, legal_move_y), (legal_move_x+1, legal_move_y+1)
                        ]
                        
                        king_adjacent = False
                        for adj_row, adj_col in adjacent_squares:
                            if Square.in_range(adj_row, adj_col):
                                adj_square = self.squares[adj_row][adj_col]
                                if (adj_square.has_piece() and 
                                    isinstance(adj_square.piece, King) and 
                                    adj_square.piece.color != piece.color):
                                    king_adjacent = True
                                    break
                        
                        if not king_adjacent:
                            initial = Square(row, col)
                            final = Square(legal_move_x, legal_move_y)
                            move = Move(initial, final)
                            
                            if bool:
                                # check if king is in check
                                if self.board.is_king_in_check(piece):             
                                    piece.in_check = True        
                                    
                                if not self.board.pinned(piece, move):
                                    piece.add_move(move)   
                            else: 
                                piece.add_move(move)
                 
            #castling moves
            if not piece.moved:
                # king-side castling
                right_rook = self.squares[row][7].piece
                if type(right_rook) == Rook and not right_rook.moved:
                    if all(self.squares[row][c].isempty() for c in range(5, 7)):
                        # adds right rook to king
                        piece.right_rook = right_rook
                        
                        # king move
                        initial = Square(row, col)
                        final = Square(row, col+2)
                        moveK = Move(initial, final)
                        
                        # rook move
                        initial = Square(row, 7)
                        final = Square (row, 5)
                        moveR = Move(initial, final)
                        
                        
                        if bool:
                            # check if the move is pinned
                            if not self.board.pinned(piece, moveK) and not self.board.pinned(right_rook, moveR):                        
                                # append new move to rook
                                right_rook.add_move(moveR)
                                
                                # append new move to king 
                                piece.add_move(moveK)     
                        else: 
                            piece.add_move(moveK)
                            right_rook.add_move(moveR)
                
                # queen-side castling
                left_rook = self.squares[row][0].piece
                if type(left_rook) == Rook and not left_rook.moved:
                    if all(self.squares[row][c].isempty() for c in range(1 ,4)):
                        # adds left rook to king
                        piece.left_rook = left_rook
                        
                        # king move
                        initial = Square(row, col)
                        final = Square(row, col-2)
                        moveK = Move(initial, final)
                        
                        # rook move
                        initial = Square(row, 0)
                        final = Square (row, 3)
                        moveR = Move(initial, final)

                        if bool:
                            # check if the move is pinned
                            if not self.board.pinned(piece, moveK) and not self.board.pinned(left_rook, moveR):                        
                                # append new move to rook
                                left_rook.add_move(moveR)
                                
                                # append new move to king 
                                piece.add_move(moveK)     
                        else: 
                            piece.add_move(moveK)
                            left_rook.add_move(moveR)
                            

        if piece.name == 'pawn': pawn_moves()
        elif piece.name == 'knight': knight_moves()
        elif piece.name == 'bishop': 
            straightline_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1),
            ])
        elif piece.name == 'rook' : 
            straightline_moves([
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
            ])
        elif piece.name == 'queen': 
            straightline_moves([
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1),
            ])
        else: king_moves()
        
        print(f"Found {len(piece.moves)} moves for {piece.name}")