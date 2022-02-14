from allAbilities import Magic, Defence, Const
from timeConvert import stot

SIMULATIONTIME = 60 * 1 # seconds

class Bar:
    def __init__(self) -> None:
        magic = Magic()
        defence = Defence()
        const = Const()
        self.bar = [magic.sunshine, magic.gchain, magic.tsunami, magic.dbreath, 
        magic.magma_tempest, magic.wild_magic, magic.corruption_blast, defence.devotion, 
        magic.sonic_wave, const.tuska, const.sacrifice, magic.combust]

    def printBarInfo(self):
        for b in self.bar:
            print(self.bar.index(b), b.name,":")
            print("\tcd =", b.cd)
            print("\tduration =", b.dur)
            print("\trequired adrenaline =", b.req)
            print("\tadrenaline change =", b.change)

    def printSimulationResult(self):
        simTick = stot(SIMULATIONTIME)
        self.printSimulationAbility(simTick)
        self.printSimulationDamage(simTick)

    def printSimulationAbility(self, simt):
        print("print the order of abilities that are used for", simt, "ticks.")

    def printSimulationDamage(self, simt):
        print("print simulation result's damage in terms of primary target & secondary targets for", simt, "ticks.")

if __name__ == "__main__":
    tick_count = 0
    adrenaline = 100
    bar = Bar()
    bar.printBarInfo()
    bar.printSimulationResult()#input is sec