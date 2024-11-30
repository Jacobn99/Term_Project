class Civilization:
    def __init__(self):
        self.settlements = set()
        self.sciencePerTurn = 0
        self.goldPerTurn = 0
        
    def addSettlement(self, settlement):
        self.settlements.add(settlement)
    
    def removeSettlement(self, settlement):
        self.settlements.remove(settlement)
    