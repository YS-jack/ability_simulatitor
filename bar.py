from allAbilities import *
from timeConvert import stot, ttos
from playerInfo import *
from calculator import *
SIMULATIONTIME = 10 # seconds

class Bar():
    def __init__(self) -> None:
        magic = Magic()
        defence = Defence()
        const = Const()
        self.bar = [magic.gconc, magic.omnipower_igneous, magic.wild_magic, magic.sunshine, magic.dbreath, 
        magic.corruption_blast, magic.asphyx, magic.combust, 
        magic.wrack, const.tuska, const.sacrifice, defence.devotion]
        self.simt = stot(SIMULATIONTIME)#length of simulation in tick
        self.tc = 0
        self.adren = [0]*self.simt
        self.adren[0] = INITADREN
        self.simAbility = []
        
        self.dmgPrimary = [] #[{"ability1":damage, "ability2":damage,...},{},...]
        self.dmgSecondary = []
        for i in range(self.simt):
            self.dmgPrimary.append({})
            self.dmgSecondary.append({})
        self.relentlessOffcd = 0
        self.dmgPTotal = 0
        self.dmgSTotal = 0

    def printBarInfo(self):
        for b in self.bar:
            print(self.bar.index(b), b.name,":")
            print("\tcd =", b.cd)
            print("\tduration =", b.dur)
            print("\trequired adrenaline =", b.req)
            print("\tadrenaline change =", b.change)
    
    def getNextAbility(self):
            if (self.tc == 0):
                currentAdren = INITADREN
            else:
                currentAdren = self.adren[self.tc - 1]
            for ability in self.bar:
                if (self.tc >= ability.offcd and currentAdren >= ability.req):
                    return ability
            return 0
    def addSimAbility(self, ability):
            for i in range(ability.dur):
                if (len(self.simAbility) >= self.simt):
                    break
                self.simAbility.append(ability)
    def fillHits(self, ability, pOrS):
        #fill hitP and hitS caused by "ability" input, including hits >self.tc
        if (pOrS == "p"):
            for i in range(len(ability.pDmg)):
                if (i + self.tc >= self.simt):
                    break
                tickHits = ability.pDmg[i]
                for j in range(len(tickHits)):
                    min = ability.pDmg[i][j][0]
                    max = ability.pDmg[i][j][1]
                    avDmg = Damage.getAvDmg(min, max, ability)
                    self.dmgPTotal += avDmg
                    if (avDmg > 0):
                        if (ability in self.dmgPrimary[i + self.tc]):
                            self.dmgPrimary[i + self.tc][ability].append(avDmg)
                        else:
                            self.dmgPrimary[i + self.tc][ability] = [avDmg]
                        #check poison proc, call fillHits(posion ability, "p")?
        elif(pOrS == "s"):
            for i in range(len(ability.sDmg)):
                if (i + self.tc >= self.simt):
                    break
                tickHits = ability.sDmg[i]
                for j in range(len(tickHits)):
                    min = ability.sDmg[i][j][0]
                    max = ability.sDmg[i][j][1]
                    avDmg = Damage.getAvDmg(min, max, ability)
                    self.dmgSTotal += avDmg
                    if (avDmg > 0):
                        if (ability in self.dmgSecondary[i + self.tc]):
                            self.dmgSecondary[i + self.tc][ability].append(avDmg)
                        else:
                            self.dmgSecondary[i + self.tc][ability] = [avDmg]
                        #check poison proc, call fillHits(posion ability, "s")?

    def renewAdren(self, ability):
        abilityAdrenGain = ability.getAdren(self.tc, self.relentlessOffcd)
        if (abilityAdrenGain == 0):#set relentless on cooldown
            self.relentlessOffcd = self.tc + stot(RELENTLESSCD)
        if (self.tc == 0):
            self.adren[self.tc] += abilityAdrenGain
        else:
            self.adren[self.tc] = self.adren[self.tc - 1] + abilityAdrenGain
        if (self.adren[self.tc] >= 100 + CONSERVATIONOFENERGY * 10):
            self.adren[self.tc] = 100 + CONSERVATIONOFENERGY * 10
        for t in range(self.tc + 1, self.tc + ability.dur):
            if (t < self.simt):
                self.adren[t] += self.adren[t-1]
                if (self.adren[t] >= 100 + CONSERVATIONOFENERGY * 10):
                    self.adren[t] = 100 + CONSERVATIONOFENERGY * 10
                
    def setcd(self, ability):
        ability.offcd = self.tc + ability.cd
    
    def simulate(self):
        while self.tc < self.simt:
            nextAbility = self.getNextAbility() #check what ability would be used at tick self.tc, type(nextAbility) same as type(self.bar[i])
            if (nextAbility == 0):#TODO: check if this works
                self.tc += 1
                continue
            self.addSimAbility(nextAbility) #edit simAbility
            self.fillHits(nextAbility, "p") #fill dmgPriamry[{}]
            self.fillHits(nextAbility, "s") #dmgSecondary[{}]
            self.renewAdren(nextAbility) #calc adren, edit adren[]
            self.setcd(nextAbility)
            self.tc += nextAbility.dur
            
    def printSimulationResult(self):
        print("simulation time :\t", ttos(self.simt),"seconds")
        print("Primary dmg/s =\t",self.dmgPTotal/ttos(self.simt))
        print("Primary dmg/min =\t",self.dmgPTotal*60/ttos(self.simt))
        print("Total primary damage\t:",self.dmgPTotal)
        print()
        print("Secondary dmg/s =\t",self.dmgSTotal/ttos(self.simt))
        print("Secondary dmg/min =\t",self.dmgSTotal*60/ttos(self.simt))
        print("Total secondary damage\t:",self.dmgSTotal)
        print()
        for i in range(self.simt):
            print("tick", i, end=", ")
            for hitAbility in self.dmgPrimary[i]:
                print(hitAbility.name, self.dmgPrimary[i][hitAbility], end=", ")
            if (i > 0):
                if (self.adren[i] == self.adren[i-1]):
                    print("adren = ..", end=", ")
                else:
                    print("adren =", self.adren[i], end=", ")
                if (self.simAbility[i] == self.simAbility[i-1]):
                    print("ability used:    ..")
                else:
                    print("ability used:", self.simAbility[i].name)
            else:
                print("adren =", self.adren[i], " ,ability used :",self.simAbility[i].name)
            #print("\t\tdmg on primary:", 100, "\tdmg on secondary:", 100)