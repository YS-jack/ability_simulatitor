from playerInfo import *
import numpy as np
import math

class Damage():
    def __init__(self) -> None:
        self.magiclv = self.getOvlBoostedLV(MAGICLV)
        self.rangelv = self.getOvlBoostedLV(RANGEDLV)
        self.atklv = self.getOvlBoostedLV(ATTACKLV)
        self.strlv = self.getOvlBoostedLV(STRENGTHLV)
        self.deflv = self.getOvlBoostedLV(DEFENCELV)
        
        if(STYLE == STYLEMAGIC):
            if(DUALWIELD):
                mhBaseDmg = 2.5*self.magiclv + min(9.6*MAGICMHTIER,MHSPELLDMG) + STRENGTHBONOUS
                ohBaseDmg = 1.25*self.magiclv * min(4.8*MAGICOHTIER,0.5*OHSPELLDMG) + 0.5*STRENGTHBONOUS
                self.baseDmg = mhBaseDmg + ohBaseDmg
            else:
                self.baseDmg = 3.75*self.magiclv + min(14.4*MAGIC2HTIER,1.5*TWOHSPELLDMG) + 1.5*STRENGTHBONOUS
        elif(STYLE == STYLERANGED):
            if(DUALWIELD):
                mhBaseDmg = 2.5*self.rangelv + min(9.6*RANGEDMHTIER,AMMODMG) + STRENGTHBONOUS
                ohBaseDmg = 1.25*self.rangelv + min(4.8*RANGEDOHTIER,0.5*AMMODMG) * 0.5*STRENGTHBONOUS
                self.baseDmg = mhBaseDmg + ohBaseDmg
            else:
                self.baseDmg = 3.75*self.rangelv + min(14.4*RANGED2HTIER,1.5*AMMODMG) + 1.5*STRENGTHBONOUS
        elif(STYLE == STYLEMELEE):
            if(DUALWIELD):
                mhBaseDmg = 2.5*self.strlv + MELEEMHDMG*MELEESPEEDMH + STRENGTHBONOUS
                ohBaseDmg = 1.25*self.strlv + MELEEOHDMG*MELEESPEEDOH + 0.5*STRENGTHBONOUS
                self.baseDmg = mhBaseDmg + ohBaseDmg
            else:
                self.baseDmg = 3.75*self.strlv + MELEE2HDMG*MELEESPEED2H + 1.5*STRENGTHBONOUS
    
    def getOvlBoostedLV(self, lv):
        if(OVERLOADTYPE == OVLNM):
            newlv = math.floor(lv * 1.15) + 3
        elif(OVERLOADTYPE == OVLSPREME):
            newlv = math.floor(lv * 1.16) + 4
        elif(OVERLOADTYPE == OVLELDER):
            newlv = math.floor(lv * 1.17) + 5
        return newlv

    def round(self, x):
        if (x == 0.05):
            return 0.1
        else:
            return np.round(x, decimals =2)

    def getAvDmg(self, min, max, ability, pOrS, berserkUlt):
        if(max == 0):
            ave = 0
        else:
            if (ability.name == "Dismember" or ability.name == "Combust" or ability.name == "Fragmentation Shot"):
                max += LUNGING * 4
                ave = self.round(self, min*min/max + (max-min)*(max+min)/(max*2))
            elif (ability.bleed == 1):
                ave = (min + max) / 2
                ave = self.round(self, ave)
            else:#non bleeds that perks apply
                min = min + PRECISE * 0.015 * max
                mMdiff = max - min
                min = mMdiff * 0.03 * EQUI + min
                max = max - mMdiff * 0.01 * EQUI
                ave = (min + max) / 2
                critChance = BITING * 0.02 * (1 + math.floor(BITINGGEARLV/20)*0.1)+ GRIMOIRE*0.12 + STALKERSRING*0.03 + REAVERSRING*0.05 + KALDEMON*0.01 + KALDEMONSCROLL*0.05
                aveCrit = max - (max - min) * 0.025
                ave = aveCrit*critChance + ave*(1-critChance)
                ave = ave * (1 + RIPPERDEMON*0.025) * (1 + BERSERKAURA*0.1)
                ave =self.round(self, ave)
        return ave