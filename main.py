from bar import Bar
from allAbilities import *
from Optimise import Optimizer
if __name__ == "__main__":
    #bar.printBarInfo()
    attack = Attack()
    strength = Strength()
    magic = Magic()
    range = Range()
    defence = Defence()
    const = Const()
    """bar = Bar()
    bar.bar = [magic.sunshine, magic.gchain,magic.dbreath,magic.tsunami,
    magic.wild_magic,magic.corruption_blast,magic.deep_impact,magic.magma_tempest,
    magic.sonic_wave,defence.devotion, const.tuska, magic.combust]
    bar.simulate()
    bar.printSimulationResult()
    bar.showResutGraph()"""
    
    
    

    pool = [magic.corruption_blast,magic.dbreath,magic.sonic_wave, magic.gchain, magic.magma_tempest, const.tuska, magic.wrack]
    #print(pool)
    """, magic.wild_magic, magic.deep_impact, magic.omnipower_igneous,
    magic.tsunami, magic.sunshine"""

    optimizer = Optimizer()
    optimizer.findTopAOE(pool) #get top n bars