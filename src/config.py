import pygame
import os 

from sound import Sound
from theme import Theme

class Config:
    
    def __init__(self):
        
        # color theme
        self.themes = []
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]
        
        # font
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        
        # sounds
        self.sounds = []
        self._add_sounds()
        self.idxs = 0 
        self.sound = self.sounds[self.idxs] 
        self.move_sound = Sound(os.path.join('assets/sounds/' + self.sound[0]))
        self.checkmate = Sound(os.path.join('assets/sounds/chess_com_checkmate.mp3'))
        self.promote = Sound(os.path.join('assets/sounds/chess_com_promote.mp3'))
        self.castling = Sound(os.path.join('assets/sounds/chess_com_castle.mp3'))
        self.capture_sound = Sound(
            os.path.join('assets/sounds/' + self.sound[1]))
    
    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]
    
    def _add_themes(self):
        green = Theme((234, 235, 200), (119, 154, 88), (244, 247, 116), (172, 195, 51), '#C86464', '#C84646')
        brown = Theme((235, 209, 166), (165, 117, 80), (245, 234, 100), (209, 185, 59), '#C86464', '#C84646')
        blue = Theme((229, 228, 200), (60, 95, 135), (123, 187, 227), (43, 119, 191), '#C86464', '#C84646')
        gray = Theme((232, 235, 239), (125, 135, 150), (244, 247, 116), (172, 195, 51), '#C86464', '#C84646')
        
        self.themes = [green, brown, blue, gray]
        
        '''
        Gray 
        color = (232, 235, 239)
                
                else: 
                    color = (125, 135, 150)
        '''
        
    def _add_sounds(self):
        lichess = ['lichess_move.mp3', 'lichess_capture.mp3']
        
        chess_com = ['chess_com_move.mp3', 'chess_com_capture.mp3']
        
        standard = ['move.wav', 'capture.wav']
        
        self.sounds = [lichess, chess_com, standard]
    
    def change_sound(self):
        self.idxs += 1
        self.idxs %= len(self.sounds)
        self.sound = self.sounds[self.idxs]
        self.move_sound = Sound(os.path.join('assets/sounds/' + self.sound[0]))
        self.capture_sound = Sound(
            os.path.join('assets/sounds/' + self.sound[1]))