import abilityDef as Ability
from playerInfo import DUALWIELD, PLANTEDFEET, WEAPONPOISON, CINDERBANE, KWUARMINCPOTENCY
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
        iLoc = "./ability_icons/magic/"#location of where the icon is stored
        #damage array meaning  [[[min damage, max damage]]  <- damage splat in a single tick]<-ability's damage each tick
        self.asphyx = Ability.thresh(name="Asphyxiate", cd=20, dur = 7*0.6, pDmg=[[[0,0]],[[37.6,188]],[[0,0]],[[37.6,188]],[[0,0]],[[37.6,188]],[[0,0]],[[37.6,188]]], icon=iLoc+"Asphixiate.png")
        self.deep_impact = Ability.thresh(name="Deep Impact", cd=15, pDmg=[[[0,0]],[[40,200]]], icon=iLoc+"Deep_Impact.png")
        self.dbreath = Ability.basic(name="Dragon Breath", cd=10, nAOE=4, pDmg=[[[0,0]],[[37.6,188]]], sDmg=[[[0,0]],[[37.6,188]]],icon=iLoc+"Dragon_Breath.png")
        self.gchain = Ability.basic(name="Greater Chain", cd=10, nAOE=2, pDmg=[[[0,0]],[[20,100]]], sDmg=[[[0,0]],[[20,100]]],icon=iLoc+"Greater_Chain.png")
        self.chain = Ability.basic(name="Chain", cd=10, nAOE=2, pDmg=[[[0,0]],[[20,100]]], sDmg=[[[0,0]],[[20,100]]])
        self.magma_tempest = Ability.basic(name="Magma Tempest", nAOE=24, cd=15, #check max hit (cant crit, so might not hit 19%?)
                        pDmg=[[[0,0]],[[0,0]],[[0,0]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]]], 
                        sDmg=[[[0,0]],[[0,0]],[[0,0]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]],[[0,0]],[[5,19]]],icon=iLoc+"Magma_Tempest.png")
        self.tsunami = Ability.ult(name="Tsunami", cd=60, req=40, change=-40, nAOE=8, pDmg=[[[0,0]],[[200,300]]], sDmg=[[[0,0]],[[200,300]]],icon=iLoc+"Tsunami.png")
        self.sunshine = Ability.ult(name="Sunshine", cd=60,icon=iLoc+"Sunshine.png", bleed=1)
        #TODO sunishine bleeds
        self.gconc = Ability.basic(name="Greater Concentrated Blast", cd=5, dur=4*0.6, pDmg=[[[0,0]], [[15.8,79]], [[17.8,89]], [[19.8, 99]]],icon=iLoc+"Greater_Conc.png")
        self.wrack = Ability.basic(name="Wrack", cd=3, pDmg=[[[0,0]],[[18.8,94]]],icon=iLoc+"Wrack.png")
        self.wrack_and_ruin = Ability.basic(name="Wrack and Ruin", cd=3, pDmg=[[[0,0]],[[60,300]]],icon=iLoc+"Wrack_And_Ruin.png")
        self.impact = Ability.basic(name="Imapct", cd=15, pDmg=[[[0,0]],[[20,100]]],icon=iLoc+"Impact.png")
        self.metamorph = Ability.ult(name="Metamorphosis",icon=iLoc+"Metamorphosis.png")
        self.tendril = Ability.thresh(name="Smoke Tendrils", cd=45, dur=7*0.6, pDmg=[[[0,0]],[[20,100]],[[0,0]],[[25,125]],[[0,0]],[[30,150]],[[0,0]],[[40,200]]],icon=iLoc+"Smoke_Tendril.png")
        #first hit delayed
        self.sonic_wave = Ability.basic(name="Sonic Wave", cd = 5,pDmg=[[[0,0]],[[0,0]],[[31.4,157]]],icon=iLoc+"Sonic_Wave.png")
        self.combust = Ability.basic(name="Combust", cd=15, bleed=1, pDmg=[[[0,0]],[[0,0]],[[20,37.6]],[[0,0]],[[20,37.6]],[[0,0]],[[20,37.6]],[[0,0]],[[20,37.6]],[[0,0]],[[20,37.6]]], icon=iLoc+"Combust.png")
        self.corruption_blast = Ability.basic(name="Corruption Blast", cd=15,bleed=1, nAOE=9999,pDmg=[[[0,0]],[[0,0]],[[33,100]],[[0,0]],[[26.7,80]],[[0,0]],[[20,60]],[[0,0]],[[13.3,40]],[[0,0]],[[6.7, 20]]],
                                                                            sDmg=[[[0,0]],[[0,0]],[[0,0]],[[0,0]],[[26.7,80]],[[0,0]],[[20,60]],[[0,0]],[[13.3,40]],[[0,0]],[[6.7, 20]]], icon=iLoc+"Corruption_Blast.png")
        self.omnipower_igneous = Ability.ult(name="Omnipower", cd=30, req=60, change=-60, pDmg=[[[0,0]], [[0,0]], [[0,0]],[[90,180]],[[0,0]],[[90,180],[90,180],[90,180]]],icon=iLoc+"Omnipower.png")
        
        if (DUALWIELD):#delayed if dual wield
            self.wild_magic = Ability.thresh(name="Wild Magic", cd=20, pDmg=[[[0,0]], [[0,0]], [[50,215]], [[50,215]]],icon=iLoc+"Wild_Magic.png")
        else:
            self.wild_magic = Ability.thresh(name="Wild Magic", cd=20, pDmg=[[[0,0]], [[50,215]], [[50,215]]],icon=iLoc+"Wild_Magic.png")

class Range:
    def __init__(self) -> None:
        self.death_swift = Ability.ult(name="Death's Swiftness", cd=60)

class Defence:
    def __init__(self):
        iLoc = "./ability_icons/defence/"
        self.devotion = Ability.thresh(name="Devotion", cd=30,icon=iLoc+"Devotion.png",pDmg=[[[0,0]]])
class Const:
    def __init__(self):
        iLoc = "./ability_icons/constitution/"
        self.tuska = Ability.basic(name="Tuska's Wrath", cd=15, pDmg=[[[0,0]],[[30,110]]],icon=iLoc+"Tuska's_Wrath.png")
        self.sacrifice = Ability.basic(name="Sacrifice", cd=30, pDmg=[[[0,0]],[[20,100]]],icon=iLoc+"Sacrifice.png")
class OtherAbility:
    def __init__(self):
        self.noAbility = Ability.other(name="(no ability available)", cd=0.6, dur = 0.6, change=0, pDmg=[[[0,0]]])
        
        poisonLV = WEAPONPOISON + CINDERBANE
        if (poisonLV == 0):
            poisonMin = 0
            poisonMax = 0
        elif(poisonLV > 0):
            poisonMin = 5 + poisonLV*2 + KWUARMINCPOTENCY*2.5 #=25% max +++,cinder
            poisonMax = 18 + poisonLV*6 + KWUARMINCPOTENCY*2.5 #=58% max +++,cinder
        self.poisonP = Ability.other(name="Poison", cd=0,dur=0,req=0,change=0,pDmg=[[[poisonMin,poisonMax]]],sDmg=[[]], bleed=1)
        self.poisonS = Ability.other(name="Poison", cd=0,dur=0,req=0,change=0,pDmg=[[]],sDmg=[[[poisonMin,poisonMax]]], bleed=1, nAOE=1)
        
        self.bloodReaverPassive = Ability.other(name="Blood Reaver Passive", cd=0,dur=0,req=0,pDmg=[[[1,1]]])