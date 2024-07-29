

class Counter:
    def __init__(self,initial) -> None:
        self.initial = initial
        self.count = initial
    
    def decrement(self):
        self.count -= 1
    
    def reset(self):
        self.count = self.initial