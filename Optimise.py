from itertools import combinations
from bar import Bar

class Optimizer():
    def __init__(self) -> None:
        self.topPrimary = 0
        self.topSecondary = 0
    
    def permutation(self, pool):
        if (len(pool) == 0):
            return []
        if (len(pool) == 1):
            return [pool]
        l = []
        for i in range(len(pool)):
            m  = pool[i]
            remLst = pool[:i] + pool[i+1:]
            for p in self.permutation(remLst):
                l.append([m] + p)
        return l


    def findBestAOE(self, pool):#TODO save top 5 just in case?
        bestDmg = 0
        barInst = [Bar()]
        for barPattern in self.permutation(pool):
            #init ability cd
            for ability in pool:
                ability.offcd = 0
            barInst.append(Bar())
            del barInst[0]
            barInst[0].bar=barPattern
            barInst[0].simulate()

            print("[",end="")
            for ability in barPattern:
                print(ability.name,end=" ")
            print("]\n\texpected damage on secondary targets(average) =",barInst[0].getExpectedDpsS(),end="\n\n")

            if (bestDmg < barInst[0].getExpectedDpsS()):
                bestDmg = barInst[0].getExpectedDpsS()
                bestBarPattern = barPattern
        self.printBestBarInfo(bestBarPattern)
        
    def printBestBarInfo(self, bestBarPattern):
        for ability in bestBarPattern:
                ability.offcd = 0
        barInst = Bar()
        barInst.bar = bestBarPattern
        barInst.simulate()
        print("*************\tinfo of best bar:")
        barInst.printSimulationResult()
        barInst.showResutGraph()