import abilityDef as ability

class magic:
    def __init__(self, tc):
        self.omnipower_igneous = ability.ult(tc, cd=30, req=60, change=-60)
        self.deep_impact = ability.thresh(tc,cd=15)
        self.dbreath = ability.basic(tc, cd=10)
        self.sonic_wave = ability.basic(tc, cd = 5)
        self.combust = ability.basic(tc, cd=15)
        self.gchain = ability.basic(tc, cd=10)
        self.wild_magic = ability.thresh(tc, cd=20)
        self.magma_tempest = ability.basic(tc, cd=15)
        self.corruption_blast = ability.basic(tc, cd=15)
        self.tsunami = ability.ult(tc,cd=60, req=40)
        self.sunshine = ability.ult(tc)

class defence:
    def __init__(self, tc):
        self.devotion = ability.thresh(tc, cd=30)

class const:
    def __init__(self, tc):
        self.tuska = ability.basic(tc, cd=15)
        self.sacrifice = ability.basic(tc, cd=30)