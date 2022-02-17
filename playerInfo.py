#player stat, armour
ACCURACY = 4479
STRENGTHBONOUS = 1000 #for all 3 combat styles
INQUISITOR = 1 #1 if using inquisitor/hexhunter/omen
DUALWIELD = 0 #0 if 2h weapon, 1 if dual wield
STYLEMAGIC = 1
STYLERANGED = 2
STYLEMELEE = 3
STYLE = STYLEMAGIC #1 = magic, 2 = ranged, 3 = melee

#magic wp, spells
MAGICMHTIER = 90
MAGICOHTIER = 90
MAGIC2HTIER = 80
MHSPELLDMG = 100
OHSPELLDMG = 100
TWOHSPELLDMG = 100

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
OVLNM = 1
OVLSPREME = 2
OVLELDER = 3
OVERLOADTYPE = OVLELDER #0 if not using overloads, 1 for normal ovl, 2 for supreme ovl, 3 for elder ovl
TURMOILPRAYER = 2 #0 if not using damage boosting prayer, 1 if turmoil variant, 2 if praesul variant
VIGOUR = 0 #0 if not using, 1 if using ring of vigour
OTHERDMGMULTIPLIER = 1*1 #multiply all other multiplier. e.g. slave amulet(e) and slayer helmet = 1.2 * 1.145.
#list of multipliers found here : https://runescape.wiki/w/Ability_damage#Other_boosts

#poison stuff
WEAPONPOISON = 3 #0 if not using weapon poison, 1 if +, 2 if ++, 3 if +++
KWUARMINCPOTENCY = 4 #potency of kwuarm incense sticks
CINDERBANE = 1 #0 if not using, 1 if using cinderbane gloves

#crit boosts
REAVERSRING = 1
KALDEMON = 0 #0 if not using, 1 if using kalgelion demon
KALDEMONSCROLL = 0 #0 if not using, 1 if using kalg demon scroll
GRIMOIRE = 0
STALKERSRING = 0
CHAMPIONSRING = 0 #3%crit boost to bleeding target, not implemented yet

#familiar (kalgerion demon is in crit boost section)
RIPPERDEMON = 1
BLOODREAVER = 0

#invention perks
RELENTLESS = 5
RELENTLESSGEARLV = 20
RELENTLESSCD = 30 #seconds

IMPATIENT = 4
IMPATIENTGEARLV = 20

BITING = 4
BITINGGEARLV = 19

INVIGORATING = 0
INVIGORATINGGEARLV = 20

PRECISE = 6
EQUI = 4
AFTERSHOCK = 4
PLANTEDFEET = 1
RUTHELESS = 3
RUTHELESSSTACK = 5
LUNGING = 4
CAROMING = 4

#aura
BERSERKAURA = 0
INSPIRATIONAURA = 0 #1 if using inspiration aura, 0 if not

#arch relics
FURYOFTHESMALL = 1 # 0 if inactive, 1 if active
CONSERVATIONOFENERGY = 0 #0 if not using, 1 if using the relic "conservation of energy"
HEIGHTENEDSENSES = 0

#other
INITADREN = 100.0 #starting amount of adrenaline, float
CANNON = 10 #0 if not using, 1 if kinetic cyclone, 2 if oldak coil, 3 if dwarf multi cannon, *10 if upgraded
AVERAGENENEMIES = 4 #average number of enemies you attack at once
HITCHANCE = 1 #hit chance agianst enemies

#some variables
NOBERSERK = 0
BERSERK = 1
SUNSHINE = 2
DEATHSSWIFTNESS = 3
NOTACTIVE = 0
ACTIVE = 1