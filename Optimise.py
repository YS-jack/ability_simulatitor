from itertools import permutations
from bar import Bar
from datetime import datetime

class Optimizer():
    def __init__(self) -> None:
        pass

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
    def printTime(self):
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        print("date and time =", dt_string)
    def printDateTime(self):
        now = datetime.now()
        dt_string = now.strftime("%m-%d  %Hh %Mm %Ss")
        print("date and time =", dt_string)
        return dt_string

    def copyInstInfo(self, newbarInst, originalInst):
        newbarInst.poisonDmg = originalInst.poisonDmg
        """newbarInst.atk = originalInst.atk
        newbarInst.str = originalInst.str
        newbarInst.magic = originalInst.magic
        newbarInst.range = originalInst.range
        newbarInst.defence = originalInst.defence
        newbarInst.const = originalInst.const
        newbarInst.otherAbility = originalInst.otherAbility"""
        """newbarInst.otherAbs = originalInst.otherAbs
        newbarInst.otherCanHeal = originalInst.otherCanHeal"""
        #newbarInst.damageInst = originalInst.damageInst (for unknown reason this decreases damage for every bar except the first)
        #newbarInst.enemy = originalInst.enemy (for unknown reason this disables bloodreaver)

    def findTopAOE(self, bar, pool, topN):#TODO save top 5 just in case?
        topDmgS = [0]
        topDmgP = [0]
        topDmgBars = [Bar()]

        for barPattern in permutations(pool):
            #init ability cd
            for ability in pool:
                ability.offcd = 0
            barInst = Bar()
            barInst.bar=barPattern
            self.copyInstInfo(barInst,bar)
            barInst.simulate()
            dpsS = barInst.getDpsS()
            #find if in top topN
            if (topDmgS[-1] < dpsS):
                for i in range(len(topDmgS)):
                    if(topDmgS[i] < dpsS):
                        topDmgS.insert(i, dpsS)
                        topDmgBars.insert(i, barPattern)
                        topDmgP.insert(i, barInst.getDpsP())
                        if (i == 0):
                            print("[",end="")
                            for ability in barPattern:
                                print(ability.name,end=", ")
                            print("]\texpected dps on secondary targets(average) =",dpsS)
                            self.printTime()
                            print()
                        if (len(topDmgS) > topN):
                            del topDmgS[-1]
                            del topDmgBars[-1]
                            del topDmgP[-1]
                        break

        f = open("outputfile "+self.printDateTime()+".txt","w")
        print("top",topN,"bars:")
        for i in range(len(topDmgBars)):
            line = "["
            print("[",end="")
            for ability in topDmgBars[i]:
                print(ability.name,end=", ")
                line = line + ability.name + ", "
            print("]\texpected primary dps =",topDmgP[i],", secondary dps =",topDmgS[i],end="\n\n")
            line = line + "]\texpected primary dps ="+str(topDmgP[i])+", secondary dps ="+str(topDmgS[i])
            f.write(line+"\n")
        f.close()

        return(topDmgBars[0])

        
    def printBestBarInfo(self, bar, bestBarPattern):
        for ability in bestBarPattern:
                ability.offcd = 0
        barInst = Bar()
        barInst.bar = bestBarPattern
        self.copyInstInfo(barInst, bar)
        barInst.simulate()
        #print("*************\tinfo of best bar:")
        #barInst.printSimulationResult()
        barInst.setDmgDitc()
        barInst.showResutGraph()