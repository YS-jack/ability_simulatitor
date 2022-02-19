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
    bar = Bar()
    
    bar.simulate()
    bar.printSimulationResult()
    bar.showResutGraph()
    
    """
    bar = [magic.sunshine, magic.gchain,magic.dbreath,magic.tsunami,
    magic.wild_magic,magic.corruption_blast,magic.deep_impact,magic.magma_tempest,
    magic.sonic_wave,defence.devotion, const.tuska, magic.combust]

    pool = [magic.sonic_wave, magic.gchain, magic.dbreath, magic.corruption_blast,
    magic.magma_tempest, magic.wild_magic, magic.deep_impact, magic.omnipower_igneous,
    magic.tsunami, magic.sunshine, const.tuska, magic.corruption_blast, defence.devotion]

    optimizer = Optimizer()
    optimizer.findBestAOE(pool)"""