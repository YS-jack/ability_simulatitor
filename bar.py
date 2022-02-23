import math
import random
from allAbilities import *
from timeConvert import stot, ttos
from playerInfo import *
import calculator
from drawGraph import makeGraph
import numpy as np
SIMULATIONTIME = 4*60 # seconds

class Bar():
    def __init__(self) -> None:
        self.atk = Attack()
        self.str = Strength()
        self.magic = Magic()
        self.range = Range()
        self.defence = Defence()
        self.const = Const()
        self.otherAbility = OtherAbility()
        #abilities that dont use gchain buff, dont impact adren, not displayed in result graph x axis icon TODO add aftershock and cannon, puncture, blood reaver .. in self.otherAbs
        self.otherAbs = [self.otherAbility.poisonP,self.otherAbility.poisonS,self.otherAbility.noAbility]#dont insert, only append
        self.otherAbsName = [self.otherAbility.poisonP.name, self.otherAbility.noAbility] #dont insert, only append
        
        self.bar = []
        self.usedAbility = np.array([],dtype=object)
        self.simt = stot(SIMULATIONTIME)#length of simulation in tick
        self.tc = 0
        self.adrenNow = INITADREN
        self.offGcdChanneled = 0

        self.berserkOfftc = -1 #tc of until when berserk is active, set in flagBerserk()
        self.damageInst = calculator.Damage()
        self.gchainBuff = NOTACTIVE
        self.gchainOfftc = -1 #tc of until when gchain effect is active

    def initArrays(self):
        self.y = self.barlen + len(self.otherAbs)
        self.dmgP = np.zeros((self.y, self.simt))
        self.dmgS = np.zeros((self.y, self.simt))
        self.hitsP = np.zeros((self.y, self.simt))
        self.hitsS = np.zeros((self.y, self.simt))
        self.abilityOffCd = np.zeros(self.barlen)
        
        self.abilityAdrens = np.array([])
        self.abilityAdrenChange = np.array([])
        self.offGcdChanneledArray = np.array([])
        for ability in self.bar:
            self.abilityAdrens = np.append(self.abilityAdrens, [ability.req])
            self.abilityAdrenChange = np.append(self.abilityAdrenChange, [ability.change])
            self.offGcdChanneledArray = np.append(self.offGcdChanneledArray, [ability.dur])

        self.abilityCd = np.array([])
        for ability in self.bar:
            self.abilityCd = np.concatenate((self.abilityCd,[ability.cd]))
        self.abilityCd = np.concatenate((self.abilityCd,np.zeros(len(self.otherAbs))))

        if  STYLE == STYLEMAGIC:
            multiplier = SUNSHINEMULT
        elif STYLE == STYLERANGED:
            multiplier = DEATHSSWIFTNESSMULT
        else:
            multiplier = BERSERKMULT
        for i, ability in enumerate(self.bar + self.otherAbs):
            if i == 0:
                if ability.bleed or type(ability) == OtherAbility:
                    self.berserkMult = np.array([[1]])
                else:
                    self.berserkMult = np.array([[multiplier]])
            else:
                if ability.bleed or type(ability) == OtherAbility:
                    self.berserkMult = np.append(self.berserkMult,[[1]],axis=0)
                else:
                    self.berserkMult = np.append(self.berserkMult,[[multiplier]],axis=0)

    def takeDamage(self):
        damage = self.enemy.getAttack(self.tc)
        self.health -= damage
        #if(self.health<0):
            #print("you died at tick",self.tc)

    def flagBerserk(self, ability):
        if ability.name == self.str.berserk.name and STYLE == STYLEMELEE:
            self.berserkOfftc = self.tc + BERSERKDUR
        elif ability.name == self.magic.sunshine.name and STYLE == STYLEMAGIC:
            self.berserkOfftc = self.tc + SUNSHINEDUR
        elif ability.name == self.range.death_swift.name and STYLE == STYLERANGED:
            self.berserkOfftc = self.tc + DEATHSWIFTNESSDUR
    def flagGchain(self, ability):
        if (ability.name == self.magic.gchain.name):
            self.gchainBuff = ACTIVE
            self.gchainOfftc = self.tc + GCHAINBUFFDUR
    def getNextAbility(self):
        self.abilityOffCd -= 1
        for i, ability in enumerate(self.bar):
            if (self.abilityOffCd.item(i) <= 0 and self.abilityAdrens.item(i) <= self.adrenNow and self.offGcdChanneled <= self.tc): #if ability i is available
                #set ability offcd
                self.abilityOffCd[i:i+1] = self.abilityCd[i] #set ability's + ability.cd
                
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
        return [self.otherAbility.noAbility, -1] #when no ability is available. 
        
    def checkGchain(self, ability):
        notApplicableToGchain = [self.magic.magma_tempest.name, self.magic.gchain.name] + self.otherAbsName
        if (self.gchainOfftc >= self.tc and self.gchainBuff == ACTIVE and ability.name not in notApplicableToGchain and np.sum(ability.pDmg)):#if not used yet
            self.gchainOfftc = 0
            self.gchainBuff = NOTACTIVE
            if (ability.name == self.magic.corruption_blast.name):
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
    def addPoison(self):
        if self.tc:
            nhitsP = np.sum(self.hitsP[:,self.tc-1])
            nhitsS = np.sum(self.hitsS[:,self.tc-1])
            
            poisonHitsP = math.floor((nhitsP+nhitsS)*POISONPROCCHANCE)
            poisonDmgP = poisonHitsP*self.otherAbility.poisonP.pDmg.item(0)
            
            self.hitsP[self.barlen,self.tc] = poisonHitsP
            self.dmgP[self.barlen,self.tc] = poisonDmgP
            
            poisonHitsS = math.floor(nhitsS*POISONPROCCHANCE)
            poisonDmgS = poisonHitsS*self.otherAbility.poisonS.sDmg.item(0)/AVERAGENENEMIES
            self.hitsS[self.barlen+1,self.tc] = poisonHitsS
            self.dmgS[self.barlen+1,self.tc] = poisonDmgS
            
    def fillHits(self, ability, inde):#fill dmgP and dmgS caused by "ability" 
        if ability.name != self.otherAbility.noAbility.name:
            #add damage and hits to dmgP and hitsP
            self.dmgP = self.addArray(self.dmgP, ability.pDmg, inde)
            self.hitsP = self.addArray(self.hitsP, ability.hitsP, inde)
            #add gchainMult * dmgPrimary damage to dmgS
            gchainMult = self.checkGchain(ability)
            if gchainMult and ability.name == self.magic.corruption_blast.name: #if ability is cblast
                gcCbDmg = ability.pDmg[:3]
                self.dmgS = self.addArray(self.dmgS, gcCbDmg, inde)#array with all elements set to 0 except the first hit's damage of cblast
                self.hitsS = self.addArray(self.hitsS, ability.hitsP*(AVERAGENENEMIES-1), inde)
            elif gchainMult:
                self.dmgS = self.addArray(self.dmgS, gchainMult*ability.pDmg, inde)
                self.hitsS = self.addArray(self.hitsS, ability.hitsP * min(self.magic.gchain.nAOE,AVERAGENENEMIES - 1), inde)

            #add damage and hits to dmgS and hitsS
            if ability.nAOE:
                self.dmgS = self.addArray(self.dmgS, ability.sDmg, inde)
                self.hitsS = self.addArray(self.hitsS, ability.hitsS * min(ability.nAOE,AVERAGENENEMIES - 1), inde)
        
        if self.berserkOfftc >= self.tc:
            self.dmgP[:,self.tc] *= BERSERKMULT
            self.dmgS[:,self.tc] *= BERSERKMULT

        self.addPoison()
        #damage cap
        #heal
        #reaver
        #add expected posion hits (no more rolling random)
        #add to self.dmgPTotal, self.dmgSTotal, including poison
        
    def simulate(self):
        self.barlen = len(self.bar)
        self.initArrays()
        while self.tc < self.simt:
            #self.takeDamage()
            nextAbility = self.getNextAbility() #returns ability
            self.fillHits(nextAbility[0], nextAbility[1]) #fill dmgP, dmgS, addHealArray()
            #self.heal()#heal
            #self.addReaverDmg()# apply damage of blood reaver passive
            self.tc += 1

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
    
    def setDmgDitc(self):
        self.dmgPDict = [] #[{"ability1":damage, "ability2":damage,...},{(tick1)},{tick2},{tick3},...]
        self.dmgSDict = []
        for i in range(self.simt):
            self.dmgPDict.append({})
            self.dmgSDict.append({})
            for j, ability in enumerate(self.bar + self.otherAbs):
                pdmg = self.dmgP.item(j, i)
                sdmg = self.dmgS.item(j, i)
                name = ability.name
                if pdmg:
                    self.dmgPDict[i][name] = math.floor(pdmg)
                if sdmg:
                    self.dmgSDict[i][name] = math.floor(sdmg)
        #print(self.dmgPDict)
        #print(self.dmgSDict)

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

    def getDpsP(self):
        return math.floor(np.sum(self.dmgP)/ttos(self.simt))
    def getDpsS(self):
        return math.floor(np.sum(self.dmgS/ttos(self.simt)))

    def getExpectedDpsP(self):
        return math.floor((self.totalDmgNoPoisonP + self.poisonProcAttempts * (self.otherAbility.poisonP.pDmg[0][0][0] + self.otherAbility.poisonP.pDmg[0][0][1]) * self.damageInst.abilityDmg * 0.01 / 2)/ttos(self.simt)*POISONPROCCHANCE)
    def getExpectedDpsS(self):
        return math.floor((self.totalDmgNoPoisonS + self.poisonProcAttempts * (self.otherAbility.poisonS.sDmg[0][0][0] + self.otherAbility.poisonS.sDmg[0][0][1]) * self.damageInst.abilityDmg * 0.01 / 2)/ttos(self.simt)*POISONPROCCHANCE)
    
    def showResutGraph(self):
        makeGraph.psCompare(self.dmgPDict, self.dmgSDict, list(self.usedAbility), self.bar)
        otherAbsP = self.otherAbs[0:1] + self.otherAbs[2:]
        otherAbsS = self.otherAbs[1:]
        makeGraph.pDetail(self.dmgPDict, list(self.usedAbility), self.bar, otherAbsP, self.getDpsP())
        makeGraph.sDetail(self.dmgSDict, list(self.usedAbility), self.bar, otherAbsS, self.getDpsS())