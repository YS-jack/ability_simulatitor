from playerInfo import *
class Enemy():
    def __init__(self) -> None:
        self.health = ENEMYHEALTH
        self.attackInterval = ENEMYATTACKINTERVAL
        self.aveDmg = ENEMYAVERAGEDMG
        self.atkCd = 0 #when it can do an attack (tick)
    
    def getAttack(self, tc):
        if (tc >= self.atkCd):
            self.atkCd = tc + self.attackInterval
            return self.aveDmg
        else:
            return 0