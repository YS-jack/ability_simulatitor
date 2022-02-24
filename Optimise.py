from bar import Bar
from datetime import datetime
from multiprocessing import Process, Queue, Pipe
import math
from time import sleep
import numpy as np

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
        
    def printDateTime(self):
        now = datetime.now()
        dt_string = now.strftime("%m-%d  %Hh %Mm %Ss")
        print("date and time =", dt_string)
        return dt_string

    def copyInstInfo(self, newbarInst, originalInst):
        newbarInst.poisonDmg = originalInst.poisonDmg
    
    def simulate(self, q, bar, pool, permPool, id):
        for barPattern in permPool:
            for ability in pool:
                ability.offcd = 0
            barInst = Bar()
            barInst.bar=barPattern
            self.copyInstInfo(barInst,bar)
            barInst.simulate()
            dpsS = barInst.getDpsS()
            dpsP = barInst.getDpsP()
            q.put([barPattern, dpsS, dpsP])
        while 1:
            q.put(id)
            sleep(1)
        
    def rank(self,q, conn, topN, nPc):
        topDmgS = [0]
        topDmgP = [0]
        topDmgBars = [Bar()]
        count = np.zeros((nPc))
        while np.sum(count) != nPc:
            valList = q.get(True)
            if type(valList) == int:
                count[valList] = 1
                print(f'process {valList} ended, count = {count}')
                continue
            barPattern = valList[0]
            dpsS = valList[1]
            dpsP = valList[2]
            #find if in top topN
            if (topDmgS[-1] < dpsS):
                for i in range(len(topDmgS)):
                    if(topDmgS[i] < dpsS):
                        topDmgS.insert(i, dpsS)
                        topDmgBars.insert(i, barPattern)
                        topDmgP.insert(i, dpsP) #barInst.getDpsP()
                        if (i == 0):
                            print("[",end="")
                            for ability in barPattern:
                                print(ability.name,end=", ")
                            print("]\texpected dps on secondary targets(average) =",dpsS)
                            print("date and time =", datetime.now().strftime("%H:%M:%S"),end="\n\n")
                        if (len(topDmgS) > topN):
                            del topDmgS[-1]
                            del topDmgBars[-1]
                            del topDmgP[-1]
                        break
        conn.send([topDmgBars,topDmgP,topDmgS])
        conn.close()

    def findTopAOE(self, bar, pool, topN):#TODO save top 5 just in case?
        nPc = 7
        q = Queue()
        permList = self.permutation(pool)
        permLen = math.floor(len(permList)/nPc)
        parent_conn, child_conn = Pipe()
        
        pRank = Process(target=self.rank, args=(q, child_conn, topN, nPc)) #last input is number of pSim
        pRank.start()
        
        proceList = [Process(target=self.simulate, args=(q, bar, pool, permList[permLen*i:permLen*(i+1)], i)) for i in range(nPc)]
        for p in proceList:
            p.start()
        
        valList = parent_conn.recv()
        for p in proceList:
            p.terminate()
        pRank.terminate()

        topDmgBars = valList[0]
        topDmgP = valList[1]
        topDmgS = valList[2]            

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