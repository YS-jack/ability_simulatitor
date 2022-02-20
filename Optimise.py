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


    def findTopAOE(self, pool, topN):#TODO save top 5 just in case?
        topDmgS = [0]
        topDmgP = [0]
        topDmgBars = [Bar()]
        barInst = [Bar()]
        for barPattern in self.permutation(pool):
            #init ability cd
            for ability in pool:
                ability.offcd = 0
            barInst.append(Bar())
            del barInst[0]
            barInst[0].bar=barPattern
            barInst[0].simulate()
            #find if in top topN
            if (topDmgS[-1] < barInst[0].getExpectedDpsS()):
                for i in range(len(topDmgS)):
                    if(topDmgS[i] < barInst[0].getExpectedDpsS()):
                        topDmgS.insert(i, barInst[0].getExpectedDpsS())
                        topDmgBars.insert(i, barPattern)
                        topDmgP.insert(i, barInst[0].getExpectedDpsP())
                        if (i == 0):
                            print("[",end="")
                            for ability in barPattern:
                                print(ability.name,end=", ")
                            print("]\texpected damage on secondary targets(average) =",barInst[0].getExpectedDpsS(),end="\n\n")
                        if (len(topDmgS) > topN):
                            del topDmgS[-1]
                            del topDmgBars[-1]
                            del topDmgP[-1]
                        break

        print("top",topN,"bars:")
        for i in range(len(topDmgBars)):
            print("[",end="")
            for ability in topDmgBars[i]:
                print(ability.name,end=", ")
            print("]\texpected primary dps =",topDmgP[i],", secondary dps =",topDmgS[i],end="\n\n")

        self.printBestBarInfo(topDmgBars[0])
        
    def printBestBarInfo(self, bestBarPattern):
        for ability in bestBarPattern:
                ability.offcd = 0
        barInst = Bar()
        barInst.bar = bestBarPattern
        barInst.simulate()
        #print("*************\tinfo of best bar:")
        #barInst.printSimulationResult()
        barInst.showResutGraph()