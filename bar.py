from lib2to3.pgen2.token import MINUS
import math
from timeConvert import stot, ttos
from playerInfo import * #INITADREN, NOTACTIVE, 
from drawGraph import makeGraph
import numpy as np

SIMULATIONTIME = 60*4 # seconds

class Bar():
    def __init__(self) -> None:
        self.poisonDmg = 0
        self.bar = []
        self.usedAbility = np.array([],dtype=object)
        self.simt = stot(SIMULATIONTIME)#length of simulation in tick
        self.tc = 0
        self.adrenNow = INITADREN
        self.offGcdChanneled = 0
        self.tsunamiBoostOffCd = 0
        self.berserkOfftc = -1 #tc of until when berserk is active, set in flagBerserk()
        self.gchainBuff = NOTACTIVE
        self.gchainOfftc = -1 #tc of until when gchain effect is active

    def initArrays(self):
        self.y = self.barlen
        self.dmgP = np.zeros((self.y, self.simt))
        self.dmgS = np.zeros((self.y, self.simt))
        self.hitsP = np.zeros((self.y, self.simt))
        self.hitsS = np.zeros((self.y, self.simt))
        self.abilityOffCd = np.zeros(self.barlen)
        self.abilityAdrens = np.array([ability.req for ability in self.bar])
        self.abilityAdrenChange = np.array([ability.change for ability in self.bar])
        self.offGcdChanneledArray = np.array([ability.dur for ability in self.bar])
        self.abilityCd = np.array([ability.cd for ability in self.bar])

        if  STYLE == STYLEMAGIC:
            multiplier = SUNSHINEMULT
        elif STYLE == STYLERANGED:
            multiplier = DEATHSSWIFTNESSMULT
        else:
            multiplier = BERSERKMULT
        self.berserkMult = np.array([1 if ability.bleed else multiplier for ability in self.bar])

    def flagBerserk(self, ability):
        if ability.name == "Berserk" and STYLE == STYLEMELEE:
            self.berserkOfftc = self.tc + BERSERKDUR
        elif ability.name == "Sunshine" and STYLE == STYLEMAGIC:
            self.berserkOfftc = self.tc + SUNSHINEDUR
        elif ability.name == "Death's Swiftness" and STYLE == STYLERANGED:
            self.berserkOfftc = self.tc + DEATHSWIFTNESSDUR
    def flagGchain(self, ability):
        if ability.name == "Greater Chain":
            self.gchainBuff = ACTIVE
            self.gchainOfftc = self.tc + GCHAINBUFFDUR
    def getNextAbility(self):
        for i, ability in enumerate(self.bar):
            if (self.abilityOffCd.item(i) <= 0 and self.abilityAdrens.item(i) <= self.adrenNow and self.offGcdChanneled <= self.tc): #if ability i is available
                #set ability offcd
                self.abilityOffCd[i:i+1] = self.abilityCd[i]
                
                #set time when next ability can activate (offGcdChanneled)
                self.offGcdChanneled = self.tc + self.offGcdChanneledArray.item(i)

                #set next tick's adrenailine
                self.adrenNow = self.adrenNow + self.abilityAdrenChange.item(i)
                
                if (self.adrenNow > 100 + HEIGHTENEDSENSES * 10): #set to max adren if it was set to over max
                    self.adrenNow = 100 + HEIGHTENEDSENSES * 10
                
                #set flag if ability = berserk variant or gchain
                self.flagBerserk(ability)#flag self.berserkUlt if ability is berserk variant
                self.flagGchain(ability) #flag self.gchainBuff if ability is gchain

                #set usedAbility
                self.usedAbility = np.concatenate((self.usedAbility, np.full(int(self.offGcdChanneledArray.item(i)),ability)))
                return [ability, i]
        return [None, -1] #when no ability is available. 
        
    def checkGchain(self, ability):
        notApplicableToGchain = ["Magma Tempest", "Greater Chain"]# + self.otherAbsName
        if (self.gchainOfftc >= self.tc and self.gchainBuff == ACTIVE and ability.name not in notApplicableToGchain and np.sum(ability.pDmg)):#if not used yet
            self.gchainOfftc = 0
            self.gchainBuff = NOTACTIVE
            if (ability.name == "Corruption Blast"):
                return 1 #return multiplier of damage to s target
            else:
                return 0.5
        else:
            return 0
    def addArray(self, bigA, smallA, inde):
        if self.tc + smallA.shape[0] <= self.simt:
            bigA[inde][self.tc:self.tc + smallA.shape[0]] += smallA
        else:
            bigA[inde][self.tc:self.simt] += smallA[:self.simt - self.tc - smallA.shape[0]]
        return bigA
            
    def fillHits(self, ability, inde):#fill dmgP and dmgS caused by "ability" 
        if ability!= None:
            #add damage and hits to dmgP and hitsP
            self.dmgP = self.addArray(self.dmgP, ability.pDmg, inde)
            self.hitsP = self.addArray(self.hitsP, ability.hitsP, inde)
            #add gchainMult * dmgPrimary damage to dmgS
            gchainMult = self.checkGchain(ability)
            if gchainMult and ability.name == "Corruption Blast": #if ability is cblast
                gcCbDmg = ability.pDmg[:3]
                self.dmgS = self.addArray(self.dmgS, gcCbDmg, inde)#array with all elements set to 0 except the first hit's damage of cblast
                self.hitsS = self.addArray(self.hitsS, ability.hitsP*(AVERAGENENEMIES-1), inde)
            elif gchainMult:
                self.dmgS = self.addArray(self.dmgS, gchainMult*ability.pDmg, inde)
                self.hitsS = self.addArray(self.hitsS, ability.hitsP * min(2 + CAROMING,AVERAGENENEMIES - 1), inde)

            #add damage and hits to dmgS and hitsS
            if ability.nAOE:
                self.dmgS = self.addArray(self.dmgS, ability.sDmg, inde)
                self.hitsS = self.addArray(self.hitsS, ability.hitsS * min(ability.nAOE,AVERAGENENEMIES - 1), inde)

        if self.berserkOfftc >= self.tc:
            self.dmgP[:,self.tc] *= self.berserkMult
            self.dmgS[:,self.tc] *= self.berserkMult

    def simulate(self):
        self.barlen = len(self.bar)
        self.initArrays()
        while self.tc < self.simt:
            self.abilityOffCd -= 1
            nextAbility = self.getNextAbility() #returns ability
            self.fillHits(nextAbility[0], nextAbility[1]) #fill dmgP, dmgS, addHealArray()
            self.tc += 1

    
    def setDmgDitc(self):
        self.dmgPDict = [] #[{"ability1":damage, "ability2":damage,...},{(tick1)},{tick2},{tick3},...]
        self.dmgSDict = []
        for i in range(self.simt):
            self.dmgPDict.append({})
            self.dmgSDict.append({})
            for j, ability in enumerate(self.bar):# + self.otherAbs):
                pdmg = self.dmgP.item(j, i)
                sdmg = self.dmgS.item(j, i)
                name = ability.name
                if pdmg:
                    self.dmgPDict[i][name] = math.floor(pdmg)
                if sdmg:
                    self.dmgSDict[i][name] = math.floor(sdmg)
        #print(self.dmgPDict)
        #print(self.dmgSDict)

    def getDpsP(self):
        pHits = np.sum(self.hitsP)
        return math.floor((np.sum(self.dmgP) + (pHits + BLOODREAVER*(pHits + np.sum(self.hitsS)))*self.poisonDmg*(POISONPROCCHANCE+POISONPROCCHANCE**2+POISONPROCCHANCE**3))/ttos(self.simt))
    
    def getDpsS(self):
        return math.floor((np.sum(self.dmgS) + (np.sum(self.hitsS)/AVERAGENENEMIES)*self.poisonDmg*(POISONPROCCHANCE+POISONPROCCHANCE**2+POISONPROCCHANCE**3)/AVERAGENENEMIES)/ttos(self.simt))

    def showResutGraph(self):
        makeGraph.psCompare(self.dmgPDict, self.dmgSDict, list(self.usedAbility), self.bar)
        makeGraph.pDetail(self.dmgPDict, list(self.usedAbility), self.bar, self.getDpsP())# otherAbsP, self.getDpsP())
        makeGraph.sDetail(self.dmgSDict, list(self.usedAbility), self.bar, self.getDpsS())#otherAbsS, self.getDpsS())

