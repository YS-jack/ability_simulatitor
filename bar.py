import math
import random
from pickle import TRUE
from allAbilities import *
from timeConvert import stot, ttos
from playerInfo import *
import calculator
from drawGraph import makeGraph
SIMULATIONTIME = 60 # seconds

class Bar():
    def __init__(self) -> None:
        self.atk = Attack()
        self.str = Strength()
        self.magic = Magic()
        self.range = Range()
        self.defence = Defence()
        self.const = Const()
        self.otherAbility = OtherAbility()
        """self.bar = [self.magic.sunshine, self.magic.gchain,self.magic.dbreath,self.magic.tsunami, self.magic.wild_magic, 
        self.magic.sonic_wave, self.magic.corruption_blast, self.magic.magma_tempest, self.magic.deep_impact, 
        self.defence.devotion, self.const.tuska, self.magic.combust, self.const.sacrifice, self.magic.omnipower_igneous]"""
        self.bar = [self.magic.sunshine, self.magic.gchain,self.magic.tsunami,self.magic.dbreath,
        self.magic.wild_magic,self.magic.corruption_blast,self.magic.deep_impact,self.magic.magma_tempest,
        self.magic.sonic_wave,self.defence.devotion, self.const.tuska, self.magic.combust, self.const.sacrifice, self.magic.wrack]
        
        self.simt = stot(SIMULATIONTIME)#length of simulation in tick
        self.tc = 0
        self.abilityCd = 0
        self.adren = [0]*self.simt
        self.adren[0] = INITADREN
        self.simAbility = [] #[[ability, ability (activated in same tick, like poison, aftershock, puncture, ...)],[],[],...]       
        self.dmgPrimary = [] #[{"ability1":damage, "ability2":damage,...},{},...]
        self.dmgSecondary = []
        for i in range(self.simt):
            self.simAbility.append([])
            self.dmgPrimary.append({})
            self.dmgSecondary.append({})

        self.relentlessOffcd = 0
        self.dmgPTotal = 0
        self.dmgSTotal = 0

        self.berserkUlt = NOBERSERK #currently active berserk buff
        self.berserkOfftc = 0 #tc of until when berserk is active, set in flagBerserk()
        self.damageInst = calculator.Damage()
        self.gchainBuff = NOTACTIVE
        self.gchainOfftc = 0 #tc of until when gchain effect is active

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
        if (self.berserkOfftc <= self.tc and self.berserkUlt != NOBERSERK):#turn of beserk mode if past offtc
            self.berserkUlt = NOBERSERK
    def flagGchain(self, ability):
        if (ability == self.magic.gchain):
            self.gchainBuff = ACTIVE
            self.gchainOfftc = self.tc + GCHAINBUFFDUR
    def checkGchain(self, ability):
        if (self.gchainOfftc >= self.tc and self.gchainBuff == ACTIVE and ability != self.magic.magma_tempest and ability != self.magic.gchain):#if not used yet
            self.gchainOfftc = 0
            self.gchainBuff = NOTACTIVE
            if (ability == self.magic.corruption_blast):
                return 1 #return multiplier of damage
            else:
                return 0.5
        else:
            return 0
    def checkPoisonProc(self):
        if (not CINDERBANE):
            return NOTACTIVE
        p = POISONPROCCHANCE
        if (random.random() < p):
            return ACTIVE
    def getNextAbility(self):
            if (self.tc == 0):
                currentAdren = INITADREN
            else:
                currentAdren = self.adren[self.tc - 1]
            if (self.abilityCd > self.tc): #during gcd or still doing channeled
                return self.otherAbility.noAbility
            for ability in self.bar:
                if (self.tc >= ability.offcd and currentAdren >= ability.req):
                    self.flagBerserk(ability)#flag self.berserkUlt if ability is berserk variant
                    self.flagGchain(ability) #flag self.gchainBuff if ability is gchain
                    return ability
            print("no ability was available at tick",self.tc,"for bar ",end="")
            print("[",end="")
            for ability in self.bar:
                print(ability.name,end=", ")
            print("]")
            return self.otherAbility.noAbility #when no ability is available. TODO: replace with auto attack if its not on cd
    def addSimAbility(self, ability):
            if (len(self.simAbility[self.tc]) < self.simt and ability != self.otherAbility.noAbility):
                self.simAbility[self.tc].insert(0,ability)

    def fillHits(self, pOrS):#fill hitP and hitS caused by "ability" input, including hits > self.tc
        if (len(self.simAbility[self.tc]) == 0):
                return 0
        for ability in self.simAbility[self.tc]:
            print(ability.name)
            self.checkBerserk()
            if (pOrS == "p"):
                if(ability != self.magic.corruption_blast):#for gchain maths
                    gchainmult = self.checkGchain(ability)
                for i in range(len(ability.pDmg)):#for every hit ability will do
                    if (i + self.tc >= self.simt):
                        break
                    tickHits = ability.pDmg[i] #tickHits is list of damage done by 1 ability in 1 tick (e.g. omnipower 2nd-4th hits)
                    for j in range(len(tickHits)):
                        min = ability.pDmg[i][j][0]
                        max = ability.pDmg[i][j][1]
                        avDmg = self.damageInst.getAvDmg(min, max, ability, pOrS, self.berserkUlt) #get average damage of 1 hit of tickHits
                        if (avDmg > self.damageCap):#consider damage cap
                            avDmg = self.damageCap
                        self.dmgPTotal += avDmg #add to damage count
                        if (avDmg > 0):
                            if (ability in self.dmgPrimary[i + self.tc]):#if ability is already listed in dmgPrimary at same tick
                                self.dmgPrimary[i + self.tc][ability].append(avDmg) #append
                            else: #other wise
                                self.dmgPrimary[i + self.tc][ability] = [avDmg] #make new dictionary index
                            #process for gchain damage caluclation on secondary targets
                            if (ability == self.magic.corruption_blast):
                                gchainmult = self.checkGchain(ability)
                            if (gchainmult):#add damage to secondary targets if gchain buff is active
                                if (ability in self.dmgSecondary[i + self.tc]):
                                    self.dmgSecondary[i + self.tc][ability].append(avDmg*self.damageInst.caromingDmgMult()*gchainmult)
                                else:
                                    self.dmgSecondary[i + self.tc][ability] = [avDmg*self.damageInst.caromingDmgMult()*gchainmult]
                            #check poison proc, append to self.simAbility
                            if (self.checkPoisonProc and self.tc + 1 < self.simt):
                                self.simAbility[self.tc + 1].append(self.otherAbility.poisonP)

            elif(pOrS == "s"):
                for i in range(len(ability.sDmg)):
                    if (i + self.tc >= self.simt):
                        break
                    tickHits = ability.sDmg[i]
                    for j in range(len(tickHits)):
                        min = ability.sDmg[i][j][0]
                        max = ability.sDmg[i][j][1]
                        avDmg = self.damageInst.getAvDmg(min, max, ability, pOrS, self.berserkUlt)
                        avDmg *= self.damageInst.aoeDmgMult(ability.nAOE)
                        self.dmgSTotal += avDmg
                        if (avDmg > 0):
                            if (ability in self.dmgSecondary[i + self.tc]):
                                self.dmgSecondary[i + self.tc][ability].append(avDmg)
                            else:
                                self.dmgSecondary[i + self.tc][ability] = [avDmg]
                            #check poison proc, add to simAbility[self.tc + 1]
                            if (self.checkPoisonProc and self.tc + 1 < self.simt):
                                self.simAbility[self.tc + 1].append(self.otherAbility.poisonS)

    def renewAdren(self, ability):
        if (ability != self.otherAbility.noAbility and ability != self.otherAbility.poisonP and ability != self.otherAbility.poisonS):#dont add nor subtract adren if ability = noAbility or poison
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
                        print("adrenaline below 0 after using",ability.name)
                    if (self.adren[t] >= 100 + HEIGHTENEDSENSES * 10):
                        self.adren[t] = 100 + HEIGHTENEDSENSES * 10
    def setcd(self, ability):
        ability.offcd = self.tc + ability.cd
        self.abilityCd = self.tc + ability.cd
    def roundDownHits(self,dmgPS):
        for i in range(len(dmgPS)):
            for index in dmgPS[i]:
                for j in range(len(dmgPS[i][index])):
                    dmgPS[i][index][j] = math.floor(dmgPS[i][index][j])

    def simulate(self):
        while self.tc < self.simt:
            nextAbility = self.getNextAbility() #check what ability would be used at tick self.tc, type(nextAbility) same as type(self.bar[i])
            self.addSimAbility(nextAbility) #edit simAbility
            self.fillHits("p") #fill dmgPriamry[{}]
            self.fillHits("s") #dmgSecondary[{}]
            self.renewAdren(nextAbility) #calc adren, edit adren[]
            self.setcd(nextAbility)
            self.tc += 1
        self.roundDownHits(self.dmgPrimary)
        self.roundDownHits(self.dmgSecondary)

    def printSimulationResult(self):
        print("simulation time\t=", ttos(self.simt),"seconds")
        print()
        print("Primary dmg/s \t\t=",self.dmgPTotal/ttos(self.simt))
        print("Primary dmg/min \t=",self.dmgPTotal*60/ttos(self.simt))
        print("average time to kill primary enemy \t", ENEMYHEALTH/(self.dmgPTotal/ttos(self.simt)))
        print("Total primary damage\t=",self.dmgPTotal)
        print()
        print("Secondary dmg/s \t=",self.dmgSTotal/ttos(self.simt))
        print("Secondary dmg/min \t=",self.dmgSTotal*60/ttos(self.simt))
        print("average time to kill secondary enemy \t", ENEMYHEALTH/(self.dmgSTotal/ttos(self.simt)))
        print("Total secondary damage\t=",self.dmgSTotal)
        print()
        print("[",end="")
        for ability in self.bar:
            print(ability.name,end=", ")
        print("]")
        for i in range(self.simt):
            print("tick", i, end=", ")
            print("Primary damage : ",end="")
            for hitAbility in self.dmgPrimary[i]:
                print(hitAbility.name, self.dmgPrimary[i][hitAbility], end=", ")
            print("Secondary damage : ",end="")
            for hitAbilityS in self.dmgSecondary[i]:
                print(hitAbilityS.name, self.dmgSecondary[i][hitAbilityS], end=", ")
            if (self.adren[i] == self.adren[i-1]):
                print("adren = ..")
            else:
                print("adren =", self.adren[i])
            for j in range(len(self.simAbility[i])):
                print("ability activated:", self.simAbility[i][j].name)
            
    
    def showResutGraph(self):
        makeGraph.psCompare(self.dmgPrimary,self.dmgSecondary, self.simAbility, self.bar)
        makeGraph.pDetail(self.dmgPrimary, self.simAbility, self.bar)
        makeGraph.sDetail(self.dmgSecondary, self.simAbility, self.bar)