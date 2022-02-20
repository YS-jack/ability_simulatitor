import random
from timeConvert import stot
from playerInfo import *

def impatientBonous():
    p = 0.09 * IMPATIENT
    bonous = 0
    if (IMPATIENTGEARLV == 20):
        p *= 1.1
    if (random.random() < p):
        bonous = 3
    return bonous

def relentlessProc():
    p = 0.01 * RELENTLESS
    if (RELENTLESSGEARLV == 20):
        p *= 1.1
    if (random.random() < p):
        return 1
    else:
        return 0

class Ability:
    def __init__(self, name, cd, dur, req, change, bleed, nAOE, pDmg, sDmg,icon):
        self.name = name
        self.cd = stot(cd) #tick
        self.offcd = 0 #tick
        self.dur = stot(dur) #tick
        self.req = req
        self.change = change
        self.bleed = bleed
        self.nAOE = nAOE
        self.pDmg = pDmg
        self.sDmg = sDmg
        self.icon = icon
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
        if (self.name == "Chain" or self.name == "Greater Chain" or self.name == "Riccochet" or self.name == "Greater Riccochet"):
            self.nAOE = 2 + CAROMING
    def getAdren(self, tc, relentlessOffcd):
        if (FURYOFTHESMALL == 1):
            return self.change + 1 + impatientBonous()
        else:
            return self.change + impatientBonous()

class thresh(Ability):
    def __init__(self, name, cd = 20, dur = 1.8, req = 50, change = -15, bleed = 0, nAOE = 0, pDmg = [[[20,100]]], sDmg = [[]],icon="./ability_icons/magic/Wrack.png"):
        super().__init__(name, cd, dur, req, change, bleed, nAOE, pDmg, sDmg, icon)
    def getAdren(self, tc, relentlessOffcd):
        if (tc >= relentlessOffcd and relentlessProc()):
            return 0
        else:
            return self.change

class ult(Ability):
    def __init__(self, name, cd = 60, dur = 1.8, req = 100, change = -100, bleed = 0, nAOE = 0, pDmg = [[[0,0]]], sDmg = [[]],icon="./ability_icons/magic/Wrack.png"):
        super().__init__(name, cd, dur, req, change, bleed, nAOE, pDmg, sDmg, icon)
    def getAdren(self, tc, relentlessOffcd):
        if (tc >= relentlessOffcd and relentlessProc()):
            return 0
        else:
            return self.change