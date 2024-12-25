import numpy as np
from collections import Counter
import json
import os
from move import Move

class ChessAI:
    def __init__(self, k=5):
        self.k = k
        self.move_database = self.load_database()

    def load_database(self):
        #Load chess moves database from JSON file
        try:
            with open('assets/database/chess_moves.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def board_to_feature_vector(self, board):
        #Convert board state to feature vector
        vector = []
        for row in range(8):
            for col in range(8):
                square = board.squares[row][col]
                if square.has_piece():
                    # Convert piece to numerical value
                    piece = square.piece
                    value = piece.value
                    vector.append(value)
                else:
                    vector.append(0)
        return np.array(vector)

    def find_similar_positions(self, current_board):
        #Find k most similar positions from database
        current_vector = self.board_to_feature_vector(current_board)
        
        if not self.move_database:
            return None

        similarities = []
        for position, moves in self.move_database.items():
            position_vector = np.array(json.loads(position))
            # Calculate Euclidean distance
            distance = np.linalg.norm(current_vector - position_vector)
            similarities.append((distance, moves))

        # Sort by similarity (smallest distance first)
        similarities.sort(key=lambda x: x[0])
        return similarities[:self.k]

    def get_best_move(self, board):
        #Get the most common move from k similar positions
        similar_positions = self.find_similar_positions(board)
        
        if not similar_positions:
            return None

        # Collect all moves from similar positions
        all_moves = []
        for _, moves in similar_positions:
            all_moves.extend(moves)

        if not all_moves:
            return None

        # Find most common move
        most_common_move = Counter(all_moves).most_common(1)[0][0]
        
        # Convert string move to Move object
        initial_square, final_square = self.parse_move_string(most_common_move)
        return Move(initial_square, final_square)

    def parse_move_string(self, move_str):
        """Convert move string (e.g., 'e2e4') to Square objects"""
        from square import Square
        
        col_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        
        initial_col = col_map[move_str[0]]
        initial_row = 8 - int(move_str[1])
        final_col = col_map[move_str[2]]
        final_row = 8 - int(move_str[3])

        return (Square(initial_row, initial_col), Square(final_row, final_col))