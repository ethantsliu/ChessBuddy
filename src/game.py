import pygame
from const import * 
from board import Board
from dragger import Dragger
from config import Config
from square import Square
from ai import ChessAI

class Game:
    
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        self.next_player = 'white'
        self.hovered_sqr = None
        self.config = Config()
        self.ai = ChessAI(k=5)
    
    # Show methods
    
    def show_bg(self, surface):
        theme = self.config.theme
        
        for row in range(ROWS):
            for col in range(COLS):
                #color
                color = theme.bg.light if (row+col) % 2 == 0 else theme.bg.dark
                #rect 
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                #blit
                pygame.draw.rect(surface, color, rect)
                
                # row coordinates
                if col == 0: 
                    # color
                    color = theme.bg.dark if row%2 == 0 else theme.bg.light
                    
                    # label
                    lbl = self.config.font.render(str(ROWS - row), 1, color)
                    lbl_pos = (5, 5 + row * SQSIZE)
                    
                    # blit
                    surface.blit(lbl, lbl_pos)
                    
                if row == 7: 
                    # color
                    color = theme.bg.dark if (row + col)%2 == 0 else theme.bg.light
                    
                    # label
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    
                    # blit
                    surface.blit(lbl, lbl_pos)
    
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece?
                if self.board.squares[row][col].has_piece(): 
                    piece = self.board.squares[row][col].piece
                    # all pieces except dragger piece 
                    if piece is not self.dragger.piece:         
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center = img_center)
                        surface.blit(img, piece.texture_rect)
    
    def show_moves(self, surface):
        theme = self.config.theme
        if self.dragger.dragging:
            piece = self.dragger.piece
            print(f"Showing moves for {piece.name}: {len(piece.moves)} moves")
            
            # loop all valid or possible moves
            for move in piece.moves:
                # color
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                # rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                # blit 
                pygame.draw.rect(surface, color, rect)
                
    def show_last_move(self, surface):
        theme = self.config.theme
        
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            
            for pos in [initial, final]:
                # color
                color = theme.trace.light if (pos.row + pos.col)%2 == 0 else theme.trace.dark
                # rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)
    
    def show_hover(self, surface):
        if self.hovered_sqr:
            #color 
            color = (180, 180, 180)
            #rect
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            #blit
            pygame.draw.rect(surface, color, rect, width = 3)
            
    
    # other methods

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'
        
        if self.next_player == 'black':
            self.make_ai_move()
        
    def make_ai_move(self):
        ai_move = self.ai.get_best_move(self.board)
        
        if ai_move:
            piece = self.board.squares[ai_move.initial.row][ai_move.initial.col].piece
            
            captured = self.board.squares[ai_move.final.row][ai_move.final.col].has_piece()
            self.board.move(piece, ai_move)
            
            self.play_sound(captured)
            
            self.next_turn()
        
    def set_hover(self, row, col):
        try:
            self.hovered_sqr = self.board.squares[row][col]
        except Exception: pass
        
    def change_theme(self):
        self.config.change_theme()
        
    def change_sound(self):
        self.config.change_sound()
        
    def play_sound(self, captured = False):
        if captured: 
            self.config.capture_sound.play()
        
        else: self.config.move_sound.play()
    
    def play_checkmate(self):
        self.config.checkmate.play()
        
    def play_stalemate(self):
        self.config.checkmate.play()
    
    def play_check(self):
        self.config.check.play()
    
    def play_castle(self):
        self.config.castling.play()
        
    def reset(self):
        self.__init__()
        