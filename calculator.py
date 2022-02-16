from playerInfo import *

class Damage:
    def getAvDmg(min, max, ability):
        if (ability.name == "Dismember" or ability.name == "Combust" or ability.name == "Fragmentation Shot"):
            return (min + max) / 2
        elif (ability.bleed == 1):
            return (min + max) / 2
        else:
            return (min + max) / 2