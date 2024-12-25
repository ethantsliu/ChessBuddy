import json
import os

def create_empty_database():
    """Create an empty database structure"""
    database = {
        # Format: "board_state_vector": ["move1", "move2", ...]
        # Example: "[0,0,1,...]": ["e2e4", "d2d4", ...]
    }
    
    os.makedirs('assets/database', exist_ok=True)
    
    with open('assets/database/chess_moves.json', 'w') as f:
        json.dump(database, f)

if __name__ == "__main__":
    create_empty_database() 