"""
    def printSimulationResult(self):
        print("simulation time\t=", ttos(self.simt),"seconds")
        print()
        print("Primary dmg/s \t\t=",math.floor(self.dmgPTotal/ttos(self.simt)))
        print("Primary dmg/min \t=",math.floor(self.dmgPTotal*60/ttos(self.simt)))
        print("average time to kill primary enemy \t", math.floor(ENEMYHEALTH/(self.dmgPTotal/ttos(self.simt))))
        print("Total primary damage\t=",self.dmgPTotal)
        print()
        print("Secondary dmg/s \t=",math.floor(self.dmgSTotal/ttos(self.simt)))
        print("Secondary dmg/min \t=",math.floor(self.dmgSTotal*60/ttos(self.simt)))
        print("average time to kill secondary enemy \t", math.floor(ENEMYHEALTH/(self.dmgSTotal/ttos(self.simt))))
        print("Total secondary damage\t=",self.dmgSTotal)
        print()
    
    def takeDamage(self):
        damage = self.enemy.getAttack(self.tc)
        self.health -= damage
        #if(self.health<0):
            #print("you died at tick",self.tc)

    def heal(self): #individual heal, not total of soul split, vamp, etc
        #heal this tick
        if (self.health < MAXHEALTH):
            self.health = min(self.health + sum(self.healArray[self.tc]), MAXHEALTH)
            #healthbefore = self.health
            #print("tick",self.tc,"healed",self.health - healthbefore)
        #else:
            #print("tick",self.tc,"healed 0 becuase hp is full at", self.health)
    def addReaverDmg(self):#blood reaver passive damage
        if (self.tc >= 3 and BLOODREAVER):
            for h in self.healArray[self.tc - 3]: # apply hits 3 tick later, like ingame
                if (h != 0):
                    passiveDmg = math.floor(h/3)
                    self.totalDmgNoPoisonP += passiveDmg
                    if (self.otherAbility.bloodReaverPassive in self.dmgPrimary[self.tc]):#if self.otherAbility.bloodReaverPassive is already listed in dmgPrimary at same tick
                        self.dmgPrimary[self.tc][self.otherAbility.bloodReaverPassive].append(passiveDmg) #append
                    else: #other wise
                        self.dmgPrimary[self.tc][self.otherAbility.bloodReaverPassive] = [passiveDmg] #make new dictionary index
                    if (self.checkPoisonProc(self.otherAbility.bloodReaverPassive) and self.tc + 1 < self.simt):#add poison proc
                        #print(self.otherAbility.bloodReaverPassive.name,"at tick",self.tc,"activated poison")
                        self.simAbility[self.tc + 1].append(self.otherAbility.poisonP)
    def addHealArray(self, avdmg, ability, j):#add healing for 2 tick later
        if (self.health < MAXHEALTH and self.tc + j < self.simt and (not ability in self.otherAbs or ability in self.otherCanHeal)): 
            #print("tick",self.tc + j," : heal point from",ability.name,"added to healArray[",self.tc+j,"]", end=": ")
            if (SOULSPLIT):
                if (0 < avdmg <= 2000):
                    under2k = avdmg
                    between2k4k = 0
                    over4k = 0
                elif (2000 < avdmg and avdmg <= 4000):
                    under2k = 2000
                    between2k4k = avdmg - 2000
                    over4k = 0
                else:
                    under2k = 2000
                    between2k4k = 2000
                    over4k = avdmg - 4000
                healSoulsplit = (under2k*0.1 + between2k4k*0.05 + over4k*0.0125) * (1 + (0.1875 * AOS))
                healSoulsplit = math.floor(healSoulsplit)
                if (healSoulsplit > 0):
                    self.healArray[self.tc + j].append(healSoulsplit)
                    #print("soulsplit heal :",healSoulsplit,end=", ")
            if (VAMPAURA):
                healVampAura = math.floor(min(50, avdmg*0.05))
                #print("vamp aura heal :",healVampAura,end=",")
                self.healArray[self.tc + j].append(healVampAura)
            if (VAMPSCRIM == 1):
                healVampScrim = math.floor(min(200, avdmg*0.05))
                #print("vamp scrim heal :",healVampScrim, end=", ")
                self.healArray[self.tc + j].append(healVampScrim)
            if (VAMPSCRIM == 2):
                healSupVampScrim = math.floor(min(200, avdmg*0.0667))
                #print("sup vamp scrim heal :",healSupVampScrim, end="")
                self.healArray[self.tc + j].append(healSupVampScrim)
            #print()
    def checkPoisonProc(self, ability):
        if (not CINDERBANE):
            return NOTACTIVE
        p = POISONPROCCHANCE
        if (ability != self.otherAbility.poisonP and ability != self.otherAbility.poisonS):
            self.poisonProcAttempts += 1
        if (random.random() < p):
            return ACTIVE
        
    
    def roundDownHits(self,dmgPS):
        for i in range(len(dmgPS)):
            for index in dmgPS[i]:
                for j in range(len(dmgPS[i][index])):
                    dmgPS[i][index][j] = math.floor(dmgPS[i][index][j])

"""