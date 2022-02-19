#player stat, armour
ACCURACY = 4360
STRENGTHBONOUS = 199.2 #for all 3 combat styles
MAXHEALTH = 9900
AOS = 1 #1 if wearing amulet of souls or essence of finallity amulet
INQUISITOR = 0 #1 if using inquisitor/hexhunter/omen
DUALWIELD = 0 #0 if 2h weapon, 1 if dual wield
STYLEMAGIC = 1
STYLERANGED = 2
STYLEMELEE = 3
STYLE = STYLEMAGIC #1 = magic, 2 = ranged, 3 = melee

#magic wp, spells
MAGICMHTIER = 90
MAGICOHTIER = 90
MAGIC2HTIER = 95
MHSPELLDMG = 950.4
OHSPELLDMG = 950.4
TWOHSPELLDMG = 950.4

#ranged wp, ammo
RANGEDMHTIER = 90
RANGEDOHTIER = 90
RANGED2HTIER = 92
AMMODMG = 900

#melee wp,wp speed
MELEEMHDMG = 100
MELEEOHDMG = 100
MELEE2HDMG = 200
MELEESPEEDMH = 1 #0.644 if average, 0.783 if fast, 1 if fastest
MELEESPEEDOH = 1
MELEESPEED2H = 0.644

#player level
ATTACKLV = 99
STRENGTHLV = 99
RANGEDLV = 99
MAGICLV = 99
DEFENCELV = 99
SMITHINGLV = 99

#boosts
OVLNONE = 0
OVLNM = 1
OVLSPREME = 2
OVLELDER = 3
OVERLOADTYPE = 3 #OVLNONE if not using overloads, OVLNM for normal ovl, OVLSPREME for supreme ovl, OVLELDER for elder ovl
PRAYERBOOST = 0.12 #% of damage boost from prayer. turmoil vairant is 0.1, praesul variant is 0.12
VIGOUR = 0 #0 if not using, 1 if using ring of vigour
OTHERDMGMULTIPLIER = 1*1 #multiply all other multiplier. e.g. slave amulet(e) and slayer helmet = 1.2 * 1.145.
#list of multipliers found here : https://runescape.wiki/w/Ability_damage#Other_boosts

#overhead prayers
SOULSPLIT = 0 #1 if on, 0 if not
DEFLECTCURSE = 0

#poison wont be calculated if no cinderbane is equipped, since increase will be miniscule
WEAPONPOISON = 4 #0 if not using weapon poison, 1 if normal wp, 2 if +, 3 if ++, 4 if +++
KWUARMINCPOTENCY = 4 #potency of kwuarm incense sticks
CINDERBANE = 1 #0 if not using, 1 if using cinderbane gloves

#crit boosts
KALDEMON = 0 #0 if not using, 1 if using kalgelion demon
KALDEMONSCROLL = 0 #0 if not using, 1 if using kalg demon scroll
GRIMOIRE = 0
REAVERSRING = 1
STALKERSRING = 0
CHAMPIONSRING = 0 #3%crit boost to bleeding target, not 

#familiar (kalgerion demon is in crit boost section)
RIPPERDEMON = 1
BLOODREAVER = 0

#invention perks
RELENTLESS = 0
RELENTLESSGEARLV = 20
RELENTLESSCD = 30 #seconds

IMPATIENT = 0
IMPATIENTGEARLV = 20

BITING = 4
BITINGGEARLV = 19

INVIGORATING = 0
INVIGORATINGGEARLV = 20

PRECISE = 0
EQUI = 0
AFTERSHOCK = 4
PLANTEDFEET = 1
RUTHELESS = 2
RUTHELESSSTACK = 5
LUNGING = 0
CAROMING = 3

MOBSALYER = 1 #1 if have perk of demon/dragon/undead slayer 

#aura
BERSERKAURA = 0
INSPIRATIONAURA = 0 #1 if using inspiration aura, 0 if not
VAMPAURA = 1

#pocket slot 
VAMPSCRIM = 0 #0 if none, 1 if normal, 2 if superior vamp scrim
WENBOOK = 0
JASBOOK = 0
FULBOOK = 0

#arch relics
FURYOFTHESMALL = 1 # 0 if inactive, 1 if active
CONSERVATIONOFENERGY = 0 #0 if not using, 1 if using the relic "conservation of energy"
HEIGHTENEDSENSES = 0

#other
INITADREN = 100.0 #starting amount of adrenaline, float
CANNON = 10 #0 if not using, 1 if kinetic cyclone, 2 if oldak coil, 3 if dwarf multi cannon, multiply by 10 if upgraded
AVERAGENENEMIES = 5.5 #average number of enemies you attack at once
ENEMYHEALTH = 33563
ENEMYAVERAGEDMG = 1000 #average damage from 1 raw hit (without prayer/any reduction)
ENEMYATTACKINTERVAL = 1.5 #tick between attacks
HITCHANCE = 1 #hit chance agianst enemies




####DONT TOUCH , some variables used in script ###
NOBERSERK = 0
BERSERK = 1
SUNSHINE = 2
DEATHSSWIFTNESS = 3
NOTACTIVE = 0
ACTIVE = 1
POISONPROCCHANCE = 1/6