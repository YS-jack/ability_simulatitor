import abilityDef as Ability

class Magic:
    def __init__(self):
        self.asphyx = Ability.thresh(name="Asphyxiate", cd = 20, dur = 7*0.6)
        self.omnipower_igneous = Ability.ult(name="Omnipower", cd=30, req=60, change=-60)
        self.deep_impact = Ability.thresh(name="Deep Impact", cd=15)
        self.dbreath = Ability.basic(name="Dragon Breath", cd=10)
        self.sonic_wave = Ability.basic(name="Sonic Wave", cd = 5)
        self.combust = Ability.basic(name="Combust", cd=15)
        self.gchain = Ability.basic(name="Greater Chain", cd=10)
        self.wild_magic = Ability.thresh(name="Wild Magic", cd=20)
        self.magma_tempest = Ability.basic(name="Magma Tempest", cd=15)
        self.corruption_blast = Ability.basic(name="Corruption Blast", cd=15)
        self.tsunami = Ability.ult(name="Tsunami", cd=60, req=40)
        self.sunshine = Ability.ult(name="Sunshine", cd=60)
        self.gconc = Ability.basic(name="Greater Concentrated Blast", cd=5, dur=4*0.6)
        self.wrack = Ability.basic(name="Wrack", cd = 3)

class Defence:
    def __init__(self):
        self.devotion = Ability.thresh(name="Devotion", cd=30)

class Const:
    def __init__(self):
        self.tuska = Ability.basic(name="Tuska's Wrath", cd=15)
        self.sacrifice = Ability.basic(name="Sacrifice", cd=30)