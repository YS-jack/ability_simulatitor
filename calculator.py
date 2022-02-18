from operator import truediv
from pickle import FALSE, TRUE
from playerInfo import *
import numpy as np
import math
import random

class Damage():
    def __init__(self) -> None:
        self.magiclv = self.getBoostedLV(MAGICLV)
        self.rangelv = self.getBoostedLV(RANGEDLV)
        self.atklv = self.getBoostedLV(ATTACKLV)
        self.strlv = self.getBoostedLV(STRENGTHLV)
        self.deflv = self.getOvlBoostedLV(DEFENCELV) - self.getAuraLvReduction(DEFENCELV)
        self.abilityDmg = 0 #base ability damage!
        #get base damage
        if(STYLE == STYLEMAGIC):
            if(DUALWIELD):
                mhBaseDmg = 2.5*self.magiclv + min(9.6*MAGICMHTIER,MHSPELLDMG) + STRENGTHBONOUS
                ohBaseDmg = 1.25*self.magiclv + min(4.8*MAGICOHTIER,0.5*OHSPELLDMG) + 0.5*STRENGTHBONOUS
                self.abilityDmg = mhBaseDmg + ohBaseDmg
                print("mh =",mhBaseDmg,", oh =",ohBaseDmg," total =" ,self.abilityDmg)
            else:
                self.abilityDmg = 3.75*self.magiclv + min(14.4*MAGIC2HTIER,1.5*TWOHSPELLDMG) + 1.5*STRENGTHBONOUS
        elif(STYLE == STYLERANGED):
            if(DUALWIELD):
                mhBaseDmg = 2.5*self.rangelv + min(9.6*RANGEDMHTIER,AMMODMG) + STRENGTHBONOUS
                ohBaseDmg = 1.25*self.rangelv + min(4.8*RANGEDOHTIER,0.5*AMMODMG) + 0.5*STRENGTHBONOUS
                self.abilityDmg = mhBaseDmg + ohBaseDmg
            else:
                self.abilityDmg = 3.75*self.rangelv + min(14.4*RANGED2HTIER,1.5*AMMODMG) + 1.5*STRENGTHBONOUS
        elif(STYLE == STYLEMELEE):
            if(DUALWIELD):
                mhBaseDmg = 2.5*self.strlv + MELEEMHDMG*MELEESPEEDMH + STRENGTHBONOUS
                ohBaseDmg = 1.25*self.strlv + MELEEOHDMG*MELEESPEEDOH + 0.5*STRENGTHBONOUS
                self.abilityDmg = mhBaseDmg + ohBaseDmg
            else:
                self.abilityDmg = 3.75*self.strlv + MELEE2HDMG*MELEESPEED2H + 1.5*STRENGTHBONOUS
        print("ability damage =", self.abilityDmg)

    def getLVBoost(self):
        if (STYLE == STYLEMAGIC):
            return self.magiclv - MAGICLV
        if (STYLE == STYLERANGED):
            return self.rangelv - RANGEDLV
        if (STYLE == STYLEMELEE):
            return self.strlv - STRENGTHLV
    def getBoostedLV(self, lv):
        return self.getOvlBoostedLV(lv) + self.getAuraLvBoost(lv)
    def getOvlBoostedLV(self, lv):
        if(OVERLOADTYPE == OVLNM):
            newlv = math.floor(lv * 1.15) + 3
        elif(OVERLOADTYPE == OVLSPREME):
            newlv = math.floor(lv * 1.16) + 4
        elif(OVERLOADTYPE == OVLELDER):
            newlv = math.floor(lv * 1.17) + 5
        elif(OVERLOADTYPE == OVLNONE):
            newlv = lv
        return newlv
    def getAuraLvBoost(self, lv):
        return math.floor(BERSERKAURA * 0.1 * lv)
    def getAuraLvReduction(self, lv):
        return math.floor(BERSERKAURA * 0.15 * lv)
    def round(self, x):
        if (x == 0.05):
            return 0.1
        else:
            return np.round(x, decimals =2)
    def getCritChance(self):
        return BITING * 0.02 * (1 + math.floor(BITINGGEARLV/20)*0.1) + GRIMOIRE*0.12 + STALKERSRING*0.03 + REAVERSRING*0.05 + KALDEMON*0.01 + KALDEMONSCROLL*0.05
    def rollCritChance(self):
        p = self.getCritChance()
        if (random.random() < p):
            return TRUE
        else:
            return FALSE
    def getPrayerBoost(self):
        return 1 + PRAYERBOOST
    def getOtherBoost(self, berserkUlt):
        mult = (1 + RIPPERDEMON*0.025) * (1 + RUTHELESS*0.005*RUTHELESSSTACK) * (1 + MOBSALYER*0.07) * OTHERDMGMULTIPLIER
        if (not DUALWIELD and INQUISITOR):
            mult *= 1.125
        if (berserkUlt == BERSERK):
            mult *= 2
        elif (berserkUlt == SUNSHINE or berserkUlt == DEATHSSWIFTNESS):
            mult *= 1.5
        elif (berserkUlt == NOBERSERK):
            mult *= 1 + BERSERKAURA*0.1
        return mult
    def getAvDmg(self, min, max, ability, pOrS, berserkUlt):
        if(max == 0):
            return 0
        else:
            if (ability.name == "Dismember" or ability.name == "Combust" or ability.name == "Fragmentation Shot"):
                max += LUNGING * 4
                ave = self.round(min*min/max + (max-min)*(max+min)/(max*2))
                return ave *0.01* self.abilityDmg
            elif (ability.bleed == 1):
                ave = (min + max) / 2
                ave = self.round(ave)
                return ave *0.01* self.abilityDmg
            else:#non bleeds that perks apply
                #Precise perk
                min = min + PRECISE * 0.015 * max
                #equilibrium perk
                mMdiff = max - min
                min = mMdiff * 0.03 * EQUI + min
                max = max - mMdiff * 0.01 * EQUI
                ave = (min + max) / 2
                #print("ave after precise, equi",ave)
                #critical boosts
                critChance = self.getCritChance()
                aveCrit = max - (max - min) * 0.025
                ave = aveCrit*critChance + ave*(1-critChance)
                #print("ave after crit bonous",ave)
                #potion boost (4-8 with precise + equi)
                minpot = 4 * self.getLVBoost()
                maxpot = 8 * self.getLVBoost()
                minpot = minpot + PRECISE * 0.015 * maxpot
                mMdiff = maxpot - minpot
                minpot = mMdiff * 0.03 * EQUI + minpot
                maxpot = maxpot - mMdiff * 0.01 * EQUI
                avepot = (minpot + maxpot) / 2
                aveCritPot = maxpot - (maxpot - minpot) * 0.025
                avepot = aveCritPot*critChance + avepot*(1-critChance)
                #print("small damage increase from lv boosts = ", avepot)
                #prayer boost, other boost
                prayerMult = self.getPrayerBoost()
                #print("prayermult = ",prayerMult)
                otherMult = self.getOtherBoost(berserkUlt)
                #print("other mult =",otherMult)
                ave = ave * prayerMult * otherMult
                self.aveDmg = self.round(ave) * 0.01 * self.abilityDmg + avepot * otherMult
                #print("ave after prayer, other boosts = ", ave)
                #print()
                return self.aveDmg
    
    def caromingDmgMult(self):
        return min(1, (3 + CAROMING)/AVERAGENENEMIES)
    
    def aoeDmgMult(self, nSecTarget):
        return min(1, nSecTarget/(AVERAGENENEMIES - 1))