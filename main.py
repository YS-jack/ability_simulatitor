


if __name__ == "__main__":
    from bar import Bar
    from allAbilities import *
    from Optimise import Optimizer

    import cProfile
    import pstats
    from datetime import datetime    
    bar = Bar()

    #simulate 1 bar (bar.bar)
    bar.bar = [bar.magic.sunshine, bar.magic.gchain, bar.magic.dbreath, bar.magic.tsunami,
    bar.magic.wild_magic, bar.magic.corruption_blast, bar.magic.deep_impact, bar.magic.magma_tempest,
    bar.magic.sonic_wave, bar.defence.devotion, bar.magic.combust, bar.magic.omnipower_igneous]

    with cProfile.Profile() as pr:
        bar.simulate()
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    now = datetime.now()
    filestring = "./profiles/" + now.strftime("%y-%m-%d  %H_%M ") + "12 abilities simulation"
    #stats.dump_stats(filename=filestring)

    #bar.printSimulationResult()
    #bar.showResutGraph()#"""



    #get optimal bar using abilities in pool[]
    #pool = [bar.magic.sunshine, bar.magic.corruption_blast, bar.magic.dbreath, bar.magic.sonic_wave, bar.magic.gchain, bar.magic.magma_tempest, const.tuska, bar.magic.wild_magic, bar.magic.deep_impact, bar.magic.omnipower_igneous, bar.magic.tsunami] 
    """pool = [bar.magic.sunshine, bar.magic.sonic_wave, bar.magic.corruption_blast, bar.magic.dbreath, bar.magic.gchain,
    bar.magic.magma_tempest, bar.const.tuska, bar.magic.wild_magic, bar.magic.deep_impact, bar.magic.tsunami] 
    
    # ,bar.const.sacrifice, bar.magic.omnipower_igneous

    optimizer = Optimizer()
    optimizer.findTopAOE(bar, pool, 50) #get top n bars"""


    