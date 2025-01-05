import pygame
import sys
import os

from const import *
from game import Game
from square import Square
from move import Move

# Move up one directory to project root
os.chdir(os.path.dirname(os.path.dirname(__file__)))

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
        # Add font initialization
        self.font = pygame.font.SysFont('Arial', 32)
        # (7, 4) -> (1, e) -> e1 white king
        
    def show_checkmate(self, screen, winner):
        '''
        Displays the checkmate message
        '''
        # Create semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Create text
        text = self.font.render(f'Checkmate! {winner} wins!', True, WHITE)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        
        # Draw text
        screen.blit(text, text_rect)
        pygame.display.update()
        
    def show_stalemate (self, screen):
        '''
        Displays the checkmate message
        '''
        # Create semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Create text
        text = self.font.render(f'Stalemate!', True, WHITE)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        
        # Draw text
        screen.blit(text, text_rect)
        pygame.display.update()
        
    def display_text(self, text, x, y, font, color):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
        
    def main_menu(self):
        title = "ChessBuddy"
        title_font = pygame.font.SysFont('Arial', 70)
        subtitle_font = pygame.font.SysFont('Arial', 40)
        
        menu_options = ["New Game (N)", 
                        "Load Last Game (L)", 
                        "Quit Game (Q)", 
                        "During the game:", 
                        "Reset (R)", 
                        "Change Sound (C)", 
                        "Save Game (S)", 
                        "Quit Game (Q)"]

        while True:
            self.screen.fill(BLACK)
            self.display_text(title, WIDTH / 2, HEIGHT / 8, title_font, WHITE)
            # Draw menu options
            for i, option in enumerate(menu_options[:3]):
                color = WHITE 
                self.display_text(option, WIDTH / 2, HEIGHT / 4 + (i * 50) + 30, self.font, color)
            
            self.display_text(menu_options[3], WIDTH / 2, HEIGHT / 4 + 50 + 170, subtitle_font, color)
            
            for i, option in enumerate(menu_options[4:]):
                color = WHITE 
                self.display_text(option, WIDTH / 2, HEIGHT / 4 + (i * 50) + 290, self.font, color)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Handle key press
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        self.start_new_game()
                        return 
                    elif event.key == pygame.K_l:
                        self.load_game()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                        
    def mainloop(self):
        while True:
            self.main_menu()
            dragger = self.game.dragger
            game = self.game
            screen = self.screen
            board = self.game.board
            game_over = False
            
            while not game_over:
                opponent_king = board.kings[1] if game.next_player == 'white' else board.kings[0]
                
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
                                    
                        except Exception:
                            pass
                            
                    # dragging
                    elif event.type == pygame.MOUSEMOTION:
                        motion_row = event.pos[1] // SQSIZE
                        motion_col = event.pos[0] // SQSIZE
                        game.set_hover(motion_row, motion_col)
                        
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                    
                    # release click
                    elif event.type == pygame.MOUSEBUTTONUP:
                        try:
                            if dragger.dragging:
                                dragger.update_mouse(event.pos)
                                released_row = dragger.mouseY //SQSIZE
                                released_col = dragger.mouseX // SQSIZE
                                
                                piece = dragger.piece
                                dragger.undrag_piece()
                                
                                board.calc_moves(piece, dragger.initial_row, dragger.initial_col)
                                
                                move = None
                                for mov in piece.moves:
                                    if mov.final.row == released_row and mov.final.col == released_col:
                                        move = mov
                                        break
                                # if valid move
                                if board.valid_move(piece, move):
                                    check = False
                                    
                                    print(f"Is move an en passant? {move.is_enpassant}")
                                    if move.is_enpassant:
                                        captured = True
                                        move.is_enpassant = True 
                                    else: 
                                        captured = board.squares[released_row][released_col].has_piece()
                                    
                                    board.move(piece, move)
                                    game.show_bg(screen)
                                    game.show_last_move(screen)
                                    game.show_moves(screen)
                                    game.show_pieces(screen)
                                    game.show_hover(screen)
                                    pygame.display.update()
                                    
                                    if piece.color == 'white':
                                        opponent_king = board.kings[1]
                                    else: 
                                        opponent_king = board.kings[0]
                                    if board.is_king_in_check(opponent_king):
                                        check = True
                                        if board.is_checkmate(opponent_king):
                                            game_over = True
                                            pygame.time.wait(200)
                                            self.show_checkmate(screen, piece.color.capitalize())
                                            game.play_checkmate()
                                            pygame.display.update()
                                            pygame.time.wait(3000)
                                            # Exit to main menu
                                            break
                                        else:
                                            # Play check sound if it's not checkmate
                                            game.play_check()
                                            pygame.display.update()
                                    else: # King is not in check
                                        if board.is_stalemate(opponent_king):
                                            game_over = True
                                            print("Stalemate detected!")
                                            self.show_stalemate(screen)
                                            game.play_stalemate()
                                            pygame.display.update()
                                            # Wait for 3 seconds to show the stalemate message
                                            pygame.time.wait(3000)
                                            # Exit to main menu
                                            break 
                                    # play sound
                                    if not check:
                                        game.play_sound(captured)
                                    check = False
                                    game.next_turn()
                        except Exception:
                            pass
                        
                    # key press
                    elif event.type == pygame.KEYDOWN:
                        
                        # changing themes
                        if event.key == pygame.K_t:
                            game.change_theme()
                            
                        # changing sounds
                        elif event.key == pygame.K_c:
                            game.change_sound()
                            
                        # restart
                        elif event.key == pygame.K_r:
                            game.reset()
                            dragger = self.game.dragger
                            game = self.game
                            board = self.game.board
                            
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                        
                        elif event.key == pygame.K_s:
                            en_passant = ''
                            castling='KQkq'
                            if board.is_enpassant_possible(): 
                                # (7, 4) -> (1, e) -> e1, position of white king
                                en_passant = f'{chr(board.last_pawn_move.final.col + 97)}{board.last_pawn_move.final.row}' 
                            castling = self.get_castling_rights(board)
                            self.save_game_to_fen(board, game.next_player, castling=castling , en_passant=en_passant)
                            print("Successfully saved!")
                            print(f"Current working directory: {os.getcwd()}")
                    # quit game 
                    elif event.type == pygame.QUIT: 
                        pygame.quit()
                        sys.exit()
                pygame.display.update()
    
    def start_new_game(self):
        '''
            Starts a new game.
            Reset the game object, which includes the board and other game states
        '''
        self.game.reset()
        
        # Refresh the screen
        self.game.show_bg(self.screen)
        self.game.show_pieces(self.screen)
        pygame.display.update()
        return 
        
    def load_game(self):
        ''' 
            Load a saved game from save.txt
        '''
        try:
            with open("save.txt", "r") as file:
                data = file.read().splitlines()

                # Extract FEN, turn, and other data
                fen_line = data[0].split(":")[1].strip()  # Get FEN string
                turn_line = data[1].split(":")[1].strip()  # Get current turn
                castling_line = data[2].split(":")[1].strip()  # Get castling rights (if stored)
                en_passant_line = data[3].split(":")[1].strip()  # Get en passant (if stored)

                print("Loaded game state:")
                print(f"FEN: {fen_line}")
                print(f"Turn: {turn_line}")
                print(f"Castling Rights: {castling_line}")
                print(f"En Passant: {en_passant_line}")

                # Reconstruct board from FEN
                self.load_board_from_fen(fen_line)

                # Set the turn to the correct player
                self.game.next_player = turn_line

                # Set castling rights (if applicable)
                self.set_castling_rights(castling_line)

                # Set en passant rights (if applicable)
                self.set_en_passant(en_passant_line)

        except FileNotFoundError:
            print("No saved game found.")
            
    def board_to_fen(self, board):
        '''
            Converts the current board to FEN (Forsyth-Edwards Notation)
        '''
        fen = ""
        for row in board.squares:
            empty_squares = 0
            for square in row:
                if square.isempty():
                    empty_squares += 1
                else:
                    if empty_squares > 0:
                        fen += str(empty_squares)
                        empty_squares = 0
                    fen += square.piece.fen_symbol()
            if empty_squares > 0:
                fen += str(empty_squares)
            fen += '/'
        fen = fen[:-1]  # Remove the last '/'
        return fen

    def save_game_to_fen(self, board, turn, castling='KQkq', en_passant='-', halfmove_clock=0, fullmove_number=1):
        '''
            Saves the current game to save.txt as FEN
        '''
        fen_board = self.board_to_fen(board)
        fen_turn = 'w' if turn == 'white' else 'b'
        fen = f"{fen_board} {fen_turn} {castling} {en_passant} {halfmove_clock} {fullmove_number}"
        
        with open("save.txt", "w") as file:
            file.write(f"FEN: {fen}\n")
    
    def get_castling_rights(self, board):
        castling_rights = ''
        
        # Check White's king and rooks
        white_king = board.kings[0]
        if not white_king.moved:
            if not white_king.left_rook.moved:
                castling_rights += 'Q'  # White can castle queenside
            if not white_king.right_rook.moved:
                castling_rights += 'K'  # White can castle kingside

        # Check Black's king and rooks
        black_king = board.kings[1]
        if not black_king.moved:
            if not black_king.left_rook.moved:
                castling_rights += 'q'  # Black can castle queenside
            if not black_king.right_rook.moved:
                castling_rights += 'k'  # Black can castle kingside

        # If no castling rights are left, return '-'
        return castling_rights if castling_rights else '-'

main = Main()
main.mainloop()