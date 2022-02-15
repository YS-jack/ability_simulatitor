from allAbilities import *
from timeConvert import stot
from playerInfo import *
SIMULATIONTIME = 60 + 20 # seconds

class Bar():
    def __init__(self) -> None:
        magic = Magic()
        defence = Defence()
        const = Const()
        self.bar = [magic.gconc, magic.wild_magic, magic.sunshine, magic.dbreath, 
        magic.corruption_blast, magic.asphyx, magic.combust, 
        magic.wrack, const.tuska, const.sacrifice, magic.omnipower_igneous]
        self.simt = stot(SIMULATIONTIME)#length of simulation in tick
        self.tc = 0
        self.adren = [0]*self.simt
        self.adren[0] = INITADREN
        self.simAbility = []
        self.dmgPrimary = [{}]*self.simt #[{"ability1":damage, "ability2":damage,...},{},...]
        self.dmgSecondary = [{}]*self.simt
        self.relentlessOffcd = 0

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
    def addDamage(self, ability):
        #write damage to self.dmgPrimary[] and self.dmgSecondary[]
        #add addtional adren gain from crits and inspiration aura to self.adren[]
        pass
    def renewAdren(self, ability):
        abilityAdrenGain = ability.getAdren(self.tc, self.relentlessOffcd)
        if (abilityAdrenGain == 0):#set relentless on cooldown
            self.relentlessOffcd = self.tc + stot(RELENTLESSCD)
        print("adrenaline gain from", ability.name, "=", abilityAdrenGain)
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
            nextAbility = self.getNextAbility() #check what ability would be used at tick self.tc
            if (nextAbility == 0):#TODO: check if this works
                self.tc += 1
                continue
            self.addSimAbility(nextAbility) #edit simAbility
            self.addDamage(nextAbility) #calc damage, edit dmgPriamry[{}], edit dmgSecondary[{}]
            self.renewAdren(nextAbility) #calc adren, edit adren[]
            self.setcd(nextAbility)
            self.tc += nextAbility.dur

    def printSimulationResult(self):
        for i in range(self.simt):
            print("tick", i, end=", ")
            if (i > 0):
                if (self.adren[i] == self.adren[i-1]):
                    print("adren = ..", end=", ")
                else:
                    print("adren =", self.adren[i], end=", ")
                if (self.simAbility[i] == self.simAbility[i-1]):
                    print("ability :    ..")
                else:
                    print("ability :", self.simAbility[i].name)
            else:
                print("adren =", self.adren[i], " ,ability :",self.simAbility[i].name)
            #print("\t\tdmg on primary:", 100, "\tdmg on secondary:", 100)