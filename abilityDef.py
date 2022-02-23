import numpy as np
from timeConvert import stot
from playerInfo import *
import itertools
from calculator import Damage
import math

def impatientBonous():
    p = 0.09 * IMPATIENT
    if (IMPATIENTGEARLV == 20):
        p *= 1.1
    return round(p * 3*LUCKYNESSMULT, 2)

def relentlessBonous(cd, change):
    p = 0.01 * RELENTLESS
    if (RELENTLESSGEARLV == 20):
        p *= 1.1
    return round(p * (-1)*change * (cd/RELENTLESSCD) * LUCKYNESSMULT,1)

def ultAdrenBonous():
    return 10 * (VIGOUR + CONSERVATIONOFENERGY)

class Ability:
    def __init__(self, name, cd, dur, req, change, bleed, nAOE, pDmg, sDmg,icon):
        self.name = name
        self.cd = stot(cd) #tick
        self.dur = stot(dur) #tick
        self.req = req
        self.change = change
        self.bleed = bleed
        self.nAOE = nAOE
        self.icon = icon

        dmgInst = Damage()
        self.pDmg = np.array([])
        self.sDmg = np.array([])
        self.hitsP = np.array([]) #hits against 1 enemy
        self.hitsS = np.array([])
        for hitInTick in pDmg:
            total  = 0
            count = 0
            for hit in hitInTick:
                dmg = dmgInst.getAvDmg(hit[0], hit[1], self.name, self.bleed)
                total += dmg
                if dmg: count += 1
            self.pDmg = np.append(self.pDmg,total)
            self.hitsP = np.append(self.hitsP, count)
        for hitInTick in sDmg:
            total  = 0
            count = 0
            for hit in hitInTick:
                dmg = dmgInst.getAvDmg(hit[0], hit[1], self.name, self.bleed)
                total += dmg
                if dmg: count += 1
            self.sDmg = np.append(self.sDmg,total)
            self.hitsS = np.append(self.hitsS, count)
        self.pDmg = np.round(self.pDmg, decimals=1)
        self.sDmg = np.round(self.sDmg, decimals=1)        

#tc = tick count (basicaly the time)
#cd = how long you have to wait till you can use the ability again
#dur = how long the ability lasts untill you can use another
#req = adren required to activate
#change = change in adren. 8 means 8 adren gained, -15 means use 15 adren
#bleed = 0 if not bleed damage, 1 if bleed damage
#nAOE = number of secondary targets. doesnt include primary (e.g. dbreath's naoe = 4 not 5)

class basic(Ability):
    def __init__(self, name, cd = 10, dur = 1.8, req = 0, change = 8, bleed = 0, nAOE = 0, pDmg = [[[20,100]]], sDmg = [[]],icon="./ability_icons/magic/Wrack.png"): 
        super().__init__(name, cd, dur, req, change, bleed, nAOE, pDmg, sDmg, icon)
        if self.name == "Chain" or self.name == "Greater Chain" or self.name == "Riccochet" or self.name == "Greater Riccochet":
            self.nAOE = 2 + CAROMING
        if self.nAOE:
            self.sDmg *= min(self.nAOE/(AVERAGENENEMIES-1), 1)
            self.sDmg = np.round(self.sDmg, decimals=1)
        self.change = round(change + impatientBonous(),1)
    


class thresh(Ability):
    def __init__(self, name, cd = 20, dur = 1.8, req = 50, change = -15, bleed = 0, nAOE = 0, pDmg = [[[20,100]]], sDmg = [[]],icon="./ability_icons/magic/Wrack.png"):
        super().__init__(name, cd, dur, req, change, bleed, nAOE, pDmg, sDmg, icon)
        self.change = round(change + relentlessBonous(cd,change),1)
        if(self.change > 0):
            self.change = 0

class ult(Ability):
    def __init__(self, name, cd = 60, dur = 1.8, req = 100, change = -100, bleed = 0, nAOE = 0, pDmg = [[]], sDmg = [[]],icon="./ability_icons/magic/Wrack.png"):
        super().__init__(name, cd, dur, req, change, bleed, nAOE, pDmg, sDmg, icon)
        self.change = round(change + relentlessBonous(cd,change) + ultAdrenBonous(),1)
        if(self.change > 0):
            self.change = 0

class other(Ability):
    def __init__(self, name, cd = 0, dur = 10, req = 0, change = 0, bleed = 0, nAOE = 0, pDmg = [[]], sDmg = [[]],icon="./ability_icons/magic/Wrack.png"): 
        super().__init__(name, cd, dur, req, change, bleed, nAOE, pDmg, sDmg, icon)