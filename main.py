from bar import SIMULATIONTIME
from Optimise import NPC
if __name__ == "__main__":
    from bar import Bar
    from allAbilities import *
    from Optimise import Optimizer

    import cProfile
    import pstats
    from datetime import datetime    
    magic = Magic()
    const = Const()
    other = OtherAbility()
    bar = Bar()
    bar.poisonDmg = other.poisonP.hitsP.item(0)
    #simulate 1 bar (bar.bar)
    bar.bar = [magic.gchain, magic.combust, magic.omnipower_igneous,magic.corruption_blast, magic.dbreath, magic.magma_tempest, magic.sonic_wave, magic.tsunami,
    magic.wild_magic, magic.sunshine,  magic.deep_impact, 
    const.tuska, ]
    
    bar.simulate()

    bar.setDmgDitc()
    bar.showResutGraph()#"""

    #get optimal bar using abilities in pool[]
    #pool = [bar.magic.sunshine, bar.magic.corruption_blast, bar.magic.dbreath, bar.magic.sonic_wave, bar.magic.gchain, bar.magic.magma_tempest, const.tuska, bar.magic.wild_magic, bar.magic.deep_impact, bar.magic.omnipower_igneous, bar.magic.tsunami] 
    """pool = [
        magic.sunshine, magic.sonic_wave, magic.corruption_blast, 
        magic.dbreath, magic.gchain, magic.magma_tempest, 
        magic.wild_magic, magic.tsunami, magic.deep_impact,
         magic.combust]
    magic.omnipower_igneous
          
          const.tuska, ] """
    
    
    """optimizer = Optimizer()
    with cProfile.Profile() as pr:
        bestBar = optimizer.findTopAOE(bar, pool,10) #get top n bars

    optimizer.printBestBarInfo(bar, bestBar)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    now = datetime.now()
    filestring = "./profiles/" + now.strftime("%y-%m-%d  %H_%M_%S ") + " " + str(NPC) + " processes " + str(len(pool)) + " abilities " + str(SIMULATIONTIME) +"sec optimisation"
    stats.dump_stats(filename=filestring) #"""