import abilityDef as Ability
from playerInfo import DUALWIELD, PLANTEDFEET
from timeConvert import stot

BERSERKDUR = 34 #duration of berserk (ticks)
SUNSHINEDUR = stot(30) + PLANTEDFEET * stot(7.8) #seconds
DEATHSWIFTNESSDUR = stot(30) + PLANTEDFEET * stot(7.8) #seconds
GCHAINBUFFDUR = 10 #ticks, duration of gchain effect

#TODO: auto attacks (natural + from non-damaging abilities), dark magic damage, aftershock damage, cannon, poison, biting, blood reaver(soul split), armour spike
class Attack:
    def __init__(self) -> None:
        pass

class Strength:
    def __init__(self) -> None:
        self.berserk = Ability.ult(name="Berserk", cd=60)

class Magic:
    def __init__(self):#cd = seconds
        #damage array meaning  [[[min damage, max damage]]  <- damage splat in a single tick]<-ability's damage each tick
        self.asphyx = Ability.thresh(name="Asphyxiate", cd=20, dur = 6*0.6, pDmg=[[[0,0]],[[37.6,188]],[[0,0]],[[37.6,188]],[[0,0]],[[37.6,188]],[[0,0]],[[37.6,188]]])
        self.deep_impact = Ability.thresh(name="Deep Impact", cd=15, pDmg=[[[0,0]],[[40,200]]])
        self.dbreath = Ability.basic(name="Dragon Breath", cd=10, nAOE=4, pDmg=[[[0,0]],[[37,188]]], sDmg=[[[0,0]],[[37,188]]])
        self.gchain = Ability.basic(name="Greater Chain", cd=10, nAOE=2, pDmg=[[[0,0]],[[20,100]]], sDmg=[[[0,0]],[[20,100]]])
        self.magma_tempest = Ability.basic(name="Magma Tempest", nAOE=24, cd=15, #check max hit (cant crit, so might not hit 19%?)
                        pDmg=[[[0,0]],[[0,0]],[[0,0]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]]], 
                        sDmg=[[[0,0]],[[0,0]],[[0,0]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]]])
        self.tsunami = Ability.ult(name="Tsunami", cd=60, req=40, change=-40, nAOE=8, pDmg=[[[0,0]],[[200,300]]], sDmg=[[[0,0]],[[200,300]]])
        self.sunshine = Ability.ult(name="Sunshine", cd=60)
        #TODO sunishine bleeds
        self.gconc = Ability.basic(name="Greater Concentrated Blast", cd=5, dur=4*0.6, pDmg=[[[0,0]], [[15.8,79]], [[17.8,89]], [[19.8, 99]]])
        self.wrack = Ability.basic(name="Wrack", cd=3, pDmg=[[[0,0]],[[18.8,94]]])
        self.wrack_and_ruin = Ability.basic(name="Wrack and Ruin", cd=3, pDmg=[[[0,0]],[[60,300]]])
        self.impact = Ability.basic(name="Imapct", cd=15, pDmg=[[[0,0]],[[20,100]]])
        self.metamorph = Ability.ult(name="Metamorphosis")
        self.tendril = Ability.thresh(name="Smoke Tendrils", cd=45, dur=7*0.6, pDmg=[[[0,0]],[[20,100]],[[0,0]],[[25,125]],[[0,0]],[[30,150]],[[0,0]],[[40,200]]])
        #first hit delayed
        self.sonic_wave = Ability.basic(name="Sonic Wave", cd = 5,pDmg=[[[0,0]],[[0,0]],[[31.4,157]]])
        self.combust = Ability.basic(name="Combust", cd=15, bleed=1, pDmg=[[[0,0]],[[0,0]],[[20,37.6]],[[0,0]],[[20,37.6]],[[0,0]],[[20,37.6]],[[0,0]],[[20,37.6]],[[0,0]],[[20,37.6]]])
        self.corruption_blast = Ability.basic(name="Corruption Blast", cd=15,bleed=1, nAOE=9999,pDmg=[[[0,0]],[[0,0]],[[33,100]],[[0,0]],[[26.7,80]],[[0,0]],[[20,60]],[[0,0]],[[13.3,40]],[[0,0]],[[6.7, 20]]],
                                                                            sDmg=[[[0,0]],[[0,0]],[[0,0]],[[0,0]],[[26.7,80]],[[0,0]],[[20,60]],[[0,0]],[[13.3,40]],[[0,0]],[[6.7, 20]]])
        self.omnipower_igneous = Ability.ult(name="Omnipower", cd=30, req=60, change=-60, pDmg=[[[0,0]], [[0,0]], [[0,0]],[[90,180]],[[0,0]],[[90,180],[90,180],[90,180]]])
        
        if (DUALWIELD):#delayed if dual wield
            self.wild_magic = Ability.thresh(name="Wild Magic", cd=20, pDmg=[[[0,0]], [[0,0]], [[50,215]], [[50,215]]])
        else:
            self.wild_magic = Ability.thresh(name="Wild Magic", cd=20, pDmg=[[[0,0]], [[50,215]], [[50,215]]])

class Range:
    def __init__(self) -> None:
        self.death_swift = Ability.ult(name="Death's Swiftness", cd=60)

class Defence:
    def __init__(self):
        self.devotion = Ability.thresh(name="Devotion", cd=30)
class Const:
    def __init__(self):
        self.tuska = Ability.basic(name="Tuska's Wrath", cd=15, pDmg=[[[0,0]],[[30,110]]])
        self.sacrifice = Ability.basic(name="Sacrifice", cd=30, pDmg=[[[0,0]],[[20,100]]])
class OtherAbility:
    def __init__(self):
        self.noAbility = Ability.basic(name="(no ability available)", cd=0.6, dur = 0.6, change=0, pDmg=[[[0,0]]])