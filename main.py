from typing_extensions import Self
import random

RELENTLESS = 5
RELENTLESSGEARLV = 20
IMPATIENT = 4
IMPATIENTGEARLV = 20
FURYOFTHESMALL = 1

def stot(sec):
    if (sec == 3):
        return 5
    if (sec == 5):
        return 9
    if (sec == 10):
        return 17
    if (sec == 15):
        return 25
    if (sec == 20):
        return 34
    if (sec == 24):
        return 41
    if (sec == 30):
        return 50
    if (sec == 45):
        return 75
    if (sec == 60):
        return 100
    if (sec == 90):
        return 150
    if (sec == 120):
        return 200
    if (sec == 300):
        return 500

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
        self.offcd = 0 #tick_count it will be available from
        self.p = 0.01 * RELENTLESS
        if (RELENTLESSGEARLV == 20):
            self.p *= 1.1
    
    def roll(self):
        if (self.offcd <= tick_count):
            if (random.random() < self.p):
                self.offcd = tick_count + 50
                return 1
            else:
                return 0

class ability:
    def __init__(self, cd, dur, req, change):
        self.cd = cd
        self.offcd = 0
        self.dur = dur
        self.req = req
        self.change = change

class basic(ability):
    def __init__(self, cd, dur = 3, req = 0, change = 8):
        super().__init__(cd, dur, req, change)
        self.req = 0
        self.im = impatient()
        self.change = self.change + self.im.get_bonous()
        if (FURYOFTHESMALL == 1):
            self.change += 1
class thresh(ability):
    def __init__(self, cd, dur = 3, req = 50, change = -15):
        super().__init__(cd, dur, req, change)
        self.req = 50
        self.rel = relentless()
        if (self.rel.roll()):
            self.change = 0
class ult(ability):
    def __init__(self, cd = stot(60), dur = 3, req = 100, change = -100):
        super().__init__(cd, dur, req, change)
        self.req = 100
        self.rel = relentless()
        if (self.rel.roll()):
            self.change = 0

if __name__ == "__main__":
    tick_count = 0
    adrenaline = 100
    sunshine = ult()
    magma_tempest = basic(25)
    gchain = basic(17)
    dragon_breath = basic(17)
    queue = [