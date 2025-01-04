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
                        "Load Game (L)", 
                        "Quit Game (Q)", 
                        "During the game:", 
                        "Reset (R)", 
                        "Change Sound (S)", 
                        "Save Game (E)", 
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
                        elif event.key == pygame.K_s:
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
                        
                        # elif event.key == pygame.K_e:
                            # self.save_game(board_state, turn)
                    
                    # quit game 
                    elif event.type == pygame.QUIT: 
                        pygame.quit()
                        sys.exit()
                pygame.display.update()
    
    def start_new_game(self):
        # Reset the game object, which includes the board and other game states
        self.game.reset()
        
        # Refresh the screen
        self.game.show_bg(self.screen)
        self.game.show_pieces(self.screen)
        pygame.display.update()
        return 
        
    def load_game():
        ''' 
            Load a saved game from save.txt
        '''
        try:
            with open("save.txt", "r") as file:
                data = file.read().splitlines()
                print("Loaded game state:")
                for line in data:
                    print(line)  # You can process the game state further, like loading the board, etc.
        except FileNotFoundError:
            print("No saved game found.")
            
    def save_game(board_state, turn):
        with open("save.txt", "w") as file:
            # Save the board state
            file.write("Board State\n")
            file.write(str(board_state) + '\n')  # Board data
            file.write(f"Turn: {turn}\n")
    
main = Main()
main.mainloop()