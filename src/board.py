from const import *
from square import Square
from piece import *
from move import Move
import copy

class Board:
    
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
    
    def move(self, piece, move):
        initial = move.initial
        final = move.final 
        
        # console board move update 
        self.squares[initial.row][initial.col].piece = None
        
        self.squares[final.row][final.col].piece = piece
        
        # pawn promotion
        if piece.name == 'pawn':
            self.check_promotion(piece, final)
        
        # castling
        if isinstance(piece, King) and self.castling(initial, final):
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
                
        # move 
        piece.moved = True
        
        # clear valid moves
        piece.clear_moves()
        
        self.last_move = move
        
    
    def valid_move(self, piece, move):
        return move in piece.moves
    
    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)
    
    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2
    
    def illegal(self, piece, move): 
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)
        
        # Is the king currently in check? 
        # in_check = False
        # for row in range(ROWS):
        #     for col in range(COLS):
        #         if self.squares[row][col].has_enemy_piece(piece.color):
        #             enemy_piece = self.squares[row][col].piece
        #             self.calc_moves(enemy_piece, row, col, bool=False)
        #             for enemy_move in enemy_piece.moves:
        #                 if isinstance(enemy_move.final.piece, King):
        #                     in_check = True
        
        # Is the king in check after proposed move? 
        for row in range(ROWS): 
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool = False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False
    
    def calc_moves(self, piece, row, col, bool = True):
        '''
            Calculates all possible or valid moves for a piece on a square
        '''
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
                            # check if the move is illegal
                            if not self.illegal(piece, move):                        
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
                            # check if the move is illegal
                            if not self.illegal(piece, move):                        
                                # append new move
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
                            # check if the move is illegal
                            if not self.illegal(piece, move):                        
                                # append new move
                                piece.add_move(move)
                            else: break
                                 
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
                            # check if the move is illegal
                                if not self.illegal(piece, move):                        
                                    # append new move
                                    piece.add_move(move)     
                            else: 
                                piece.add_move(move)
                        
                        # has enemy piece
                        elif self.squares[legal_move_row][legal_move_col].has_enemy_piece(piece.color):
                            if bool:
                            # check if the move is illegal
                                if not self.illegal(piece, move):                        
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
                (row-1, col+0),
                (row+0, col+1),
                (row+0, col-1),
                (row+1, col-1),
            ]
            
            for possible_move in adjs:
                legal_move_x, legal_move_y = possible_move
                
                if Square.in_range(legal_move_x, legal_move_y):
                    if self.squares[legal_move_x][legal_move_y].isempty_or_enemy(piece.color):
                        #create squares of new move
                        initial = Square(row, col)
                        final = Square(legal_move_x, legal_move_y)

                        #create new move
                        move = Move(initial, final)
                        if bool:
                            # check if the move is illegal
                            if not self.illegal(piece, move):                        
                                # append new move
                                piece.add_move(move)    
                            else: break 
                        else: 
                            piece.add_move(move)
                 
            #castling moves
            if not piece.moved:
                
                # king-side castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook) and not right_rook.moved:
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
                            # check if the move is illegal
                            if not self.illegal(piece, moveK) and not self.illegal(right_rook, moveR):                        
                                # append new move to rook
                                right_rook.add_move(moveR)
                                
                                # append new move to king 
                                piece.add_move(moveK)     
                        else: 
                            piece.add_move(moveK)
                            right_rook.add_move(moveR)
                
                # queen-side castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook) and not left_rook.moved:
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
                            # check if the move is illegal
                            if not self.illegal(piece, moveK) and not self.illegal(left_rook, moveR):                        
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
        
    def _create(self):        
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
        
    def _add_pieces(self, color):        
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
        self.squares[row_other][4] = Square(row_other, 4, King(color))