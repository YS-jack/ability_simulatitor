from math import nextafter
from allAbilities import *
from timeConvert import stot, ttos
from playerInfo import *
import calculator
from drawGraph import makeGraph
SIMULATIONTIME = 5 # seconds

class Bar():
    def __init__(self) -> None:
        self.atk = Attack()
        self.str = Strength()
        self.magic = Magic()
        self.range = Range()
        self.defence = Defence()
        self.const = Const()
        self.otherAbility = OtherAbility()
        self.bar = [self.magic.gchain, self.magic.sunshine, self.magic.dbreath, self.magic.magma_tempest, self.magic.corruption_blast, 
         self.magic.tsunami, self.magic.sonic_wave, self.magic.omnipower_igneous, self.magic.wild_magic,
        self.magic.deep_impact, self.defence.devotion, self.const.tuska, self.const.sacrifice, self.magic.combust]
        self.simt = stot(SIMULATIONTIME)#length of simulation in tick
        self.tc = 0
        self.adren = [0]*self.simt
        self.adren[0] = INITADREN
        self.simAbility = []*self.simt
        
        self.dmgPrimary = [] #[{"ability1":damage, "ability2":damage,...},{},...]
        self.dmgSecondary = []
        for i in range(self.simt):
            self.dmgPrimary.append({})
            self.dmgSecondary.append({})
        self.relentlessOffcd = 0
        self.dmgPTotal = 0
        self.dmgSTotal = 0

        self.berserkUlt = NOBERSERK #currently active berserk buff
        self.berserkOfftc = 0 #tc of until when berserk is active, set in flagBerserk()
        self.damageInst = calculator.Damage()
        """self.gchainBuff = NOTACTIVE
        self.gchainOfftc = 0 #tc of until when gchain effect is active"""

        self.damageCap = 12000
        if (GRIMOIRE):
            self.damageCap = 15000

    def printBarInfo(self):
        for b in self.bar:
            print(self.bar.index(b), b.name,":")
            print("\tcd =", b.cd)
            print("\tduration =", b.dur)
            print("\trequired adrenaline =", b.req)
            print("\tadrenaline change =", b.change)
    def flagBerserk(self, ability):
        if (ability == self.str.berserk):
            self.berserkUlt = BERSERK
            self.berserkOfftc = self.tc + BERSERKDUR
        elif (ability == self.magic.sunshine):
            self.berserkUlt = SUNSHINE
            self.berserkOfftc = self.tc + SUNSHINEDUR
        elif (ability == self.range.death_swift):
            self.berserkUlt = DEATHSSWIFTNESS
            self.berserkOfftc = self.tc + DEATHSWIFTNESSDUR
    def checkBerserk(self):
        if (self.berserkOfftc <= self.tc and self.berserkUlt != NOBERSERK):
            self.berserkUlt = NOBERSERK
    """def flagGchain(self, ability):
        if (ability == self.magic.gchain):
            self.gchainBuff = ACTIVE
            self.gchainOfftc = self.tc + GCHAINBUFFDUR
    def checkGchain(self, ability):
        if (self.gchainOfftc <= self.tc and self.gchainBuff =)"""
    def getNextAbility(self):
            if (self.tc == 0):
                currentAdren = INITADREN
            else:
                currentAdren = self.adren[self.tc - 1]
            for ability in self.bar:
                if (self.tc >= ability.offcd and currentAdren >= ability.req):
                    print("tick",self.tc,"used",ability.name)
                    self.flagBerserk(ability)#flag self.berserkUlt if ability is berserk variant
                    """self.flagGchain(ability) #flag self.gchainBuff if ability is gchain"""
                    return ability
            return self.otherAbility.noAbility #when no ability is available. TODO: replace with auto attack if its not on cd
    def addSimAbility(self, ability):
            for i in range(ability.dur):
                if (len(self.simAbility) + 1 > self.simt):
                    break
                else:
                    self.simAbility.append(ability)
    def fillHits(self, ability, pOrS):
        #fill hitP and hitS caused by "ability" input, including hits >self.tc
        self.checkBerserk()
        """gchainbuff = self.checkGchain(ability)"""
        if (pOrS == "p"):
            for i in range(len(ability.pDmg)):
                if (i + self.tc >= self.simt):
                    break
                tickHits = ability.pDmg[i]
                for j in range(len(tickHits)):
                    min = ability.pDmg[i][j][0]
                    max = ability.pDmg[i][j][1]
                    avDmg = self.damageInst.getAvDmg(min, max, ability, pOrS, self.berserkUlt)
                    if (avDmg > self.damageCap):
                        avDmg = self.damageCap
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
                    avDmg = self.damageInst.getAvDmg(min, max, ability, pOrS, self.berserkUlt)
                    self.dmgSTotal += avDmg
                    if (avDmg > 0):
                        if (ability in self.dmgSecondary[i + self.tc]):
                            self.dmgSecondary[i + self.tc][ability].append(avDmg)
                        else:
                            self.dmgSecondary[i + self.tc][ability] = [avDmg]
                        #check poison proc, call fillHits(posion ability, "s")?

    def renewAdren(self, ability):
        if (not ability == self.otherAbility.noAbility):#dont add nor subtract adren if ability = noAbility
            abilityAdrenGain = ability.getAdren(self.tc, self.relentlessOffcd)
            if (abilityAdrenGain == 0):#set relentless on cooldown
                self.relentlessOffcd = self.tc + stot(RELENTLESSCD)
            if (self.tc == 0):
                self.adren[self.tc] += abilityAdrenGain
            else:
                self.adren[self.tc] = self.adren[self.tc - 1] + abilityAdrenGain
            if (self.adren[self.tc] >= 100 + HEIGHTENEDSENSES * 10):
                self.adren[self.tc] = 100 + HEIGHTENEDSENSES * 10
            for t in range(self.tc + 1, self.tc + ability.dur):
                if (t < self.simt):
                    self.adren[t] += self.adren[t-1]
                    if (self.adren[t] < 0):
                        print("adrenaline below 0 after using",self.simAbility[self.tc])
                    if (self.adren[t] >= 100 + HEIGHTENEDSENSES * 10):
                        self.adren[t] = 100 + HEIGHTENEDSENSES * 10
            
    def setcd(self, ability):
        ability.offcd = self.tc + ability.cd
    
    def simulate(self):
        while self.tc < self.simt:
            nextAbility = self.getNextAbility() #check what ability would be used at tick self.tc, type(nextAbility) same as type(self.bar[i])
            self.addSimAbility(nextAbility) #edit simAbility
            self.fillHits(nextAbility, "p") #fill dmgPriamry[{}]
            self.fillHits(nextAbility, "s") #dmgSecondary[{}]
            self.renewAdren(nextAbility) #calc adren, edit adren[]
            self.setcd(nextAbility)
            self.tc += nextAbility.dur
            
    def printSimulationResult(self):
        print("simulation time\t=", ttos(self.simt),"seconds")
        print()
        print("Primary dmg/s \t\t=",self.dmgPTotal/ttos(self.simt))
        print("Primary dmg/min \t=",self.dmgPTotal*60/ttos(self.simt))
        print("Total primary damage\t=",self.dmgPTotal)
        print()
        print("Secondary dmg/s \t=",self.dmgSTotal/ttos(self.simt))
        print("Secondary dmg/min \t=",self.dmgSTotal*60/ttos(self.simt))
        print("Total secondary damage\t=",self.dmgSTotal)
        print()
        for i in range(self.simt):
            print("tick", i, end=", ")
            print("Primary damage : ",end="")
            for hitAbility in self.dmgPrimary[i]:
                print(hitAbility.name, self.dmgPrimary[i][hitAbility], end=", ")
            print("Secondary damage : ",end="")
            for hitAbilityS in self.dmgSecondary[i]:
                print(hitAbilityS.name, self.dmgSecondary[i][hitAbilityS], end=", ")
            if (self.adren[i] == self.adren[i-1]):
                print("adren = ..", end=", ")
            else:
                print("adren =", self.adren[i], end=", ")
            if (self.simAbility[i] == self.simAbility[i-1]):
                print("ability used:    ..")
            else:
                print("ability used:", self.simAbility[i].name)
            
    
    def showResutGraph(self):
        makeGraph.psCompare(self.dmgPrimary,self.dmgSecondary)
        makeGraph.pDetail(self.dmgPrimary)
        makeGraph.sDetail(self.dmgSecondary)