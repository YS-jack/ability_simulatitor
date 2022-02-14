import random
from timeConvert import stot
RELENTLESS = 5
RELENTLESSGEARLV = 20
IMPATIENT = 4
IMPATIENTGEARLV = 20
FURYOFTHESMALL = 1 # 0 if inactive, 1 if active

class impatient:
    def __init__(self):
        self.p = 0.09 * IMPATIENT
        self.bonous = 0
        if (IMPATIENTGEARLV == 20):
            self.p *= 1.1
        if (random.random() < self.p):
            self.bonous = 3
    def get_bonous(self):
        return self.bonous

class relentless:
    def __init__(self):
        self.offcd = 0 #tc (tick count) it will be available from
        self.p = 0.01 * RELENTLESS
        if (RELENTLESSGEARLV == 20):
            self.p *= 1.1
    
    def roll(self, tc):
        if (self.offcd <= tc):
            if (random.random() < self.p):
                self.offcd = tc + 50
                return 1
            else:
                return 0

class Ability:
    def __init__(self, name, cd, dur, req, change):
        self.name = name
        self.cd = stot(cd)
        self.offcd = 0
        self.dur = dur
        self.req = req
        self.change = change

#tc = tick cont (basicaly the time)
#cd = how long you have to wait till you can use the ability again
#dur = how long the ability lasts untill you can use another
#req = adren required to activate
#change = change in adren. 8 means 8 adren gained, -15 means use 15 adren

class basic(Ability):
    def __init__(self, name, cd = 10, dur = 1.8, req = 0, change = 8): 
        super().__init__(name, cd, dur, req, change)
        self.req = 0
        self.im = impatient()
        self.change = self.change + self.im.get_bonous()
        if (FURYOFTHESMALL == 1):
            self.change += 1

class thresh(Ability):
    def __init__(self, name, cd = 20, dur = 1.8, req = 50, change = -15):
        super().__init__(name, cd, dur, req, change)
        self.rel = relentless()
        
"""    if (self.rel.roll(self.tc)):
            self.change = 0"""
class ult(Ability):
    def __init__(self, name, cd = 60, dur = 1.8, req = 100, change = -100):
        super().__init__(name, cd, dur, req, change)
        self.rel = relentless()
        
"""if (self.rel.roll(self.tc)):
            self.change = 0"""