import math
import random
from pickle import TRUE
from xml.dom.minidom import Notation
from allAbilities import *
from timeConvert import stot, ttos
from playerInfo import *
import calculator
from drawGraph import makeGraph
from enemy import Enemy
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
        self.otherAbs = [#abilities that dont use gchain buff, not displayed in result graph x axis icon TODO add aftershock and cannon, puncture, blood reaver .. here
            self.otherAbility.poisonP,self.otherAbility.poisonS,self.otherAbility.noAbility, self.otherAbility.bloodReaverPassive] 
        self.otherCanHeal = [] #abilities in self.othersAbs but can heal from soulsplit, vamp e.g. reflect damage, cannon(?) wen,jas book(?)
        """self.bar = [self.magic.sunshine, self.magic.gchain,self.magic.dbreath,self.magic.tsunami, self.magic.wild_magic, 
        self.magic.sonic_wave, self.magic.corruption_blast, self.magic.magma_tempest, self.magic.deep_impact, 
        self.defence.devotion, self.const.tuska, self.magic.combust, self.const.sacrifice, self.magic.omnipower_igneous]"""
        """self.bar = [self.magic.wild_magic,self.magic.gchain,self.magic.sunshine, self.magic.tsunami,self.magic.dbreath,
        self.magic.corruption_blast,self.magic.deep_impact,self.magic.magma_tempest,
        self.magic.sonic_wave,self.defence.devotion, self.const.tuska, self.magic.combust, self.const.sacrifice, self.magic.wrack]"""
        self.bar =[]
        
        self.simt = stot(SIMULATIONTIME)#length of simulation in tick
        self.tc = 0
        self.abilityCd = 0
        self.adren = [0]*self.simt
        self.adren[0] = INITADREN
        self.simAbility = [] #[[ability, ability (activated in same tick, like poison, aftershock, puncture, ...)],[],[],...]       
        self.dmgPrimary = [] #[{"ability1":damage, "ability2":damage,...},{},...]
        self.dmgSecondary = []
        self.healArray = []
        for i in range(self.simt):
            self.simAbility.append([])
            self.dmgPrimary.append({})
            self.dmgSecondary.append({})
            self.healArray.append([])
        
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
        self.health = MAXHEALTH
        self.enemy = Enemy()

        self.poisonProcAttempts = 0
        self.totalDmgNoPoisonP = 0
        self.totalDmgNoPoisonS = 0
        
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
        notApplicableToGchain = [self.magic.magma_tempest, self.magic.gchain] + self.otherAbs
        if (self.gchainOfftc >= self.tc and self.gchainBuff == ACTIVE and ability not in notApplicableToGchain):#if not used yet
            self.gchainOfftc = 0
            self.gchainBuff = NOTACTIVE
            if (ability == self.magic.corruption_blast):
                return 1 #return multiplier of damage
            else:
                return 0.5
        else:
            return 0
    def heal(self): #individual heal, not total of soul split, vamp, etc
        #heal this tick
        if (self.health < MAXHEALTH):
            healthbefore = self.health
            self.health = min(self.health + sum(self.healArray[self.tc]), MAXHEALTH)
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
    def takeDamage(self):
        damage = self.enemy.getAttack(self.tc)
        self.health -= damage
        #if(self.health<0):
            #print("you died at tick",self.tc)
    def getNextAbility(self):
            if (self.tc == 0):
                currentAdren = INITADREN
            else:
                currentAdren = self.adren[self.tc - 1]
            if (self.abilityCd > self.tc): #during gcd or still doing channeled
                #print("in getNextAbility: no ability returned becuase self.abilityCd >", self.tc)
                return self.otherAbility.noAbility
            for ability in self.bar:
                #print("in getNextAbility:", ability.name, "offcd =",ability.offcd,", tick =",self.tc,", currnetAdren =",currentAdren,", requried adren =",ability.req)
                if (self.tc >= ability.offcd and currentAdren >= ability.req):
                    self.flagBerserk(ability)#flag self.berserkUlt if ability is berserk variant
                    self.flagGchain(ability) #flag self.gchainBuff if ability is gchain
                    #print("in getNextAbility: returned", ability.name,"tick:",self.tc)
                    return ability
            #print("no ability was available at tick",self.tc,"for bar ",end="")
            #print("[",end="")
            #for ability in self.bar:
            #    print(ability.name,end=", ")
            #print("]")
            #print("in getNextAbility: no ability was available at tick",self.tc)
            return self.otherAbility.noAbility #when no ability is available. TODO: replace with auto attack if its not on cd
    def addSimAbility(self, ability):
        if (len(self.simAbility[self.tc]) < self.simt and ability != self.otherAbility.noAbility):
            self.simAbility[self.tc].insert(0,ability)

    def fillHits(self, pOrS):#fill hitP and hitS caused by "ability" input, including hits > self.tc, 
        if (len(self.simAbility[self.tc]) == 0):
            #print("fillHits: no ability was in self.simAbility[",self.tc,"]")
            return 0
        for ability in self.simAbility[self.tc]:
            self.checkBerserk()
            if (pOrS == "p"):
                if(ability != self.magic.corruption_blast):#for gchain maths
                    gchainmult = self.checkGchain(ability)
                for i in range(len(ability.pDmg)):#for every tick ability lasts for
                    if (i + self.tc >= self.simt):
                        break
                    tickHits = ability.pDmg[i] #tickHits is list of damage done by 1 ability in 1 tick (e.g. omnipower 2nd-4th hits)
                    for j in range(len(tickHits)):#for every hits ability does in a tick
                        mini = ability.pDmg[i][j][0]
                        maxi = ability.pDmg[i][j][1]
                        avDmg = self.damageInst.getAvDmg(mini, maxi, ability, pOrS, self.berserkUlt) #get average damage of 1 hit of tickHits
                        if (avDmg > self.damageCap):#consider damage cap
                            avDmg = self.damageCap
                        #print("tick",self.tc,"damage from",ability.name,"'s",i,"th hit at tick",self.tc+i," =",avDmg)
                        
                        if (avDmg > 0):
                            self.dmgPTotal += avDmg #add to damage count
                            if (ability != self.otherAbility.poisonP):
                                self.totalDmgNoPoisonP += avDmg
                            if (ability in self.dmgPrimary[i + self.tc]):#if ability is already listed in dmgPrimary at same tick
                                self.dmgPrimary[i + self.tc][ability].append(avDmg) #append
                            else: #other wise
                                self.dmgPrimary[i + self.tc][ability] = [avDmg] #make new dictionary index
                            #process for gchain damage caluclation on secondary targets
                            if (ability == self.magic.corruption_blast):
                                gchainmult = self.checkGchain(ability)
                            if (gchainmult):#add damage to secondary targets if gchain buff is active
                                self.totalDmgNoPoisonS += avDmg*self.damageInst.caromingDmgMult()*gchainmult
                                self.dmgSTotal += avDmg*self.damageInst.caromingDmgMult()*gchainmult
                                if (ability in self.dmgSecondary[i + self.tc]):
                                    self.dmgSecondary[i + self.tc][ability].append(avDmg*self.damageInst.caromingDmgMult()*gchainmult)
                                else:
                                    self.dmgSecondary[i + self.tc][ability] = [avDmg*self.damageInst.caromingDmgMult()*gchainmult]
                            #check poison proc, append to self.simAbility
                            if (self.checkPoisonProc(ability) and self.tc + i + 1< self.simt):
                                #print(ability.name,"at tick",self.tc,"activated poison")
                                self.simAbility[self.tc + i + 1].append(self.otherAbility.poisonP)
                            #add healing to self.healArray[]
                            self.addHealArray(avDmg ,ability, i)

            elif(pOrS == "s"):
                for i in range(len(ability.sDmg)):
                    if (i + self.tc >= self.simt):
                        break
                    tickHits = ability.sDmg[i]
                    for j in range(len(tickHits)):
                        mini2 = ability.sDmg[i][j][0]
                        maxi2 = ability.sDmg[i][j][1]
                        avDmg = self.damageInst.getAvDmg(mini2, maxi2, ability, pOrS, self.berserkUlt)
                        if (avDmg > self.damageCap):#consider damage cap
                            avDmg = self.damageCap
                        if (ability.name != "Poison"):#dont decrease damage when its poison hit (its a single target damage)
                            avDmg *= self.damageInst.aoeDmgMult(ability.nAOE)
                        
                        if (avDmg > 0):
                            self.dmgSTotal += avDmg
                            if (ability != self.otherAbility.poisonS):
                                self.totalDmgNoPoisonS += avDmg
                            if (ability in self.dmgSecondary[i + self.tc]):
                                self.dmgSecondary[i + self.tc][ability].append(avDmg)
                            else:
                                self.dmgSecondary[i + self.tc][ability] = [avDmg]
                            #check poison proc, add to simAbility[self.tc + 1]
                            if (self.checkPoisonProc(ability) and self.tc + i + 1 < self.simt):
                                #print(ability.name,"at tick",self.tc,"activated poison")
                                self.simAbility[self.tc + i + 1].append(self.otherAbility.poisonS)
                            #add healing to self.healArray[], add damage of bloodreaver to later tick, * number of enemies or nAOE
                            for k in range(min(ability.nAOE,math.floor(AVERAGENENEMIES - 1))):
                                self.addHealArray(avDmg, ability, i)

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
                    #if (self.adren[t] < 0):
                        #print("adrenaline below 0 after using",ability.name)
                    if (self.adren[t] >= 100 + HEIGHTENEDSENSES * 10):
                        self.adren[t] = 100 + HEIGHTENEDSENSES * 10
    def setcd(self, ability):
        if (ability != self.otherAbility.noAbility):
            ability.offcd = self.tc + ability.cd
            self.abilityCd = self.tc + ability.dur
    def roundDownHits(self,dmgPS):
        for i in range(len(dmgPS)):
            for index in dmgPS[i]:
                for j in range(len(dmgPS[i][index])):
                    dmgPS[i][index][j] = math.floor(dmgPS[i][index][j])

    def simulate(self):
        """print("start simulation of bar :",end="")
        for ab in self.bar:
            print(ab.name,end=", ")
        print()"""
        while self.tc < self.simt:
            self.takeDamage()
            nextAbility = self.getNextAbility() #check what ability would be used at tick self.tc, type(nextAbility) same as type(self.bar[i])
            self.addSimAbility(nextAbility) #edit simAbility
            #print("filling primary hits")
            self.fillHits("p") #fill dmgPriamry[{}], addHealArray()
            #print("filling secondary hits")
            self.fillHits("s") #dmgSecondary[{}], addHealArray()
            self.heal()#heal
            self.addReaverDmg()# apply damage of blood reaver passive
            self.renewAdren(nextAbility) #calc adren, edit adren[]
            self.setcd(nextAbility)
            self.tc += 1
        self.roundDownHits(self.dmgPrimary)
        self.roundDownHits(self.dmgSecondary)

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
        print("[",end="")
        for ability in self.bar:
            print(ability.name,end=", ")
        print("]",end="\n\n\n\n\n")
        """for i in range(self.simt):
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
                print("ability activated:", self.simAbility[i][j].name,"at tick",i)"""
    def getDpsP(self):
        return math.floor(self.dmgPTotal/ttos(self.simt))
    def getDpsS(self):
        return math.floor(self.dmgSTotal/ttos(self.simt))

    def getExpectedDpsP(self):
        return math.floor((self.totalDmgNoPoisonP + self.poisonProcAttempts * (self.otherAbility.poisonP.pDmg[0][0][0] + self.otherAbility.poisonP.pDmg[0][0][1]) * self.damageInst.abilityDmg * 0.01 / 2)/ttos(self.simt)*POISONPROCCHANCE)
    def getExpectedDpsS(self):
        return math.floor((self.totalDmgNoPoisonS + self.poisonProcAttempts * (self.otherAbility.poisonS.sDmg[0][0][0] + self.otherAbility.poisonS.sDmg[0][0][1]) * self.damageInst.abilityDmg * 0.01 / 2)/ttos(self.simt)*POISONPROCCHANCE)
    
    def showResutGraph(self):
        #makeGraph.psCompare(self.dmgPrimary,self.dmgSecondary, self.simAbility, self.bar)
        #makeGraph.pDetail(self.dmgPrimary, self.simAbility, self.bar, self.otherAbs, self.getDpsP())
        makeGraph.sDetail(self.dmgSecondary, self.simAbility, self.bar, self.otherAbs, self.getDpsS())