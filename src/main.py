import pygame
import sys
import os

from const import *
from game import Game
from square import Square
from move import Move

# Move up one directory to project root
os.chdir(os.path.dirname(os.path.dirname(__file__)))

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
    
    def mainloop(self):
        dragger = self.game.dragger
        game = self.game
        screen = self.screen
        board = self.game.board
        
        while True:
            #show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            
            game.show_hover(screen)
            
            if dragger.dragging:
                dragger.update_blit(screen)
            
            for event in pygame.event.get():
                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE
                    
                    try:
                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                            print(f"Selected {piece.name} at {clicked_row},{clicked_col}")
                            # valid piece color? 
                            if piece.color == game.next_player:                           
                                board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                print(f"Calculated moves: {len(piece.moves)}")
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)
                                # show methods
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)
                    except Exception:
                        pass
                        
                # dragging
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    
                    game.set_hover(motion_row, motion_col)
                    
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        #show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                
                # release click
                elif event.type == pygame.MOUSEBUTTONUP:
                    try:
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            released_row = dragger.mouseY //SQSIZE
                            released_col = dragger.mouseX // SQSIZE
                            
                            # create possible move 
                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            
                            move = Move(initial, final)
                            
                            # if valid move
                            if board.valid_move(dragger.piece, move):
                                captured = board.squares[released_row][released_col].has_piece()
                                board.move(dragger.piece, move)
                                
                                # play sound
                                game.play_sound(captured)
                                
                                # show method
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_pieces(screen)
                                
                                #next turn
                                game.next_turn()
                            
                        dragger.undrag_piece()
                    
                    except Exception:
                        pass
                    
                # key press
                elif event.type == pygame.KEYDOWN:
                    
                    # changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()
                        
                    # changing sounds
                    elif event.key == pygame.K_s:
                        game.change_sound()
                        
                    # restart
                    elif event.key == pygame.K_r:
                        game.reset()
                        dragger = self.game.dragger
                        game = self.game
                        board = self.game.board
                
                # quit game 
                elif event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
    
main = Main()
main.mainloop()