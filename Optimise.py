class Optimizer():
    def __init__(self) -> None:
        self.topPrimary = 0
        self.topSecondary = 0
    
    def findBestAOE(self, pool):
        barLen = min(14, len(pool))
        allBar = []
        