class Move:
    
    def __init__(self, initial, final, is_enpassant = False):
        # initial and final are squares 
        self.initial = initial
        self.final = final
        self.is_enpassant = is_enpassant
        
    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final
    
    