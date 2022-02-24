if __name__ == "__main__":
    from bar import Bar
    from allAbilities import *
    from Optimise import Optimizer

    import cProfile
    import pstats
    from datetime import datetime    
    magic = Magic()
    other = OtherAbility()
    bar = Bar()
    bar.poisonDmg = other.poisonP.hitsP.item(0)
    #simulate 1 bar (bar.bar)
    """bar.bar = [bar.magic.gchain,bar.magic.corruption_blast, bar.magic.dbreath, bar.magic.magma_tempest,  bar.magic.sunshine, bar.magic.tsunami,
    bar.magic.wild_magic,  bar.magic.deep_impact, 
    bar.magic.sonic_wave, bar.const.tuska, bar.magic.combust, bar.magic.omnipower_igneous]

    
    bar.simulate()
    
    #bar.printSimulationResult()
    bar.setDmgDitc()
    bar.showResutGraph()#"""

    #get optimal bar using abilities in pool[]
    #pool = [bar.magic.sunshine, bar.magic.corruption_blast, bar.magic.dbreath, bar.magic.sonic_wave, bar.magic.gchain, bar.magic.magma_tempest, const.tuska, bar.magic.wild_magic, bar.magic.deep_impact, bar.magic.omnipower_igneous, bar.magic.tsunami] 
    pool = [
        magic.sunshine, magic.sonic_wave, magic.corruption_blast, 
        magic.dbreath, magic.gchain, magic.magma_tempest]
    """
        bar.const.tuska, bar.magic.wild_magic, bar.magic.deep_impact, 
        bar.magic.tsunami, bar.magic.omnipower_igneous, bar.magic.corruption_blast] """
    
    
    optimizer = Optimizer()
    with cProfile.Profile() as pr:
        bestBar = optimizer.findTopAOE(bar, pool,5) #get top n bars"""

    #optimizer.printBestBarInfo(bar, bestBar)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    now = datetime.now()
    filestring = "./profiles/" + now.strftime("%y-%m-%d  %H_%M ") + "6 abilities 5min optimisation"
    stats.dump_stats(filename=filestring) 