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
    def __init__(self, name, cd, dur, req, change, bleed, pDmg, sDmg):
        self.name = name
        self.cd = stot(cd) #tick
        self.offcd = 0 #tick
        self.dur = stot(dur) #tick
        self.req = req
        self.change = change
        self.bleed = bleed
        self.pDmg = pDmg
        self.sDmg = sDmg

#tc = tick cont (basicaly the time)
#cd = how long you have to wait till you can use the ability again
#dur = how long the ability lasts untill you can use another
#req = adren required to activate
#change = change in adren. 8 means 8 adren gained, -15 means use 15 adren
#bleed = 0 if not bleed damage, 1 if bleed damage

class basic(Ability):
    def __init__(self, name, cd = 10, dur = 1.8, req = 0, change = 8, bleed = 0, pDmg = [[[20,100]]], sDmg = [[[0,0]]]): 
        super().__init__(name, cd, dur, req, change, bleed, pDmg, sDmg)
    def getAdren(self, tc, relentlessOffcd):
        if (FURYOFTHESMALL == 1):
            return self.change + 1 + impatientBonous()
        else:
            return self.change + impatientBonous()

class thresh(Ability):
    def __init__(self, name, cd = 20, dur = 1.8, req = 50, change = -15, bleed = 0, pDmg = [[[20,100]]], sDmg = [[[0,0]]]):
        super().__init__(name, cd, dur, req, change, bleed, pDmg, sDmg)
    def getAdren(self, tc, relentlessOffcd):
        if (tc >= relentlessOffcd and relentlessProc()):
            return 0
        else:
            return self.change

class ult(Ability):
    def __init__(self, name, cd = 60, dur = 1.8, req = 100, change = -100, bleed = 0, pDmg = [[[0,0]]], sDmg = [[[0,0]]]):
        super().__init__(name, cd, dur, req, change, bleed, pDmg, sDmg)
    def getAdren(self, tc, relentlessOffcd):
        if (tc >= relentlessOffcd and relentlessProc()):
            return 0
        else:
            return self.change
